from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element

class ElementCollection:
    def __init__(self):
        self.element_classes = []
        self.carriers_of_technologies = []
        
    def add_class(self, element_class):
        self.element_classes.append(element_class)

    def add_elements(self,model: Model):
        for element_class in self.element_classes:
            element_class(model)

    def add_carrier_of_technology(self, carrier_list: list):
        for carrier_name in carrier_list:
            if carrier_name not in self.carriers_of_technologies:   
                self.carriers_of_technologies.append(carrier_name)

    def write_files(self):
        for element in Element.get_all().values():
            element.save_attributes()
            element.save_data()