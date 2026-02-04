from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Optional
import pandas as pd

class Dataset(ABC):
    """Dataset class for general datasets."""
    def __init__(self,name: str, model: Model):
        self.name = name
        self.model = model
        self.create_time_interval()

    @cached_property
    def metadata(self) -> dict:
        return {
            "name": self.name,
            "author": self.author,
            "publication_year": self.publication_year,
            "url": self.url,
            "doi": self.doi
        }

    @property
    @abstractmethod
    def author(self) -> str:
        pass

    @property
    @abstractmethod
    def publication_year(self) -> int:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @cached_property
    def doi(self) -> Optional[str]:
        return None

    # ----- Methods to get data -----
    def create_time_interval(self):
        """ this method sets a year and then creates the time interval for which the data is extracted """
        # set year for which data is extracted
        self.data_general_year = self.model.config.time_settings.data_general_year
        self.data_timeseries_year = self.model.config.time_settings.data_timeseries_year
        self.time_start = pd.Timestamp(year=self.data_general_year, month=1, day=1, hour=0, tz='Europe/Brussels')
        self.time_end = pd.Timestamp(year=self.data_general_year + 1, month=1, day=1, hour=0, tz='Europe/Brussels')
        self.time_start_ts = pd.Timestamp(year=self.data_timeseries_year, month=1, day=1, hour=0, tz='Europe/Brussels')
        self.time_end_ts = pd.Timestamp(year=self.data_timeseries_year + 1, month=1, day=1, hour=0, tz='Europe/Brussels')
        self.time_start_history = pd.Timestamp(year=1900, month=1, day=1, hour=0, tz='Europe/Brussels')
        self.time_end_history = pd.Timestamp.today()
        self.time_range = pd.date_range(self.time_start, self.time_end, freq="h")[:-1]
        self.time_range_ts = pd.date_range(self.time_start_ts, self.time_end_ts, freq="h")[:-1]