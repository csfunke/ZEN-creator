from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field


class UnitDefinition(BaseModel):
    dimension: str
    aliases: List[str] = Field(default_factory=list)


class UnitsConfig(BaseModel):
    units: List[str] = Field(default_factory=list)
    definitions: Dict[str, UnitDefinition] = Field(default_factory=dict)

    def overwrite_from_existing_model(self, existing_model_path: Path):

        raise NotImplementedError()

    def get_base_units(self) -> Dict[str, list]:
        """
        Create dictionary for the `base_units.json` file.
        """
        return {"unit": self.units}

    def get_unit_definitions(self) -> str:
        """
        Create text for the `unit_definitions.txt` file.
        """
        txt = []
        for unit, definition in self.definitions.items():
            # Format the unit definition
            aliases_str = " = ".join(definition.aliases)
            line = f"{unit} = [{definition.dimension}] = {aliases_str}"
            txt.append(line)

        return "\n".join(txt)

    # Hard-coded defaults for this section


#     DEFAULT_UNITS = [
#         "hour", "GW", "km", "megatons", "megaEuro",
#         "kilotCO2eq", "megapkm", "megatkm", "ktonproduct",
#     ]
#     DEFAULT_EQUIVALENCES = [
#         "Euro = [currency] = EURO = Eur",
#         "tCO2eq = [massCO2eq] = tonCO2eq = tCO2 = tonne_carbon",
#         "pkm = [mileage] = passenger_km = passenger_kilometer",
#         "tkm = [tonne_mileage] = tonne_km = tonne_kilometer",
#         "tonproduct = [mass_product] = tproduct = tonne_product",
#     ]

#     @classmethod
#     def from_defaults(cls):
#         units_dict = {}
#         for line in cls.DEFAULT_EQUIVALENCES:
#             parts = [p.strip() for p in line.split("=")]
#             canonical = parts[0]
#             unit_type = parts[1].strip("[]")
#             aliases = parts[2:]
#             for name in [canonical] + aliases:
#                 units_dict[name] = UnitDefinition(
#                     canonical=canonical,
#                     type=unit_type,
#                     aliases=aliases
#                 )
#         for u in cls.DEFAULT_UNITS:
#             if u not in units_dict:
#                 units_dict[u] = UnitDefinition(canonical=u, type=None, aliases=[])
#         return cls(units=units_dict)

# class AppConfig(BaseModel):
#     # Other config sections
#     app_name: str = "MyApp"
#     debug: bool = False
#     database_url: str = "sqlite:///default.db"

#     # Units section
#     units: UnitRegistry = UnitRegistry.from_defaults()

#     @classmethod
#     def load(cls, config_file: Optional[str] = None):
#         import yaml
#         from pathlib import Path
#         if config_file and Path(config_file).exists():
#             with open(config_file) as f:
#                 data = yaml.safe_load(f)
#             return cls(**data)
#         # fallback to defaults
#         return cls()
