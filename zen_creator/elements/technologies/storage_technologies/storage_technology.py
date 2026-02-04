from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute
from functools import cached_property
from abc import abstractmethod, ABC
import numpy as np

class StorageTechnology(Element, ABC):
    subpath = 'set_storage_technologies'

    def __init__(self, model: Model, power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)

    # ---------- Attributes with default values ----------   
    @cached_property
    def efficiency_charge(self) -> Attribute:
        return Attribute('efficiency_charge', default_value=1.0, unit="1",element=self)
    
    @cached_property
    def efficiency_discharge(self) -> Attribute:
        return Attribute('efficiency_discharge', default_value=1.0, unit="1",element=self)
    
    @cached_property
    def self_discharge(self) -> Attribute:
        return Attribute('self_discharge', default_value=0.0, unit="1",element=self)
    
    @cached_property
    def capex_specific_storage(self) -> Attribute:
        return Attribute('capex_specific_storage', default_value=0.0, unit=f"Euro/({self.power_unit})",element=self)
    
    @cached_property
    def capex_specific_storage_energy(self) -> Attribute:
        return Attribute('capex_specific_storage_energy', default_value=0.0, unit=f"Euro/({self.power_unit}*h)",element=self)
    
    @cached_property
    def capacity_addition_min_energy(self) -> Attribute:
        return Attribute('capacity_addition_min_energy', default_value=0.0, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def capacity_addition_max_energy(self) -> Attribute:
        return Attribute('capacity_addition_max_energy', default_value=np.inf, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def capacity_existing_energy(self) -> Attribute:
        return Attribute('capacity_existing_energy', default_value=0.0, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def capacity_limit_energy(self) -> Attribute:
        return Attribute('capacity_limit_energy', default_value=np.inf, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def min_load_energy(self) -> Attribute:
        return Attribute('min_load_energy', default_value=0.0, unit="1",element=self)
    
    @cached_property
    def max_load_energy(self) -> Attribute:
        return Attribute('max_load_energy', default_value=1.0, unit="1",element=self)
    
    @cached_property
    def capacity_investment_existing_energy(self) -> Attribute:
        return Attribute('capacity_investment_existing_energy', default_value=0.0, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def opex_specific_fixed_energy(self) -> Attribute:
        return Attribute('opex_specific_fixed_energy', default_value=0.0, unit=f"Euro/({self.power_unit}*h)",element=self)
    
    @cached_property
    def energy_to_power_ratio_min(self) -> Attribute:
        return Attribute('energy_to_power_ratio_min', default_value=0.0, unit="h",element=self)
    
    @cached_property
    def energy_to_power_ratio_max(self) -> Attribute:
        return Attribute('energy_to_power_ratio_max', default_value=np.inf, unit="h",element=self)
    
    @cached_property
    def flow_storage_inflow(self) -> Attribute:
        return Attribute('flow_storage_inflow', default_value=0.0, unit=f"{self.power_unit}",element=self)
    