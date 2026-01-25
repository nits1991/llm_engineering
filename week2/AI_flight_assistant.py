from openai import OpenAI
from dotenv import load_dotenv
import json
import gradio as gr
import os


load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

Model = "gpt-4.1-mini"
openai = OpenAI()

# set the system Prompt
system_prompt_ai_flight_assistant = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

# Chat Function Journey


def chat(message, history):
    sanitized_history = []
    for h in history:
        sanitized_history.append({"role": h["role"], "content": h["content"]})

    messages_new = [
        {"role": "system", "content": system_prompt_ai_flight_assistant}
    ] + sanitized_history + [{"role": "user", "content": message}]

    for msg in messages_new:
        print("==========================================================")
        print(f"Full Messages :{msg}")

    response = openai.chat.completions.create(
        model=Model,
        messages=messages_new,
        tools=tools
    )
    # Check if tool call was made
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        # Convert message to dict for JSON serialization
        message_dict = {
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        }
        print(f"message in while loop:{json.dumps(message_dict, indent=2)}")
        responses = handle_tool_calls(message)
        print(f"handle_tool_calls_response:{json.dumps(responses, indent=2)}")
        messages_new.append(message_dict)
        messages_new.extend(responses)
        print(
            f"messages_new after tool call : {json.dumps(messages_new, indent=2)}")
        response = openai.chat.completions.create(
            model=Model, messages=messages_new, tools=tools)

    # Always return a string, never None
    content = response.choices[0].message.content
    return content if content else "I apologize, but I couldn't process that request."
    # result = response.choices[0].message.content
    # return result


# Let's start by making a useful function
ticket_prices = {"london": "$799", "paris": "$899",
                 "tokyo": "$1400", "berlin": "$499"}

# Tool Function


def get_ticket_price_tool(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"


# Tool Json
# There's a particular dictionary structure that's required to describe our function:

get_ticket_price_tool_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}


def set_ticket_price_tool(destination_city, price):
    ticket_prices[destination_city.lower()] = price
    return f"Set ticket price for {destination_city} to {price}"


set_ticket_price_tool_function = {
    "name": "set_ticket_price_tool",
    "description": "Set the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
            "price": {
                "type": "string",
                "description": "The price of the ticket to the destination city",
            },
        },
        "required": ["destination_city", "price"],
        "additionalProperties": False
    }
}

print("set_ticket_price_tool_function:", json.dumps(
    set_ticket_price_tool_function, indent=2))
print("get_ticket_price_function:", json.dumps(
    get_ticket_price_tool_function, indent=2))


tools = [{"type": "function", "function": get_ticket_price_tool_function},
         {"type": "function", "function": set_ticket_price_tool_function}]

print(tools)


def handle_tool_calls(message):
    responses = []
    print(f"message in handle_tool_calls:{json.dumps(message, indent=2)}")
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_details = get_ticket_price_tool(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "set_ticket_price_tool":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price = arguments.get('price')
            result = set_ticket_price_tool(city, price)
            responses.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })
    return responses


gr.ChatInterface(
    fn=chat,
    title="FlightAI Chatbot",
    type="messages"
).launch()
