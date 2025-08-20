# nba_data_scraper/utils.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from typing import List, Tuple, Optional
import logging
import re

# Set up a logger for the library
logger = logging.getLogger(__name__)

# Define a base URL for easier construction of links
BASE_URL = "https://www.basketball-reference.com"


def get_html_tables(url: str):
    """
    Fetches HTML content from a URL and returns a list of DataFrames for all tables found.
    """
    logger.info(f"Fetching HTML tables from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.read_html(StringIO(response.text))
    except (requests.exceptions.RequestException, ValueError) as e:
        logger.error(f"Error fetching or parsing tables from {url}: {e}")
        return []


def get_soup(url: str):
    """
    Fetches HTML content from a URL and returns a BeautifulSoup object.
    """
    logger.info(f"Fetching HTML content from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None


def convert_soup_to_dataframe(soup, table_id):
    """
    Converts a BeautifulSoup object containing a table to a pandas DataFrame.
    """
    logger.debug(f"Converting soup to DataFrame for table ID: {table_id}")
    table = soup.find("table", id=table_id)
    if not table:
        logger.warning(f"No table found with ID: {table_id}")
        return None
    return pd.read_html(StringIO(str(table)))[0]
