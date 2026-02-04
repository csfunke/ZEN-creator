from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute

from abc import ABC, abstractmethod
from functools import cached_property
import numpy as np

class Technology(Element,ABC):
    subpath = 'set_technologies'

    def __init__(self, model: Model, power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)


    # ---------- Attributes with default values ----------
    @cached_property
    def capacity_addition_min(self) -> Attribute:
        return Attribute('capacity_addition_min', default_value=0.0, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def capacity_addition_max(self) -> Attribute:
        return Attribute('capacity_addition_max', default_value=np.inf, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def capacity_addition_unbounded(self) -> Attribute:
        return Attribute('capacity_addition_unbounded', default_value=0.0, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def capacity_existing(self) -> Attribute:
        return Attribute('capacity_existing', default_value=0.0, unit=f"{self.power_unit}",element=self)
    @cached_property
    def capacity_limit(self) -> Attribute:
        return Attribute('capacity_limit', default_value=np.inf, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def min_load(self) -> Attribute:
        return Attribute('min_load', default_value=0.0, unit="1",element=self)
    
    @cached_property
    def max_load(self) -> Attribute:
        return Attribute('max_load', default_value=1.0, unit="1",element=self)

    @cached_property
    def opex_specific_variable(self) -> Attribute:
        return Attribute('opex_specific_variable', default_value=0.0, unit=f"Euro/({self.power_unit}*h)",element=self)
    
    @cached_property
    def opex_specific_fixed(self) -> Attribute:
        return Attribute('opex_specific_fixed', default_value=0.0, unit=f"Euro/({self.power_unit})",element=self)
    
    @cached_property
    def carbon_intensity_technology(self) -> Attribute:
        return Attribute('carbon_intensity_technology', default_value=0.0, unit=f"kilotons/({self.power_unit}*h)",element=self)
    
    @cached_property
    def construction_time(self) -> Attribute:
        return Attribute('construction_time', default_value=0, unit="1",element=self)
    
    @cached_property
    def capacity_investment_existing(self) -> Attribute:
        return Attribute('capacity_investment_existing', default_value=0.0, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def max_diffusion_rate(self) -> Attribute:
        return Attribute('max_diffusion_rate', default_value=np.inf, unit="1",element=self)

    # ---------- Mandatory attributes to be filled for each technology ----------
    @property
    @abstractmethod 
    def lifetime(self) -> Attribute:
        return Attribute('lifetime', unit="1",element=self)
    
    @property
    @abstractmethod
    def reference_carrier(self) -> Attribute:
        return Attribute('reference_carrier', element=self)
    
    def set_carriers(self,carrier_attr: Attribute, carrier_list: list) -> Attribute:
        self.model.element_collection.add_carrier_of_technology(carrier_list)
        return carrier_attr.set_data(default_value=carrier_list)

    