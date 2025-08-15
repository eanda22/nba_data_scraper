# nba_data_scraper/player.py

import pandas as pd
from typing import Optional
from io import StringIO
import logging

# Import from our own library files
from .utils import get_data, BASE_URL

logger = logging.getLogger(__name__)

class Player:
    """Represents a single player and provides methods to access their stats."""
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.url = f"{BASE_URL}/players/{player_id[0]}/{player_id}.html"
        logger.debug(f"Initializing Player for ID: {player_id}")
        self._tables, self._soup = get_data(self.url)

        if self._tables is None and self._soup is None:
            raise ValueError(f"Failed to get data for player: {player_id}")

    def get_per_game_stats(self) -> Optional[pd.DataFrame]:
        if self._tables:
            return self._tables[0]
        logger.warning(f"No tables found for {self.player_id}.")
        return None

    def get_advanced_stats(self) -> Optional[pd.DataFrame]:
        if self._soup:
            adv_table_html = self._soup.find('table', id='advanced')
            if adv_table_html:
                return pd.read_html(StringIO(str(adv_table_html)))[0]
        logger.warning(f"Could not find advanced stats table for {self.player_id}.")
        return None

    def get_bio(self) -> Optional[dict]:
        """Returns a dictionary containing biographical information."""
        if not self._soup:
            return None

        bio_div = self._soup.find('div', id='info')
        if not bio_div:
            logger.warning(f"Could not find bio info div for {self.player_id}.")
            return None

        # --- Defensive Scraping: Find each element and check before use ---
        
        name_element = bio_div.find('span', itemprop='name')
        name = name_element.text.strip() if name_element else "Unknown"

        height_element = bio_div.find('span', itemprop='height')
        height = height_element.text.strip() if height_element else "Unknown"

        weight_element = bio_div.find('span', itemprop='weight')
        weight = weight_element.text.strip() if weight_element else "Unknown"

        # The weight is now in a separate line from its label, so we clean it up
        if weight_element:
            weight_text = weight_element.find_next_sibling(text=True).strip()
            weight = f"{weight_text} lbs"

        return {
            "name": name,
            "height": height,
            "weight": weight,
        }