from zen_creator.datasets.combined_datasets.combined_datasets_technology_economic_parameters import CombinedDatasetTechnoEconomicParameters
from zen_creator.elements.element import Element
from zen_creator.utils.default_config import Config
from zen_creator.utils.element_collection import ElementCollection
from zen_creator.sectors import Sector
from zen_creator.elements.energy_system import EnergySystem
from zen_creator.datasets.dataset import Dataset

import os 
from pathlib import Path
import shutil

class Model:
    def __init__(self, config: Config):
        self.config = config
        self.model_name = None
        self.out_path = None
        self.source_path = None
        self.energy_system = None
        self.existing_model = None
        self.sectors = []

    def prepare_model(self, model_name: str, out_path: str, source_path: str, existing_model: str = None):
        self.create_paths(model_name, out_path, source_path)
        self.add_existing_model(existing_model,out_path)
        self.create_new_folders()
        self.load_datasets()

    def create_paths(self, model_name: str, out_path: str, source_path: str):
        self.model_name = model_name
        self.out_path = os.path.join(out_path, model_name)
        self.source_path = Path(source_path)
        assert self.source_path.exists(), f"Input path {self.source_path} does not exist."

    def create_new_folders(self):
        if not os.path.exists(self.out_path):
            # create top level folder
            os.makedirs(self.out_path)
            print(f"New folder structure created for {self.model_name}")
        else:
            # clear content of folder
            print(f"Clear folder {self.model_name}")
            for file in os.listdir(self.out_path):
                file_path = os.path.join(self.out_path, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        # create subfolders
        subfolders = ["set_technologies","set_carriers","energy_system"]
        for subfolder in subfolders:
            os.mkdir(f"{self.out_path}/{subfolder}")

    def load_datasets(self):
        self.datasets = {}
        for dataset_class in Dataset.__subclasses__():
            if dataset_class.__subclasses__():
                continue
            dataset_instance = dataset_class(self)
            self.datasets[dataset_instance.name] = dataset_instance
            print(f"Loaded dataset: {dataset_instance.name}")
        
        self.techno_economic_parameters = CombinedDatasetTechnoEconomicParameters(self)
            
    def create_energy_system(self):
        self.energy_system = EnergySystem(self)
    
    def add_sectors(self):
        self.element_collection = ElementCollection()
        for sector_name in self.config.sector_settings.sectors:
            self.add_sector(sector_name)

    def add_sector(self, sector_name: str):
        for sector in Sector.__subclasses__():
            if sector.name == sector_name:
                self.sectors.append(sector(self))
                return
        raise ValueError(f"Sector '{sector_name}' not found.")

    def add_elements(self):
        elements: list[Element] = []
        for element in self.element_collection.element_classes:
            elements.append(element(self))

    def check_completeness(self):
        # check that all carriers of technologies are defined
        for carrier_name in self.element_collection.carriers_of_technologies:
            if carrier_name not in self.element_collection.carriers:
                raise ValueError(f"Carrier '{carrier_name}' used in technologies but not defined in carriers.")
        print("Model completeness check passed.")

    def write_files(self):
        self.energy_system.system_file.save_system_file()
        self.element_collection.write_files()

    def add_existing_model(self, existing_model_name: str, out_path: str):
        existing_model_path = os.path.join(out_path, existing_model_name)
        if not os.path.exists(existing_model_path):
            print(f"Existing model path '{existing_model_path}' does not exist. Skipping import of existing model.")
            return
        self.existing_model = Path(existing_model_name)
        