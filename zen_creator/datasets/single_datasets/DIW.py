from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.single_datasets.techno_economic_dataset import TechnoEconomicDataset
import pandas as pd

class DIW(TechnoEconomicDataset):
    """Dataset class for the DIW source data."""

    def __init__(self, model: Model):
        super().__init__(name="diw", model=model)

    # ------ Metadata properties ------
    @property
    def author(self) -> str:
        return "DIW Berlin"
    
    @property
    def publication_year(self) -> int:
        return 2018
    
    @property
    def url(self) -> str:
        return "https://ars.els-cdn.com/content/image/1-s2.0-S2211467X19301142-mmc1.pdf"
    
    @property
    def money_year_source(self) -> int:
        return 2018
    
    @property
    def unit(self) -> str:
        return "Euro/kW"
    
    # ----- Methods to get data -----
    def load_raw_data(self):
        """Method to load the raw techno-economic data."""
        url = self.source_path / "capex_diw.xlsx"
        raw_finance_data = pd.read_excel(url,header=1,sheet_name="costs").set_index(["Technology"])
        raw_eff_data = pd.read_excel(url,header=1,sheet_name="efficiency").set_index(["Efficiency"])
        raw_lt_data = pd.read_excel(url,sheet_name="lifetime").set_index("Column1")
        raw_finance_data.columns = raw_finance_data.columns.astype(int)
        raw_finance_data = self.rename_finance_tech(raw_finance_data)
        raw_eff_data = self.rename_efficiency_tech(raw_eff_data)
        raw_lt_data = self.rename_lt_tech(raw_lt_data)

        finance_index = pd.MultiIndex.from_product(
            [raw_finance_data.index, ["capex"]],names=["technology","variable"])
        raw_finance_data.index = finance_index
        inflation = self.model.datasets["ecb"].calculate_inflation_rate(base_year=self.money_year_source, target_year=self.model.config.time_settings.data_general_year)
        raw_finance_data = raw_finance_data * inflation

        self.raw_data = {
            "finance": raw_finance_data,
            "efficiency": raw_eff_data,
            "lifetime": raw_lt_data
        }
        self.set_available_technologies(finance=raw_finance_data, efficiency=raw_eff_data, lifetime=raw_lt_data)

    def rename_finance_tech(self,df: pd.DataFrame) -> pd.DataFrame:
        """Method to rename finance and techno-economic parameters."""
        DIW_names = {
            'wind_onshore': "OnshoreWind",
            'wind_offshore_near_shore':"OffshoreWind[shallow]",
            'wind_offshore':"OffshoreWind[transitional]",
            'photovoltaics': "PVUtility",
            'rooftop_photovoltaics': "PVRooftop[residential]",
            'rooftop_photovoltaics_com': "PVRooftop[commercial]",
            "solar_thermal": "CSP",
            "run-of-river_hydro": "Hydro[small]",
            "reservoir_hydro": "Hydro[large]",
            'natural_gas_turbine': "GasPowerPlant(CCGT)",
            'natural_gas_turbine_CCS': "GasPowerPlant(CCGT)+CCTS",
            'hard_coal_plant': "HardCoalPowerPlant",
            'hard_coal_plant_CCS': "HardCoalPowerPlant+CCTS",
            'lignite_coal_plant': "LignitePowerPlant",
            'lignite_coal_plant_CCS': "LignitePowerPlant+CCTS",
            "nuclear": "NuclearPowerPlant",
            'biomass_plant': "BiomassPowerPlant",
            'biomass_plant_CCS': "BiomassPowerPlant+CCTS",
            'oil_plant': "OilPowerPlant(CCGT)",
            "fuel_cell": "FuelCell"
        }
        df_renamed = self.rename_index(df, DIW_names)      
        df_renamed.index.name = "technology"
        return df_renamed
    
    def rename_efficiency_tech(self,df: pd.DataFrame) -> pd.DataFrame:
        """Method to rename efficiency techno-economic parameters."""
        DIW_names = {
            'natural_gas_turbine': "CCGT(NaturalGas)",
            'hard_coal_plant': "HardCoal",
            'lignite_coal_plant': "Lignite",
            "nuclear": "Nuclear",
            'oil_plant': "CCGT(Oil)",
        }
        df_renamed = self.rename_index(df, DIW_names)      
        df_renamed.index.name = "technology"
        return df_renamed
    
    def rename_lt_tech(self,df: pd.DataFrame) -> pd.DataFrame:
        """Method to rename lifetime techno-economic parameters."""
        DIW_names = {
            'wind_onshore': "OnshoreWind",
            'wind_offshore_near_shore':"OffshoreWind",
            'wind_offshore':"OffshoreWind",
            'photovoltaics': "PVUtility",
            'rooftop_photovoltaics': "PVRooftop",
            'rooftop_photovoltaics_com': "PVRooftop",
            "solar_thermal": "CSP",
            "run-of-river_hydro": "HydroPowerPlant",
            "reservoir_hydro": "HydroPowerPlant",
            'natural_gas_turbine': "GasPowerPlant(CCGT)",
            'natural_gas_turbine_CCS': "GasPowerPlant(CCGT)",
            'hard_coal_plant': "HardCoalPowerPlant",
            'hard_coal_plant_CCS': "HardCoalPowerPlant",
            'lignite_coal_plant': "LignitePowerPlant",
            'lignite_coal_plant_CCS': "LignitePowerPlant",
            "nuclear": "NuclearPowerPlant",
            'biomass_plant': "BiomassPowerPlant",
            'biomass_plant_CCS': "BiomassPowerPlant",
            'oil_plant': "OilPowerPlant(CCGT)",
        }
        df_renamed = self.rename_index(df, DIW_names)
        df_renamed.index.name = "technology"
        return df_renamed
    
    def get_cost_data(self, technology, variable):
        df_finance = self.raw_data["finance"]
        if variable in df_finance.index.get_level_values("variable"):
            df_tech = df_finance.loc[(technology, variable)].T
            df_tech.index.name = "year"
            df_tech.name = variable
            return df_tech.squeeze()
        else:
            return None
    
    def get_lifetime(self, technology):
        df_lifetime = self.raw_data["lifetime"]
        lt = df_lifetime.loc[technology].squeeze()
        df_lt = pd.Series(index=self.get_years(), data=lt)
        df_lt.index.name = "year"
        df_lt.name = "lifetime"
        return df_lt
    
    def get_efficiency(self, technology):
        df_efficiency = self.raw_data["efficiency"]
        df_tech = df_efficiency.loc[technology]
        df_tech.index.name = "year"
        df_tech.name = "efficiency"
        return df_tech.squeeze()
    
    def get_construction_time(self, technology):
        # DIW does not provide construction time data
        return None