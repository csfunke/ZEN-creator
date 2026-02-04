from __future__ import annotations
from functools import cached_property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.dataset import Dataset
import pandas as pd
import scipy.stats as stats

class ECB(Dataset):
    """Dataset class for ECB data."""

    def __init__(self, model: Model):
        super().__init__(name="ecb", model=model)

    # ------ Metadata properties ------
    @property
    def author(self) -> str:
        return "European Central Bank"
    
    @property
    def publication_year(self) -> int:
        return 2025
    
    @property
    def url(self) -> str:
        return "https://data.ecb.europa.eu/"
    
    @cached_property
    def inflation_rate(self) -> float:
        """Method to get the inflation rate."""
        return self.get_inflation_rate()
    
    # ----- Methods to get data -----
    def get_inflation_rate(self) -> float:
        """Method to get the inflation rate from ECB data."""
        url = "https://data-api.ecb.europa.eu/service/data/ICP/M.U2.N.000000.4.ANR?format=csvdata"
        df = pd.read_csv(url)
        df_sel = df[["TIME_PERIOD","OBS_VALUE"]].set_index("TIME_PERIOD").astype(float).squeeze()
        df_sel.index = pd.MultiIndex.from_tuples(df_sel.index.map(lambda x: (int(x.split("-")[0]), int(x.split("-")[1]))),names=["year","month"])
        inflation = (df_sel/100+1).groupby(level="year").apply(stats.gmean)
        return inflation

    def calculate_inflation_rate(self, base_year: int, target_year: int) -> float:
        """Method to calculate the inflation rate between two years."""
        inflation_rate = self.inflation_rate
        years_diff = target_year - base_year
        inflation = float(inflation_rate.loc[base_year:target_year-1].prod())
        return inflation