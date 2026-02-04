from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

import os
import json
import inspect
from functools import cached_property
from pathlib import Path

class Element:
    name = None
    _instances = set()
    subpath: str = ""

    def __init__(self, model: Model,power_unit:str = "MW"):
        self.model = model
        self.config = model.config
        self.power_unit = power_unit
        self.folder_path = self.set_path()
        self.source_path = model.source_path
        Element.add_element(self)

    def set_path(self):
        mro = self.__class__.mro()
        path = Path(self.name)
        for _cls in mro:
            if hasattr(_cls, 'subpath') and _cls is not self.__class__:
                path = os.path.join(_cls.subpath, path)
        full_path = Path(os.path.join(self.model.out_path, path))
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    def attributes_to_dict(self) -> dict:
        output = {}
        for attr_name in inspect.getmembers(self.__class__, lambda a: isinstance(a, cached_property)):
            attr = getattr(self, attr_name[0])
            output[attr_name[0]] = attr.default_to_dict()
        return output
    
    def save_attributes(self):
        print(f"Saving 'attributes.json' for element '{self.name}' ...")
        output = self.attributes_to_dict()
        with open(os.path.join(self.folder_path, 'attributes.json'), 'w') as f:
            json.dump(output, f, indent=4)
    
    def save_data(self):
        for attr_name in inspect.getmembers(self.__class__, lambda a: isinstance(a, cached_property)):
            attr = getattr(self, attr_name[0])
            attr.save_data(self.folder_path,self.name)

    @classmethod
    def add_element(cls, element: Element):
        Element._instances.add(element)

    @classmethod
    def get_all(cls) -> dict[str, Element]:
        return {e.name: e for e in Element._instances if isinstance(e, cls)}
    
    @classmethod
    def get_by_name(cls, name: str) -> Element | None:
        for element in Element._instances:
            if isinstance(element, cls) and element.name == name:
                return element
        return None
