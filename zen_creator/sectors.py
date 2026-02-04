from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

import zen_creator.elements.carriers as carriers
import zen_creator.elements.technologies.conversion_technologies as conversion_technologies
import zen_creator.elements.technologies.storage_technologies as storage_technologies
import zen_creator.elements.technologies.transport_technologies as transport_technologies


class Sector:
    def __init__(self,model: Model):
        self.model = model

    def add(self,element):
        if element not in self.model.element_collection.element_classes:
            self.model.element_collection.add_class(element)

class Electricity(Sector):
    name = "electricity"
    def __init__(self,model: Model):
        super().__init__(model)
        # carriers
        self.add(carriers.Electricity)
        self.add(carriers.Heat)
        self.add(carriers.Lignite)
        # technologies
        self.add(conversion_technologies.Photovoltaics)
        self.add(conversion_technologies.LigniteCoalPlant)

class Heat(Sector):
    name = "heat"
    def __init__(self,model: Model):
        super().__init__(model)

        # carriers
        self.add(carriers.Heat)
        # technologies
        self.add(conversion_technologies.HeatPump)
        self.add(conversion_technologies.ElectrodeBoiler)
        if model.config.sector_settings.use_district_heating:
            pass

class PassengerTransport(Sector):
    name = "passenger_transport"
    def __init__(self,model: Model):
        super().__init__(model)

class TruckTransport(Sector):
    name = "truck_transport"
    def __init__(self,model: Model):
        super().__init__(model)

class Shipping(Sector):
    name = "shipping"
    def __init__(self,model: Model):
        super().__init__(model)

class Aviation(Sector):
    name = "aviation"
    def __init__(self,model: Model):
        super().__init__(model)

class Refining(Sector):
    name = "refining"
    def __init__(self,model: Model):
        super().__init__(model)

class Hydrogen(Sector):
    name = "hydrogen"
    def __init__(self,model: Model):
        super().__init__(model)

class Methanol(Sector):
    name = "methanol"
    def __init__(self,model: Model):
        super().__init__(model)

class Ammonia(Sector):
    name = "ammonia"
    def __init__(self,model: Model):
        super().__init__(model)

class Carbon(Sector):
    name = "carbon"
    def __init__(self,model: Model):
        super().__init__(model)

class Cement(Sector):
    name = "cement"
    def __init__(self,model: Model):
        super().__init__(model)

class Steel(Sector):
    name = "steel"
    def __init__(self,model: Model):
        super().__init__(model)