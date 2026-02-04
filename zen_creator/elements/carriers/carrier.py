from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute
from functools import cached_property
import numpy as np


class Carrier(Element):
    subpath = 'set_carriers'

    def __init__(self, model: Model, power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)

    # ---------- Default attributes ----------
    @cached_property
    def demand(self) -> Attribute:
        return Attribute('demand', default_value=0.0, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def availability_import(self) -> Attribute:
        return Attribute('availability_import', default_value=0.0, unit=f"{self.power_unit}",element=self)
    
    @cached_property
    def availability_export(self) -> Attribute:
        return Attribute('availability_export', default_value=0.0, unit=f"{self.power_unit}",element=self)    
    
    @cached_property
    def availability_import_yearly(self) -> Attribute:
        return Attribute('availability_import_yearly', default_value=0.0, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def availability_export_yearly(self) -> Attribute:
        return Attribute('availability_export_yearly', default_value=0.0, unit=f"{self.power_unit}*h",element=self)
    
    @cached_property
    def price_import(self) -> Attribute:
        return Attribute('price_import', default_value=0.0, unit=f"Euro/({self.power_unit}*h)",element=self)
    
    @cached_property
    def price_export(self) -> Attribute:
        return Attribute('price_export', default_value=0.0, unit=f"Euro/({self.power_unit}*h)",element=self)
    
    @cached_property
    def carbon_intensity_carrier_import(self) -> Attribute:
        return Attribute('carbon_intensity_carrier_import', default_value=0.0, unit=f"kilotons/({self.power_unit}*h)",element=self)
    
    @cached_property
    def carbon_intensity_carrier_export(self) -> Attribute:
        return Attribute('carbon_intensity_carrier_export', default_value=0.0, unit=f"kilotons/({self.power_unit}*h)",element=self)
    @cached_property
    def price_shed_demand(self) -> Attribute:
        return Attribute('price_shed_demand', default_value=np.inf, unit=f"Euro/({self.power_unit}*h)",element=self)

