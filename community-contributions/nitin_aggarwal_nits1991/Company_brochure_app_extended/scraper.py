"""
Web Scraper Module
==================

Functions for fetching website content and links using BeautifulSoup.
"""

from bs4 import BeautifulSoup
import requests
from typing import List, Optional

# Standard headers to mimic browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url: str, max_length: int = 2000) -> str:
    """
    Fetch and extract text content from a website.

    Args:
        url: Website URL to fetch
        max_length: Maximum characters to return (default: 2000)

    Returns:
        String containing page title and body text

    Raises:
        requests.RequestException: If request fails
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        title = soup.title.string if soup.title else "No title found"

        # Extract body text
        if soup.body:
            # Remove irrelevant elements
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        # Combine and truncate
        content = f"{title}\n\n{text}"
        return content[:max_length]

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch {url}: {str(e)}")


def fetch_website_links(url: str) -> List[str]:
    """
    Extract all links from a webpage.

    Args:
        url: Website URL to fetch

    Returns:
        List of links found on the page

    Raises:
        requests.RequestException: If request fails
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all links
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                # Convert relative links to absolute
                if href.startswith("/") and not href.startswith("//"):
                    # Extract base URL
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    href = base_url + href
                links.append(href)

        return links

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch links from {url}: {str(e)}")


def validate_url(url: str) -> bool:
    """
    Validate if URL is properly formatted.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
