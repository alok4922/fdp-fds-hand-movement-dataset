"""
Visualization utilities.

Handles:
- Drawing text
- Drawing hand landmarks
- Highlighting the selected finger
- Highlighting the target joint for FDP/FDS tests
"""

import cv2

from config import (
    GREEN,
    RED,
    BLUE,
    YELLOW,
    WHITE,
    FINGERS,
)


# ============================================================
# TEXT
# ============================================================

def put_text(
    frame,
    text,
    x,
    y,
    size=0.55,
    color=WHITE,
    thickness=1,
):
    """
    Draw readable text on the webcam frame.
    """

    cv2.putText(
        frame,
        str(text),
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        color,
        thickness,
        cv2.LINE_AA,
    )


# ============================================================
# DRAW HAND
# ============================================================

def draw_hand(
    frame,
    landmarks,
):
    """
    Draw all 21 MediaPipe hand landmarks.
    """

    h, w = frame.shape[:2]

    connections = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),

        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),

        (5, 9),
        (9, 10),
        (10, 11),
        (11, 12),

        (9, 13),
        (13, 14),
        (14, 15),
        (15, 16),

        (13, 17),
        (17, 18),
        (18, 19),
        (19, 20),

        (0, 17),
    ]

    # --------------------------------------------------------
    # Draw bones
    # --------------------------------------------------------

    for a, b in connections:

        p1 = (
            int(landmarks[a].x * w),
            int(landmarks[a].y * h),
        )

        p2 = (
            int(landmarks[b].x * w),
            int(landmarks[b].y * h),
        )

        cv2.line(
            frame,
            p1,
            p2,
            BLUE,
            2,
        )

    # --------------------------------------------------------
    # Draw joints
    # --------------------------------------------------------

    for landmark in landmarks:

        point = (
            int(landmark.x * w),
            int(landmark.y * h),
        )

        cv2.circle(
            frame,
            point,
            4,
            GREEN,
            -1,
        )


# ============================================================
# HIGHLIGHT SELECTED FINGER
# ============================================================

def highlight_finger(
    frame,
    landmarks,
    finger_name,
    test_type,
):
    """
    Highlight the finger being tested.

    FDP:
        DIP joint is highlighted yellow.

    FDS:
        PIP joint is highlighted yellow.
    """

    h, w = frame.shape[:2]

    mcp_i, pip_i, dip_i, tip_i = FINGERS[
        finger_name
    ]

    indices = [
        0,
        mcp_i,
        pip_i,
        dip_i,
        tip_i,
    ]

    points = []

    for index in indices:

        point = (
            int(landmarks[index].x * w),
            int(landmarks[index].y * h),
        )

        points.append(point)

    # --------------------------------------------------------
    # Highlight finger bones
    # --------------------------------------------------------

    for a, b in zip(
        points[:-1],
        points[1:],
    ):

        cv2.line(
            frame,
            a,
            b,
            GREEN,
            5,
        )

    # --------------------------------------------------------
    # Highlight joints
    # --------------------------------------------------------

    for i, point in zip(
        indices,
        points,
    ):

        if (
            test_type == "FDP"
            and i == dip_i
        ):
            color = YELLOW

        elif (
            test_type == "FDS"
            and i == pip_i
        ):
            color = YELLOW

        elif i == tip_i:
            color = RED

        else:
            color = BLUE

        cv2.circle(
            frame,
            point,
            9,
            color,
            -1,
        )

        cv2.circle(
            frame,
            point,
            10,
            WHITE,
            1,
        )