from zen_creator.utils.default_config import Config, load_config
from zen_creator.model import Model
import os 


if __name__ == "__main__":
    source_path = "C:\\Users\\jmannhardt\\Desktop\\02-ZEN\\ZEN-creator\\raw_data" # TODO make configurable
    existing_model = "Crystal_Ball"
    out_path = os.getcwd()  # or any other desired path
    model_configs = load_config(os.path.join(source_path, "config.yaml")) # TODO overwrite default config with user inputs
    models = {}
    for model_name, config in model_configs.items():
        model = Model(config)
        model.add_sectors()
        
        model.prepare_model(model_name, out_path, source_path, existing_model=existing_model)
        model.create_energy_system()
        model.add_elements()
        
        
        model.check_completeness()
        model.write_files()
        models[model_name] = model