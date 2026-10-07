"""
MediaPipe hand tracking module.

Handles:
- Creating the MediaPipe Hand Landmarker
- Processing webcam frames
- Detecting hand landmarks
"""

import os

import cv2
import mediapipe as mp

from config import MODEL_PATH


# ============================================================
# CREATE MEDIAPIPE HAND LANDMARKER
# ============================================================

def create_landmarker():
    """
    Create and configure the MediaPipe Hand Landmarker.

    Returns
    -------
    HandLandmarker
        Configured MediaPipe hand landmarker instance.

    Raises
    ------
    FileNotFoundError
        If the MediaPipe model file cannot be found.
    """

    # --------------------------------------------------------
    # Check that the model exists
    # --------------------------------------------------------

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"\nMediaPipe model was not found:\n"
            f"{MODEL_PATH}\n\n"
            f"Make sure hand_landmarker.task is inside "
            f"the models/ folder."
        )

    # --------------------------------------------------------
    # Configure MediaPipe
    # --------------------------------------------------------

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=MODEL_PATH
        ),

        running_mode=(
            mp.tasks.vision.RunningMode.VIDEO
        ),

        num_hands=1,

        min_hand_detection_confidence=0.5,

        min_hand_presence_confidence=0.5,

        min_tracking_confidence=0.5
    )

    # --------------------------------------------------------
    # Create landmarker
    # --------------------------------------------------------

    return (
        mp.tasks.vision.HandLandmarker
        .create_from_options(options)
    )


# ============================================================
# DETECT HAND
# ============================================================

# ============================================================
# TIMESTAMP STATE
# ============================================================

_last_timestamp_ms = -1


# ============================================================
# HAND DETECTION
# ============================================================

def detect_hand(
    landmarker,
    frame,
    timestamp_ms
):
    """
    Detect hand landmarks in a webcam frame.

    Parameters
    ----------
    landmarker
        MediaPipe Hand Landmarker instance.

    frame
        OpenCV BGR image.

    timestamp_ms : int
        Timestamp required by MediaPipe VIDEO mode.

    Returns
    -------
    result
        MediaPipe hand detection result.
    """

    global _last_timestamp_ms

    # --------------------------------------------------------
    # Guarantee monotonically increasing timestamps
    # --------------------------------------------------------

    if timestamp_ms <= _last_timestamp_ms:
        timestamp_ms = _last_timestamp_ms + 1

    _last_timestamp_ms = timestamp_ms

    # --------------------------------------------------------
    # OpenCV uses BGR.
    # MediaPipe expects RGB.
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # --------------------------------------------------------
    # Convert OpenCV image to MediaPipe image
    # --------------------------------------------------------

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    # --------------------------------------------------------
    # Run MediaPipe detection
    # --------------------------------------------------------

    return landmarker.detect_for_video(
        image,
        timestamp_ms
    )