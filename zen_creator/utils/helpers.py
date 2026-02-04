import os
import numpy as np
import pandas as pd

def get_relative_path(element) -> str:
    """Get the relative path of a folder path."""
    assert hasattr(element, 'folder_path'), f"Element {element} has no attribute 'folder_path'."
    folder_path = element.folder_path
    assert hasattr(element, 'model'), f"Element {element} has no attribute 'model'."
    model = element.model
    assert hasattr(model, 'out_path'), f"Model {model} has no attribute 'out_path'."
    return os.path.relpath(folder_path, start=model.out_path)

def get_partial_index(idx, inv_map: dict) -> pd.Index:
    """Get a partial index based on an inverse mapping."""
    if idx in inv_map:
        return inv_map[idx]
    if isinstance(next(iter(inv_map.keys())), str):
        return np.nan
    for key in inv_map.keys():
        if all([idx[i] == key[i] for i in range(len(key))]):
            return inv_map[key]