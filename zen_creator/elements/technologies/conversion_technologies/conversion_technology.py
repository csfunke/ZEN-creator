from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.technology import Technology
from zen_creator.utils.attribute import Attribute

from abc import ABC, abstractmethod
from functools import cached_property
import numpy as np

class ConversionTechnology(Technology,ABC):
    subpath = 'set_conversion_technologies'

    def __init__(self, model: Model,power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)

    # ---------- Attributes with default values ----------   
    @cached_property
    def capex_specific_conversion(self) -> Attribute:
        return Attribute('capex_specific_conversion', default_value=0.0, unit=f"Euro/({self.power_unit})",element=self)

    # ---------- Mandatory attributes to be filled for each technology ----------
    @property
    @abstractmethod 
    def input_carrier(self) -> Attribute:
        return Attribute('input_carrier',element=self)
    
    @property
    @abstractmethod
    def output_carrier(self) -> Attribute:
        return Attribute('output_carrier',element=self)
    
    @property
    @abstractmethod 
    def conversion_factor(self) -> Attribute:
        return Attribute('conversion_factor',element=self)
    


    