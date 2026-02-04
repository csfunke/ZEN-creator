from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.conversion_technologies.conversion_technology import ConversionTechnology
    
class RetrofittingTechnology(ConversionTechnology):
    subpath = 'set_retrofitting_technologies'

    def __init__(self, model: Model,power_unit:str = "MW"):
        super().__init__(model, power_unit=power_unit)