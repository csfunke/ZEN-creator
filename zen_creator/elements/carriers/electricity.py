from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.carriers.carrier import Carrier
from zen_creator.utils.attribute import Attribute
from functools import cached_property

class Electricity(Carrier):
    name = "electricity"
    def __init__(self, model: Model):
        super().__init__(model=model)

    @cached_property
    def demand(self) -> Attribute:
        attr = super().demand
        demand = self.model.datasets["combined_datasets_electricity"].get_demand()
        return attr.set_data(df=demand,unit="GW", source="ENTSOE Transparency Platform")
    
        
        