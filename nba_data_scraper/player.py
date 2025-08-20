# nba_data_scraper/player.py

import pandas as pd
from typing import Optional
import logging
import re

# Import from our own library files
from .utils import convert_soup_to_dataframe, get_soup, BASE_URL

logger = logging.getLogger(__name__)


class Player:
    """Represents a single player and provides methods to access their stats."""

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.player_id = self._get_player_id(player_name)
        if not self.player_id:
            raise ValueError(f"Could not find player ID for {player_name}")
        self.first_initial = self.player_id[0]
        self.PLAYER_PAGE_URL = (
            f"{BASE_URL}/players/{self.first_initial}/{self.player_id}.html"
        )
        self.PLAYER_GAMELOG_URL = (
            f"{BASE_URL}/players/{self.first_initial}/{self.player_id}/gamelog/{{}}"
        )

    def _get_player_id(self, player_name):
        """
        Returns the player ID for a given player name.
        """
        search_url = (
            f"{BASE_URL}/search/search.fcgi?search={player_name.replace(' ', '+')}"
        )
        logger.info(f"Searching for player ID for: {player_name}")

        soup = get_soup(search_url)
        if not soup:
            logger.error(f"Failed to fetch search results for {player_name}.")
            return None
        player_link = soup.find("a", href=re.compile(r"/players/.*\.html"))

        if player_link:
            return player_link["href"].split("/")[-1].replace(".html", "")

        logger.warning(f"No player ID found for {player_name}.")
        return None

    def get_all_per_game_stats(self):
        """
        Fetches all per game stats for the player.
        """
        url = self.PLAYER_PAGE_URL.format(self.player_id[0], self.player_id)
        logger.info(f"Fetching all per game stats from: {url}")

        soup = get_soup(url)
        if not soup:
            logger.error(f"No soup found at {url}.")
            return None
        table_id = "per_game_stats"
        per_game_table = convert_soup_to_dataframe(soup, table_id)
        if per_game_table is None:
            logger.warning(f"No per game stats table found for {self.player_name}.")
            return None
        return per_game_table

    def get_game_log_stats(self, season):
        """
        Fetches game log for the player for a specific season.
        """
        url = self.PLAYER_GAMELOG_URL.format(season)
        logger.info(f"Fetching game log from: {url}")

        soup = get_soup(url)
        if not soup:
            logger.error(f"No soup found at {url}.")
            return None

        table_id = f"player_game_log_reg"
        game_log_table = convert_soup_to_dataframe(soup, table_id)
        if game_log_table is None:
            logger.warning(
                f"No game log table found for {self.player_name} in season {season}."
            )
            return None
        return game_log_table
