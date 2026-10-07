"""
Feature extraction for hand movement analysis.

Contains:
- Joint angle calculation
- Landmark distance calculation
- MCP/PIP/DIP angle extraction
"""


import math
import numpy as np

from config import FINGERS


# ============================================================
# JOINT ANGLE
# ============================================================

def calculate_angle(a, b, c):
    """
    Calculate angle ABC.

    Parameters
    ----------
    a : list or tuple
        First point (x, y, z)

    b : list or tuple
        Joint point (x, y, z)

    c : list or tuple
        Third point (x, y, z)

    Returns
    -------
    float
        Joint angle in degrees.

    Notes
    -----
    A straight joint is approximately 180 degrees.
    More bending produces a smaller included angle.
    """

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    ba = a - b
    bc = c - b

    denominator = (
        np.linalg.norm(ba) *
        np.linalg.norm(bc)
    )

    if denominator < 1e-8:
        return 0.0

    cosine = np.dot(ba, bc) / denominator

    cosine = np.clip(
        cosine,
        -1.0,
        1.0
    )

    return round(
        float(
            np.degrees(
                np.arccos(cosine)
            )
        ),
        2
    )


# ============================================================
# DISTANCE
# ============================================================

def calculate_distance(a, b):
    """
    Calculate Euclidean distance between two
    3D MediaPipe landmarks.
    """

    return round(
        float(
            np.linalg.norm(
                np.array(a) -
                np.array(b)
            )
        ),
        4
    )


# ============================================================
# GET JOINT ANGLES AND DISTANCES
# ============================================================

def get_angles(landmarks, finger_name):
    """
    Calculate MCP, PIP and DIP angles and
    selected landmark distances.

    Parameters
    ----------
    landmarks
        MediaPipe hand landmarks.

    finger_name : str
        Finger being tested.

    Returns
    -------
    dict
        Extracted movement features.
    """

    mcp_i, pip_i, dip_i, tip_i = FINGERS[
        finger_name
    ]

    # --------------------------------------------------------
    # Get landmarks
    # --------------------------------------------------------

    wrist = landmarks[0]
    mcp = landmarks[mcp_i]
    pip = landmarks[pip_i]
    dip = landmarks[dip_i]
    tip = landmarks[tip_i]

    # --------------------------------------------------------
    # Convert landmarks to XYZ coordinates
    # --------------------------------------------------------

    wrist_xyz = [
        wrist.x,
        wrist.y,
        wrist.z
    ]

    mcp_xyz = [
        mcp.x,
        mcp.y,
        mcp.z
    ]

    pip_xyz = [
        pip.x,
        pip.y,
        pip.z
    ]

    dip_xyz = [
        dip.x,
        dip.y,
        dip.z
    ]

    tip_xyz = [
        tip.x,
        tip.y,
        tip.z
    ]

    # --------------------------------------------------------
    # Calculate features
    # --------------------------------------------------------

    return {

        "mcp_angle": calculate_angle(
            wrist_xyz,
            mcp_xyz,
            pip_xyz
        ),

        "pip_angle": calculate_angle(
            mcp_xyz,
            pip_xyz,
            dip_xyz
        ),

        "dip_angle": calculate_angle(
            pip_xyz,
            dip_xyz,
            tip_xyz
        ),

        "tip_mcp_distance": calculate_distance(
            tip_xyz,
            mcp_xyz
        ),

        "tip_pip_distance": calculate_distance(
            tip_xyz,
            pip_xyz
        ),

        "tip_wrist_distance": calculate_distance(
            tip_xyz,
            wrist_xyz
        )
    }