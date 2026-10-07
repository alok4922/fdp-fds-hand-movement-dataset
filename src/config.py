"""
Central configuration for the FDP/FDS Hand Movement Dataset Collector.
"""

import os


# ============================================================
# PROJECT PATHS
# ============================================================

# Project root = folder containing src/ and models/
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "hand_landmarker.task",
)


# ============================================================
# DATASET PATHS
# ============================================================

DATA_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
)

RAW_DATA_FOLDER = os.path.join(
    DATA_FOLDER,
    "raw",
)

PROCESSED_DATA_FOLDER = os.path.join(
    DATA_FOLDER,
    "processed",
)

METADATA_FOLDER = os.path.join(
    DATA_FOLDER,
    "metadata",
)

# Kept as an alias for compatibility
DATASET_FOLDER = DATA_FOLDER


# ============================================================
# CAMERA
# ============================================================

CAMERA_INDEX = 1

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

MIRROR_CAMERA = True


# ============================================================
# RECORDING
# ============================================================

RECORDING_SECONDS = 10

COUNTDOWN_SECONDS = 3


# ============================================================
# FINGER LANDMARK INDICES
# ============================================================

FINGERS = {

    "Thumb": (
        1,   # MCP
        2,   # PIP
        3,   # DIP
        4,   # TIP
    ),

    "Index": (
        5,   # MCP
        6,   # PIP
        7,   # DIP
        8,   # TIP
    ),

    "Middle": (
        9,   # MCP
        10,  # PIP
        11,  # DIP
        12,  # TIP
    ),

    "Ring": (
        13,  # MCP
        14,  # PIP
        15,  # DIP
        16,  # TIP
    ),

    "Pinky": (
        17,  # MCP
        18,  # PIP
        19,  # DIP
        20,  # TIP
    ),
}


# ============================================================
# TEST CONFIGURATION
# ============================================================

TESTS = {

    "FDP": {
        "title": "FDP Test",
        "target_joint": "DIP",

        "instructions": [
            "Keep the other fingers straight.",
            "Bend only the selected finger.",
            "Try to touch the palm with the fingertip.",
            "Move slowly and completely.",
        ],
    },

    "FDS": {
        "title": "FDS Test",
        "target_joint": "PIP",

        "instructions": [
            "Keep the other fingers straight.",
            "Bend the selected finger at the PIP joint.",
            "Keep the fingertip as straight as possible.",
            "Move slowly and completely.",
        ],
    },
}


# ============================================================
# COLORS
# ============================================================

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

RED = (0, 0, 255)

GREEN = (0, 255, 0)

BLUE = (255, 0, 0)

YELLOW = (0, 255, 255)

CYAN = (255, 255, 0)

DARK = (30, 30, 30)