"""Test for creating models from config using custom element classes.

Element classes are imported locally within the test function to avoid
registering them globally, which would cause contamination of other tests.
"""

from __future__ import annotations

import importlib
from pathlib import Path

from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_trees
from zen_creator.utils.default_config import Config

FIXTURE_ROOT = Path(__file__).parent / "fixtures"
EXISTING_MODEL_PATH = FIXTURE_ROOT / "existing_model"
CONFIG_PATH = FIXTURE_ROOT / "config_existing_model.yaml"
OUTPUT_FOLDER = Path(".//tests//end_to_end//outputs")


def test_from_config():
    """Recreate the existing_model fixture tree from config and explicit classes.

    Note: Element classes are imported locally to prevent global registry
    contamination when this test runs alongside other tests.
    """
    # Import element classes locally to prevent registry contamination
    # from tests.end_to_end.existing_model_elements import (
    #     ExistingModelEnergySystem,
    #     ElectricityCarrier,
    #     HeatCarrier,
    #     NaturalGasCarrier,
    #     NaturalGasBoiler,
    #     Photovoltaics,
    #     NaturalGasStorage,
    #     PumpedHydro,
    #     NaturalGasPipeline,
    # )
    importlib.import_module("tests.end_to_end.fixtures.existing_model_elements")

    config = Config.load_from_yaml(CONFIG_PATH)
    config.source_path = str(EXISTING_MODEL_PATH)
    config.elements.insert.energy_system = "energy_system"

    model = Model.from_config(config)
    model.output_folder = OUTPUT_FOLDER
    model.name = "test_from_config_existing_model_replica"
    model.build()
    model.write()

    compare_trees(EXISTING_MODEL_PATH, model.output_path, raise_error=True)
