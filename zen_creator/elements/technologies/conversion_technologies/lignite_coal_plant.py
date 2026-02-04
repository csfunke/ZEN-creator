from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.conversion_technologies.conversion_technology import ConversionTechnology
from zen_creator.utils.attribute import Attribute
from functools import cached_property

class LigniteCoalPlant(ConversionTechnology):
    name = "lignite_coal_plant"
    def __init__(self, model: Model):
        super().__init__(model=model)

    @cached_property
    def lifetime(self) -> Attribute:
        attr = super().lifetime
        lifetime = 46
        return attr.set_data(default_value=lifetime, source="https://www.nature.com/articles/s41467-019-12618-3")
    
    @cached_property
    def capex_specific_conversion(self) -> Attribute:
        attr = super().capex_specific_conversion
        capex = self.model.techno_economic_parameters.get_cost_data(self.name, "capex").loc[self.model.config.time_settings.reference_year]
        return attr.set_data(default_value=capex, unit="Euro/kW", source="multiple sources")
    
    @cached_property
    def conversion_factor(self) -> Attribute:
        attr = super().conversion_factor
        conversion_factor = 1/self.model.techno_economic_parameters.get_efficiency(self.name)
        return attr.set_data(default_value=[{"lignite": {"default_value": conversion_factor,"unit":"GWh/GWh"}}], source="multiple sources")
    
    @cached_property
    def reference_carrier(self) -> Attribute:
        attr = super().reference_carrier
        return self.set_carriers(attr, ["electricity"])
    
    @cached_property
    def input_carrier(self) -> Attribute:
        attr = super().input_carrier
        return self.set_carriers(attr, ["lignite"]) 
    
    @cached_property
    def output_carrier(self) -> Attribute:
        attr = super().output_carrier
        return self.set_carriers(attr, ["electricity"])


