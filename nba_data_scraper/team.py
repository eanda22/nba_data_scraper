# nba_data_scraper/team.py

import pandas as pd
from typing import Optional
from io import StringIO
import logging

# Import from our own library files
from .utils import get_soup, convert_soup_to_dataframe, BASE_URL

logger = logging.getLogger(__name__)


class Team:
    """Represents a single team for a specific season."""

    TEAM_URL = f"{BASE_URL}/teams/{{}}/{{}}.html"

    def __init__(self, team_abbr, year):
        self.team_abbr = team_abbr.upper()
        self.year = year

    def get_roster(self):
        """
        Fetches the roster for the team for the specified year
        """
        url = self.TEAM_URL.format(self.team_abbr, self.year)
        logger.info(f"Fetching roster from: {url}")

        soup = get_soup(url)
        if not soup:
            logger.error(f"No soup found at {url}.")
            return None

        table_id = "roster"
        roster_table = convert_soup_to_dataframe(soup, table_id)
        if roster_table is None:
            logger.warning(
                f"No roster table found for {self.team_abbr} in {self.year}."
            )
            return None
        return roster_table

    def get_team_stats(self):
        """
        Fetches the team stats for the specified year
        """
        url = self.TEAM_URL.format(self.team_abbr, self.year)
        logger.info(f"Fetching team stats from: {url}")

        soup = get_soup(url)
        if not soup:
            logger.error(f"No soup found at {url}.")
            return None

        table_id = "per_game_stats"
        stats_table = convert_soup_to_dataframe(soup, table_id)
        if stats_table is None:
            logger.warning(
                f"No team stats table found for {self.team_abbr} in {self.year}."
            )
            return None
        return stats_table
