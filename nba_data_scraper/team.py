# nba_data_scraper/team.py

import pandas as pd
from typing import Optional
from io import StringIO
import logging

# Import from our own library files
from .utils import get_data, BASE_URL

logger = logging.getLogger(__name__)

class Team:
    """Represents a single team for a specific season."""
    def __init__(self, team_abbr: str, year: int):
        self.team_abbr = team_abbr.upper()
        self.year = year
        self.url = f"{BASE_URL}/teams/{self.team_abbr}/{self.year}.html"
        logger.debug(f"Initializing Team: {team_abbr} {year}")
        self._tables, self._soup = get_data(self.url)

        if self._tables is None and self._soup is None:
            raise ValueError(f"Failed to get data for team: {team_abbr} in {year}")

    def get_roster(self) -> Optional[pd.DataFrame]:
        if self._soup:
            roster_table = self._soup.find('table', id='roster')
            if roster_table:
                return pd.read_html(StringIO(str(roster_table)))[0]
        logger.warning(f"Could not find roster table for {self.team_abbr} {self.year}.")
        return None

    def get_team_stats(self) -> Optional[pd.DataFrame]:
        if self._soup:
            stats_table = self._soup.find('table', id='team_stats')
            if stats_table:
                return pd.read_html(StringIO(str(stats_table)))[0]
        logger.warning(f"Could not find team stats table for {self.team_abbr} {self.year}.")
        return None