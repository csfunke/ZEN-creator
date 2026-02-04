from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.conversion_technologies.conversion_technology import ConversionTechnology
from zen_creator.utils.attribute import Attribute
from functools import cached_property

class Photovoltaics(ConversionTechnology):
    name = "photovoltaics"
    def __init__(self, model: Model):
        super().__init__(model=model)

    @cached_property
    def lifetime(self) -> Attribute:
        attr = super().lifetime
        lifetime = self.model.techno_economic_parameters.get_lifetime(self.name)
        return attr.set_data(default_value=lifetime, source="")
    
    @cached_property
    def capex_specific_conversion(self) -> Attribute:
        attr = super().capex_specific_conversion
        sic = float(self.model.techno_economic_parameters.get_cost_data(self.name, "capex").loc[self.model.config.time_settings.reference_year])
        return attr.set_data(default_value=sic, unit="Euro/kW", source="")
    
    @cached_property
    def conversion_factor(self) -> Attribute:
        attr = super().conversion_factor
        return attr.set_data(default_value=[], source="")
    
    @cached_property
    def reference_carrier(self) -> Attribute:
        attr = super().reference_carrier
        return self.set_carriers(attr, ["electricity"])
    
    @cached_property
    def input_carrier(self) -> Attribute:
        attr = super().input_carrier
        return self.set_carriers(attr, [])
    
    @cached_property
    def output_carrier(self) -> Attribute:
        attr = super().output_carrier
        return self.set_carriers(attr, ["electricity"])
