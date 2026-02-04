from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute
from functools import cached_property
import numpy as np

class TransportTechnology(Element):
    subpath = 'set_transport_technologies'

    def __init__(self, model: Model, power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)

    # ---------- Attributes with default values ----------   
    @cached_property
    def transport_loss_factor_linear(self) -> Attribute:
        return Attribute('transport_loss_factor_linear', default_value=0, unit="1/km",element=self)
    
    @cached_property
    def capex_per_distance_transport(self) -> Attribute:
        return Attribute('capex_per_distance_transport', default_value=0.0, unit=f"Euro/({self.power_unit})/km",element=self)
    
    @cached_property
    def distance(self) -> Attribute:
        return Attribute('distance', default_value=np.inf, unit="km",element=self)
