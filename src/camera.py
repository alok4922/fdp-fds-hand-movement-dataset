"""
Camera utilities.

Handles:
- Opening the laptop webcam
- Camera fallback
- Resolution configuration
"""

import cv2

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)


# ============================================================
# OPEN WEBCAM
# ============================================================

def open_webcam():
    """
    Open the laptop webcam.

    Attempts:
        1. Configured camera using DirectShow
        2. Alternate camera index using DirectShow
        3. Configured camera using default OpenCV backend

    Returns
    -------
    cv2.VideoCapture
        Open webcam object.

    Raises
    ------
    RuntimeError
        If no webcam can be opened.
    """

    print(
        "\nOpening laptop webcam..."
    )

    # --------------------------------------------------------
    # Attempt 1
    # --------------------------------------------------------

    print(
        f"Trying camera index "
        f"{CAMERA_INDEX}..."
    )

    cap = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW,
    )

    if cap.isOpened():

        print(
            f"Webcam opened at "
            f"index {CAMERA_INDEX}."
        )

        configure_camera(
            cap
        )

        return cap

    cap.release()

    # --------------------------------------------------------
    # Attempt 2 - alternate index
    # --------------------------------------------------------

    fallback_index = (
        0
        if CAMERA_INDEX == 1
        else 1
    )

    print(
        f"Camera {CAMERA_INDEX} failed."
    )

    print(
        f"Trying camera index "
        f"{fallback_index}..."
    )

    cap = cv2.VideoCapture(
        fallback_index,
        cv2.CAP_DSHOW,
    )

    if cap.isOpened():

        print(
            f"Webcam opened at "
            f"index {fallback_index}."
        )

        configure_camera(
            cap
        )

        return cap

    cap.release()

    # --------------------------------------------------------
    # Attempt 3 - default backend
    # --------------------------------------------------------

    print(
        "DirectShow failed."
    )

    print(
        "Trying default OpenCV "
        "camera backend..."
    )

    cap = cv2.VideoCapture(
        CAMERA_INDEX
    )

    if cap.isOpened():

        print(
            f"Webcam opened at "
            f"index {CAMERA_INDEX}."
        )

        configure_camera(
            cap
        )

        return cap

    cap.release()

    raise RuntimeError(
        "Could not open any webcam."
    )


# ============================================================
# CONFIGURE CAMERA
# ============================================================

def configure_camera(cap):
    """
    Configure webcam resolution.
    """

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH,
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT,
    )