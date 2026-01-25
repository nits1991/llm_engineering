"""
Content Templates Module
=========================

Predefined templates for different types of content generation.
Add new templates here to extend the application's capabilities.
"""

CONTENT_TEMPLATES = {
    "Company Brochure": {
        "description": """
        📋 **Company Brochure Template**
        
        Generates a professional company brochure including:
        - Company overview and mission
        - Products/services
        - Company culture
        - Career opportunities
        - Customer information
        
        Perfect for prospective customers, investors, and recruits.
        """,
        "system_prompt": """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
Use professional tone and highlight key strengths.
        """,
        "user_prompt_template": """
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.

"""
    },

    "Humorous Brochure": {
        "description": """
        😄 **Humorous Brochure Template**
        
        Generates an entertaining, witty company brochure with humor while
        maintaining professionalism. Great for:
        - Creative companies
        - Internal presentations
        - Fun marketing materials
        """,
        "system_prompt": """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short, humorous, entertaining, witty brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
Make it fun but keep it professional and informative.
        """,
        "user_prompt_template": """
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a fun, witty brochure of the company in markdown without code blocks.

"""
    },

    "Job Postings Summary": {
        "description": """
        💼 **Job Postings Summary**
        
        Analyzes career/jobs pages and creates a summary of:
        - Available positions
        - Key requirements
        - Company culture/benefits
        - Application process
        - Salary ranges (if available)
        
        Useful for job seekers and recruiters.
        """,
        "system_prompt": """
You are an assistant that analyzes job postings and career pages from a company website.
Create a comprehensive summary of available positions including:
- Job titles and roles
- Key requirements and qualifications
- Benefits and perks
- Company culture highlights
- Salary information if available
- Application process

Respond in markdown without code blocks. Organize by department or role type.
        """,
        "user_prompt_template": """
Analyze the career and job pages for: {company_name}
Create a detailed summary of their job openings and opportunities.

"""
    },

    "Investment Pitch": {
        "description": """
        💰 **Investment Pitch Template**
        
        Creates an investor-focused document highlighting:
        - Business model
        - Market opportunity
        - Competitive advantages
        - Growth metrics
        - Financial health indicators
        
        Perfect for pitch decks and investor presentations.
        """,
        "system_prompt": """
You are an investment analyst creating a pitch summary for potential investors.
Analyze the company website and highlight:
- Business model and revenue streams
- Market opportunity and size
- Competitive advantages and moats
- Growth trajectory and metrics
- Key partnerships and customers
- Management team highlights

Use data-driven language, focus on ROI potential, and maintain professional investor-focused tone.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create an investment pitch summary for: {company_name}
Focus on investment opportunities and business potential.

"""
    },

    "Product Catalog": {
        "description": """
        🛍️ **Product Catalog Template**
        
        Generates a product/service catalog including:
        - Product descriptions
        - Key features
        - Use cases
        - Pricing information (if available)
        - Product categories
        """,
        "system_prompt": """
You are a product specialist creating a catalog of a company's products and services.
Analyze the website and create a structured catalog including:
- Product/service names and categories
- Key features and benefits
- Use cases and target customers
- Pricing information if available
- Technical specifications if relevant

Organize by category and make it easy to scan.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create a product/service catalog for: {company_name}
List and describe all their offerings.

"""
    },

    "Competitive Analysis": {
        "description": """
        📊 **Competitive Analysis Template**
        
        Analyzes the company from a competitive perspective:
        - Unique selling points
        - Market positioning
        - Strengths and advantages
        - Target market
        - Differentiators
        """,
        "system_prompt": """
You are a market analyst creating a competitive analysis report.
Analyze the company website and identify:
- Unique selling propositions (USPs)
- Market positioning and target segments
- Key strengths and competitive advantages
- Value propositions
- Differentiators from competitors

Use analytical tone, be objective, and focus on strategic insights.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create a competitive analysis report for: {company_name}
Focus on their market position and competitive advantages.

"""
    },

    "Company Culture Report": {
        "description": """
        🏢 **Company Culture Report**
        
        Deep dive into company culture:
        - Values and mission
        - Work environment
        - Employee benefits
        - Diversity and inclusion
        - Team structure
        - Work-life balance
        """,
        "system_prompt": """
You are an HR analyst creating a company culture report.
Analyze the website for insights about:
- Company values and mission
- Work environment and office culture
- Employee benefits and perks
- Diversity, equity, and inclusion initiatives
- Team structure and collaboration style
- Work-life balance philosophy
- Employee growth opportunities

Write in an engaging, people-focused tone.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create a company culture report for: {company_name}
Focus on what it's like to work there.

"""
    },

    "Technical Overview": {
        "description": """
        🔧 **Technical Overview Template**
        
        Technical deep-dive for developers/engineers:
        - Technology stack
        - Product architecture
        - APIs and integrations
        - Technical documentation
        - Developer resources
        """,
        "system_prompt": """
You are a technical writer creating a technical overview for developers and engineers.
Analyze the website for technical information including:
- Technology stack and platforms
- Product architecture and infrastructure
- APIs and integration capabilities
- Developer tools and resources
- Technical documentation availability
- Open source contributions

Use technical language appropriate for a developer audience.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create a technical overview for: {company_name}
Focus on their technology and developer resources.

"""
    },

    "Customer Success Stories": {
        "description": """
        ⭐ **Customer Success Stories**
        
        Highlights customer achievements:
        - Client testimonials
        - Use cases
        - Success metrics
        - ROI examples
        - Customer profiles
        """,
        "system_prompt": """
You are a content marketer creating a customer success stories document.
Extract and highlight:
- Customer testimonials and quotes
- Real-world use cases
- Success metrics and ROI
- Problem-solution narratives
- Customer profiles and industries served
- Results and achievements

Make it compelling and results-focused.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create a customer success stories document for: {company_name}
Focus on how they help their customers succeed.

"""
    },

    "Executive Summary": {
        "description": """
        📝 **Executive Summary Template**
        
        High-level summary for executives:
        - Company snapshot
        - Key metrics
        - Strategic priorities
        - Market position
        - Future outlook
        """,
        "system_prompt": """
You are creating an executive summary for C-level stakeholders.
Provide a concise, high-level overview including:
- Company snapshot (what they do, who they serve)
- Key metrics and achievements
- Strategic priorities and focus areas
- Market position and competitive landscape
- Future outlook and growth areas

Keep it brief, impactful, and decision-maker focused.
Use bullet points for key information.
Respond in markdown without code blocks.
        """,
        "user_prompt_template": """
Create an executive summary for: {company_name}
Focus on high-level strategic information.

"""
    }
}

# Custom template function for user-defined templates


def create_custom_template(name: str, description: str, system_prompt: str) -> dict:
    """
    Create a custom template dynamically.

    Args:
        name: Template name
        description: Template description for UI
        system_prompt: System prompt for the LLM

    Returns:
        Template dictionary
    """
    return {
        "description": description,
        "system_prompt": system_prompt,
        "user_prompt_template": """
You are analyzing: {company_name}
Here are the contents of their website pages:

"""
    }
