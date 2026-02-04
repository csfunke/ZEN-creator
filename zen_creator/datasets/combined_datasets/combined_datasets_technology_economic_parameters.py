from __future__ import annotations
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.combined_datasets.combined_datasets import CombinedDataset
from zen_creator.datasets.single_datasets.techno_economic_dataset import TechnoEconomicDataset

import pandas as pd

class CombinedDatasetTechnoEconomicParameters(CombinedDataset):
    """Class for techno-economic parameters."""

    def __init__(self, model: Model):
        super().__init__(name="combined_techno_economic_parameters", model=model)
        self.load_data_sources()
    
    @property
    def author(self) -> str | None:
        return None
    
    @property
    def publication_year(self) -> int | None:
        return None
    
    @property
    def url(self) -> str | None:
        return None
    

    def load_data_sources(self):
        """Load all available techno-economic data sources."""
        self.data_sources: list[TechnoEconomicDataset] = []
        for dataset_class in TechnoEconomicDataset.__subclasses__():
            data_source_instance = dataset_class(self.model)
            data_source_instance.load_raw_data()
            self.data_sources.append(data_source_instance)
    
    def get_cost_data(self, technology: str, variable: str) -> pd.DataFrame | None:
        """Get the finance data of a technology."""
        df_finance_list = []
        for data_source in self.data_sources:
            if technology in data_source.available_technologies_finance:
                df_finance = data_source.get_cost_data(technology, variable)
                if df_finance is None:
                    continue
                assert df_finance.index.name == "year", "Finance dataframe index must be 'year'"
                if isinstance(df_finance, pd.DataFrame):
                    df_finance = df_finance.mean(axis=1)
                missing_years = set(data_source.get_years()).difference(df_finance.index)
                if missing_years:
                    df_finance = df_finance.reindex(data_source.get_years())
                    df_finance = df_finance.interpolate(method='linear', limit_direction='both')
                df_finance_list.append(df_finance)
        if df_finance_list:
            df_finance_concat = pd.concat(df_finance_list, axis=1)
            # average over data sources
            if len(df_finance_concat.columns) > 1:
                df_finance_avg = df_finance_concat.mean(axis=1)
            else:
                df_finance_avg = df_finance_concat
            return df_finance_avg.astype(float)
        return None
    
    def get_lifetime(self, technology: str) -> float | None:
        """Get the lifetime of a technology."""
        df_lifetimes = {}
        for data_source in self.data_sources:
            if technology in data_source.available_technologies_lifetime:
                df_lt = data_source.get_lifetime(technology)
                assert df_lt.index.name == "year", "Lifetime dataframe index must be 'year'"
                if isinstance(df_lt, pd.Series):
                    lt = df_lt.iloc[0]
                elif isinstance(df_lt, pd.DataFrame):
                    lt = df_lt.mean(axis=1).iloc[0]
                else:
                    raise ValueError(f"Lifetime data type '{type(df_lt)}' not recognized.")
                df_lifetimes[data_source.name] = int(lt)
        if df_lifetimes:
            df_lifetime = pd.Series(df_lifetimes)
            lifetime = int(df_lifetime.median())
            return lifetime
        return None

    def get_efficiency(self, technology: str) -> float | None:
        """Get the efficiency of a technology."""
        df_effs = {}
        for data_source in self.data_sources:
            if technology in data_source.available_technologies_efficiency:
                df_eff = data_source.get_efficiency(technology)
                assert df_eff.index.name == "year", "Efficiency dataframe index must be 'year'"
                if isinstance(df_eff, pd.Series):
                    eff = df_eff.iloc[0]
                elif isinstance(df_eff, pd.DataFrame):
                    eff = df_eff.mean(axis=1).iloc[0]
                else:
                    raise ValueError(f"Efficiency data type '{type(df_eff)}' not recognized.")
                df_effs[data_source.name] = float(eff)
        if df_effs:
            df_efficiency = pd.Series(df_effs)
            efficiency = float(df_efficiency.mean())
            return efficiency
        return None

    def get_construction_time(self, technology: str) -> float | None:
        """Get the construction time of a technology."""
        raise NotImplementedError("Construction time retrieval not finalized yet. Analagous to get_efficiency and get_lifetime methods.")
        df_cts = {}
        for data_source in self.data_sources:
            if technology in data_source.available_technologies_construction_time:
                df_ct = data_source.get_construction_time(technology)
                df_cts[data_source.name] = df_ct
        if df_cts:
            df_ct = pd.Series(df_cts)
            return df_ct
        return None
