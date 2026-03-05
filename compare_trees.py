# import difflib
import difflib
import json
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

# ----------------------------
# JSON DEEP DIFF
# ----------------------------


def json_diff(obj1, obj2, path=""):
    diffs = []

    if type(obj1) is not type(obj2):
        diffs.append(f"{path} - Type changed: {type(obj1)} -> {type(obj2)}")
        return diffs

    if isinstance(obj1, dict):
        keys = set(obj1.keys()).union(obj2.keys())
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            if key not in obj1:
                diffs.append(f"{new_path} - Key missing in Tree1")
            elif key not in obj2:
                diffs.append(f"{new_path} - Key missing in Tree2")
            else:
                diffs.extend(json_diff(obj1[key], obj2[key], new_path))

    elif isinstance(obj1, list):
        min_len = min(len(obj1), len(obj2))
        for i in range(min_len):
            diffs.extend(json_diff(obj1[i], obj2[i], f"{path}[{i}]"))
        if len(obj1) > len(obj2):
            diffs.append(f"{path} - Extra items in Tree1")
        elif len(obj2) > len(obj1):
            diffs.append(f"{path} - Extra items in Tree2")

    else:
        if obj1 != obj2:
            diffs.append(f"{path} - Value changed: {obj1} -> {obj2}")

    return diffs


# ----------------------------
# TEXT DIFF
# ----------------------------


def text_diff(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1:
        lines1 = f1.readlines()

    with open(file2, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()

    diff = difflib.unified_diff(
        lines1, lines2, fromfile=str(file1), tofile=str(file2), lineterm=""
    )
    return list(diff)


# ----------------------------
# CSV DIFF
# ----------------------------


def csv_diff(file1: str, file2: str, tol: float = 1e-10) -> List[str]:

    differences: List[str] = []

    # Load CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Check columns
    if not df1.columns.equals(df2.columns):
        differences.append(
            f"Different columns:\n"
            f"File1: {df1.columns.tolist()}\n"
            f"File2: {df2.columns.tolist()}"
        )
        return differences  # Cannot compare further safely

    # Check shape
    if df1.shape != df2.shape:
        differences.append(f"Different shapes: File1 {df1.shape}, File2 {df2.shape}")
        return differences

    # Compare column-by-column
    for col in df1.columns:
        s1 = df1[col]
        s2 = df2[col]

        # Numeric columns → compare with tolerance
        if pd.api.types.is_numeric_dtype(s1):
            comparison = np.isclose(s1, s2, atol=tol, rtol=0, equal_nan=True)
        else:
            comparison = (s1 == s2) | (s1.isna() & s2.isna())

        # Record differences
        diff_indices = np.where(~comparison)[0]
        for idx in diff_indices:
            differences.append(
                f"Row {idx}, Column '{col}': {s1.iloc[idx]} != {s2.iloc[idx]}"
            )

    return differences


# def csv_diff(file1, file2):
#     # Load the CSV files into DataFrames
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)

#     diffs = []

#     # Compare column names
#     if not df1.columns.equals(df2.columns):
#         diffs.append(
#             "The CSV files have different columns. "
#             f"{file1} contains {df1.columns}, whereas"
#             f"{file2} contains {df2.columns}"

#         )

#     # Compare the entire DataFrame
#     if not df1.equals(df2):
#         diff = df1.compare(df2)
#         diffs.append(
#             f"The CSV files have different values. Differences: {diff}"
#         )

#     return diffs


# ----------------------------
# FILE COMPARISON
# ----------------------------


def compare_files(file1, file2):
    ext = file1.suffix.lower()

    if ext == ".json":
        with open(file1, "r", encoding="utf-8") as f1:
            obj1 = json.load(f1)
        with open(file2, "r", encoding="utf-8") as f2:
            obj2 = json.load(f2)

        return json_diff(obj1, obj2)

    if ext == ".csv":
        return csv_diff(file1, file2)

    else:
        # fallback to text diff
        return text_diff(file1, file2)


# ----------------------------
# TREE BUILDING
# ----------------------------


def build_file_map(root):
    root = Path(root)
    file_map = {}
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root)
            file_map[rel] = path
    return file_map


# ----------------------------
# MAIN TREE COMPARISON
# ----------------------------


def compare_trees(dir1, dir2) -> bool:
    map1 = build_file_map(dir1)
    map2 = build_file_map(dir2)

    all_paths = set(map1.keys()).union(map2.keys())

    is_equal = True

    for rel_path in sorted(all_paths):
        f1 = map1.get(rel_path)
        f2 = map2.get(rel_path)

        print(f"\n=== {rel_path} ===")

        if f1 and not f2:
            print("Only in Tree1")
            is_equal = False
        elif f2 and not f1:
            print("Only in Tree2")
            is_equal = False
        else:
            diffs = compare_files(f1, f2)
            if not diffs:
                print("No differences")
            else:
                print("Differences found:")
                for d in diffs:
                    print(d)
                    is_equal = False

    return is_equal


# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    dir1 = (
        "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe"
        "\\03_ZEN_data\\Test\\test_8a"
    )
    dir2 = (
        "C:\\Users\\funkec\\Documents\\GITHUB\\01_Models\\01_ZEN_universe\\"
        "03_ZEN_data\\Test\\test_8a_replica"
    )

    compare_trees(dir1, dir2)
