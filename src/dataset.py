"""
Dataset management.

Handles:
- Dataset folder creation
- FDP/FDS folder selection
- CSV filename generation
- Saving frame-level recordings
- Calculating ROM
- Saving test summaries
"""

import csv
import os
from datetime import datetime

from config import (
    RAW_DATA_FOLDER,
    PROCESSED_DATA_FOLDER,
    METADATA_FOLDER,
)


# ============================================================
# CREATE DATASET FOLDERS
# ============================================================

def create_dataset_folders():
    """
    Create the complete dataset structure.
    """

    folders = [
        RAW_DATA_FOLDER,
        PROCESSED_DATA_FOLDER,
        METADATA_FOLDER,

        os.path.join(
            RAW_DATA_FOLDER,
            "FDP",
        ),

        os.path.join(
            RAW_DATA_FOLDER,
            "FDS",
        ),
    ]

    for folder in folders:

        os.makedirs(
            folder,
            exist_ok=True,
        )


# ============================================================
# GET TEST FOLDER
# ============================================================

def get_test_folder(test_type):
    """
    Return the folder for FDP or FDS recordings.
    """

    if test_type not in ("FDP", "FDS"):
        raise ValueError(
            f"Unknown test type: {test_type}"
        )

    folder = os.path.join(
        RAW_DATA_FOLDER,
        test_type,
    )

    os.makedirs(
        folder,
        exist_ok=True,
    )

    return folder


# ============================================================
# CALCULATE ROM
# ============================================================

def calculate_rom(rows):
    """
    Calculate complete-test ROM values.

    ROM = maximum angle - minimum angle
    """

    if not rows:
        return None

    mcp_values = [
        float(row[6])
        for row in rows
    ]

    pip_values = [
        float(row[7])
        for row in rows
    ]

    dip_values = [
        float(row[8])
        for row in rows
    ]

    mcp_min = round(
        min(mcp_values),
        2,
    )

    mcp_max = round(
        max(mcp_values),
        2,
    )

    pip_min = round(
        min(pip_values),
        2,
    )

    pip_max = round(
        max(pip_values),
        2,
    )

    dip_min = round(
        min(dip_values),
        2,
    )

    dip_max = round(
        max(dip_values),
        2,
    )

    return {
        "mcp_min": mcp_min,
        "mcp_max": mcp_max,
        "mcp_rom": round(
            mcp_max - mcp_min,
            2,
        ),

        "pip_min": pip_min,
        "pip_max": pip_max,
        "pip_rom": round(
            pip_max - pip_min,
            2,
        ),

        "dip_min": dip_min,
        "dip_max": dip_max,
        "dip_rom": round(
            dip_max - dip_min,
            2,
        ),
    }


# ============================================================
# SAVE RECORDING
# ============================================================

def save_recording(
    filename,
    rows,
):
    """
    Save frame-by-frame recording to CSV.

    ROM values are added to every frame row.
    """

    if not rows:

        print(
            "\nNothing to save."
        )

        return False

    rom = calculate_rom(
        rows
    )

    rom_values = [
        rom["mcp_min"],
        rom["mcp_max"],
        rom["mcp_rom"],

        rom["pip_min"],
        rom["pip_max"],
        rom["pip_rom"],

        rom["dip_min"],
        rom["dip_max"],
        rom["dip_rom"],
    ]

    # --------------------------------------------------------
    # CSV headers
    # --------------------------------------------------------

    headers = [
        "timestamp",
        "frame_number",
        "subject_id",
        "finger",
        "test_type",
        "label",

        "mcp_angle",
        "pip_angle",
        "dip_angle",

        "tip_mcp_distance",
        "tip_pip_distance",
        "tip_wrist_distance",

        "mcp_min",
        "mcp_max",
        "mcp_rom",

        "pip_min",
        "pip_max",
        "pip_rom",

        "dip_min",
        "dip_max",
        "dip_rom",
    ]

    # --------------------------------------------------------
    # Add 21 MediaPipe landmarks
    # --------------------------------------------------------

    for i in range(21):

        headers.extend([
            f"landmark_{i}_x",
            f"landmark_{i}_y",
            f"landmark_{i}_z",
        ])

    # --------------------------------------------------------
    # Make sure folder exists
    # --------------------------------------------------------

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Write CSV
    # --------------------------------------------------------

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            headers
        )

        for row in rows:

            writer.writerow(
                row[:12]
                + rom_values
                + row[12:]
            )

    # --------------------------------------------------------
    # Display ROM
    # --------------------------------------------------------

    print(
        f"\nMCP: min={rom['mcp_min']} "
        f"max={rom['mcp_max']} "
        f"ROM={rom['mcp_rom']} deg"
    )

    print(
        f"PIP: min={rom['pip_min']} "
        f"max={rom['pip_max']} "
        f"ROM={rom['pip_rom']} deg"
    )

    print(
        f"DIP: min={rom['dip_min']} "
        f"max={rom['dip_max']} "
        f"ROM={rom['dip_rom']} deg"
    )

    print(
        "\n================================"
    )

    print(
        "DATA SAVED SUCCESSFULLY"
    )

    print(
        "================================"
    )

    print(
        f"Frames: {len(rows)}"
    )

    print(
        f"File: {filename}"
    )

    return True


# ============================================================
# SAVE TEST SUMMARY
# ============================================================

def save_test_summary(
    subject_id,
    finger,
    test_type,
    label,
    pain,
    rows,
):
    """
    Save one row describing the complete test.
    """

    if not rows:
        return False

    rom = calculate_rom(
        rows
    )

    summary_folder = (
        METADATA_FOLDER
    )

    os.makedirs(
        summary_folder,
        exist_ok=True,
    )

    summary_file = os.path.join(
        summary_folder,
        "test_summary.csv",
    )

    headers = [
        "timestamp",
        "subject_id",
        "finger",
        "test_type",
        "label",
        "pain_0_10",
        "frames_recorded",

        "mcp_min",
        "mcp_max",
        "mcp_rom",

        "pip_min",
        "pip_max",
        "pip_rom",

        "dip_min",
        "dip_max",
        "dip_rom",
    ]

    file_exists = os.path.exists(
        summary_file
    )

    with open(
        summary_file,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        if not file_exists:

            writer.writerow(
                headers
            )

        writer.writerow([
            datetime.now().isoformat(),

            subject_id,
            finger,
            test_type,
            label,
            pain,

            len(rows),

            rom["mcp_min"],
            rom["mcp_max"],
            rom["mcp_rom"],

            rom["pip_min"],
            rom["pip_max"],
            rom["pip_rom"],

            rom["dip_min"],
            rom["dip_max"],
            rom["dip_rom"],
        ])

    return True