# nba_data_scraper/utils.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from typing import List, Tuple, Optional
import logging

# Set up a logger for the library
logger = logging.getLogger(__name__)

# Define a base URL for easier construction of links
BASE_URL = "https://www.basketball-reference.com"

def get_data(url: str) -> Tuple[Optional[List[pd.DataFrame]], Optional[BeautifulSoup]]:
    """
    Fetches and parses HTML content from a URL.
    """
    logger.info(f"Fetching data from: {url}")
    headers = {"User-Agent": "nba-data-scraper"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None, None

    try:
        all_tables = pd.read_html(StringIO(response.text))
    except (ImportError, ValueError) as e:
        logger.warning(f"No tables found on page {url}. Error: {e}")
        all_tables = None

    soup = BeautifulSoup(response.text, 'html.parser')
    return all_tables, soup