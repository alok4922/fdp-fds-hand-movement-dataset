"""
Recording engine for FDP/FDS hand movement tests.

This module connects:
    Camera
       ↓
    MediaPipe
       ↓
    Landmark extraction
       ↓
    Feature extraction
       ↓
    Visualization
       ↓
    CSV dataset
"""

import cv2
import time
import os
from datetime import datetime

from config import (
    RECORDING_SECONDS,
    MIRROR_CAMERA,

    DATASET_FOLDER,

    RED,
    YELLOW,
    WHITE,
    CYAN,
)

from hand_tracking import detect_hand

from feature_extraction import (
    get_angles,
)

from visualization import (
    put_text,
    draw_hand,
    highlight_finger,
)

from dataset import (
    get_test_folder,
    save_recording,
    save_test_summary,
)

from ui import (
    show_instructions,
    countdown,
    ask_pain,
)


# ============================================================
# RECORD ONE TEST
# ============================================================

def record_test(
    cap,
    landmarker,
    finger,
    test_type,
    subject_id,
    label,
):
    """
    Record one complete FDP/FDS test.

    Flow:

        Instructions
             ↓
        SPACE
             ↓
        Countdown
             ↓
        Recording
             ↓
        R / automatic stop
             ↓
        Pain score
             ↓
        Save CSV
    """

    # --------------------------------------------------------
    # Instructions
    # --------------------------------------------------------

    if not show_instructions(
        cap,
        finger,
        test_type,
    ):
        return False

    # --------------------------------------------------------
    # Countdown
    # --------------------------------------------------------

    if not countdown(
        cap,
        finger,
        test_type,
    ):
        return False

    print(
        f"\nRecording started for "
        f"{RECORDING_SECONDS} seconds."
    )

    print(
        "[R = stop early] [ESC = cancel]"
    )

    # --------------------------------------------------------
    # Recording variables
    # --------------------------------------------------------

    rows = []

    frame_number = 0

    last_timestamp = 0

    recording_start_time = time.time()

    # --------------------------------------------------------
    # Recording loop
    # --------------------------------------------------------

    while True:

        recording_elapsed = (
            time.time()
            - recording_start_time
        )

        # Automatic stop
        if recording_elapsed >= RECORDING_SECONDS:
            break

        ret, frame = cap.read()

        if not ret:

            print(
                "Could not read webcam."
            )

            return False

        # ----------------------------------------------------
        # Mirror camera
        # ----------------------------------------------------

        if MIRROR_CAMERA:

            frame = cv2.flip(
                frame,
                1,
            )

        # ----------------------------------------------------
        # MediaPipe timestamp
        # ----------------------------------------------------

        now = time.time()

        timestamp_ms = int(
            now * 1000
        )

        if timestamp_ms <= last_timestamp:

            timestamp_ms = (
                last_timestamp + 1
            )

        last_timestamp = timestamp_ms

        # ----------------------------------------------------
        # Detect hand
        # ----------------------------------------------------

        result = detect_hand(
            landmarker,
            frame,
            timestamp_ms,
        )

        # ====================================================
        # HAND DETECTED
        # ====================================================

        if result.hand_landmarks:

            landmarks = (
                result.hand_landmarks[0]
            )

            # ------------------------------------------------
            # Draw hand
            # ------------------------------------------------

            draw_hand(
                frame,
                landmarks,
            )

            # ------------------------------------------------
            # Highlight tested finger
            # ------------------------------------------------

            highlight_finger(
                frame,
                landmarks,
                finger,
                test_type,
            )

            # ------------------------------------------------
            # Calculate features
            # ------------------------------------------------

            angles = get_angles(
                landmarks,
                finger,
            )

            frame_number += 1

            # ------------------------------------------------
            # Create frame row
            # ------------------------------------------------

            row = [
                datetime.now().isoformat(),

                frame_number,

                subject_id,

                finger,

                test_type,

                label,

                angles["mcp_angle"],

                angles["pip_angle"],

                angles["dip_angle"],

                angles["tip_mcp_distance"],

                angles["tip_pip_distance"],

                angles["tip_wrist_distance"],
            ]

            # ------------------------------------------------
            # Add all 21 landmarks
            # ------------------------------------------------

            for landmark in landmarks:

                row.extend([
                    round(
                        landmark.x,
                        6,
                    ),

                    round(
                        landmark.y,
                        6,
                    ),

                    round(
                        landmark.z,
                        6,
                    ),
                ])

            rows.append(
                row
            )

            # ------------------------------------------------
            # Display joint angles
            # ------------------------------------------------

            put_text(
                frame,
                f"MCP: "
                f"{angles['mcp_angle']:.1f} deg",
                20,
                35,
                0.58,
                WHITE,
                2,
            )

            put_text(
                frame,
                f"PIP: "
                f"{angles['pip_angle']:.1f} deg",
                20,
                70,
                0.58,
                YELLOW
                if test_type == "FDS"
                else WHITE,
                2,
            )

            put_text(
                frame,
                f"DIP: "
                f"{angles['dip_angle']:.1f} deg",
                20,
                105,
                0.58,
                YELLOW
                if test_type == "FDP"
                else WHITE,
                2,
            )

        # ====================================================
        # HAND NOT DETECTED
        # ====================================================

        else:

            put_text(
                frame,
                "HAND NOT DETECTED",
                350,
                60,
                0.75,
                RED,
                2,
            )

        # ----------------------------------------------------
        # Recording information
        # ----------------------------------------------------

        remaining_time = max(
            0,
            RECORDING_SECONDS
            - int(recording_elapsed),
        )

        put_text(
            frame,
            "● RECORDING",
            20,
            frame.shape[0] - 100,
            0.65,
            RED,
            2,
        )

        put_text(
            frame,
            f"Time left: {remaining_time}s",
            20,
            frame.shape[0] - 65,
            0.58,
            YELLOW,
            2,
        )

        put_text(
            frame,
            f"Frames: {frame_number}",
            20,
            frame.shape[0] - 30,
            0.55,
            WHITE,
            1,
        )

        put_text(
            frame,
            "Press R = stop",
            frame.shape[1] - 230,
            frame.shape[0] - 30,
            0.5,
            YELLOW,
            1,
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        cv2.imshow(
            "Hand Movement Test",
            frame,
        )

        key = (
            cv2.waitKey(1)
            & 0xFF
        )

        # R = stop
        if key in [
            ord("r"),
            ord("R"),
        ]:
            break

        # ESC = cancel
        if key == 27:
            return False

    # --------------------------------------------------------
    # Recording finished
    # --------------------------------------------------------

    print(
        f"\nRecorded {len(rows)} frames."
    )

    # --------------------------------------------------------
    # Close window before console input
    # --------------------------------------------------------

    cv2.destroyWindow(
        "Hand Movement Test"
    )

    # --------------------------------------------------------
    # Pain score
    # --------------------------------------------------------

    pain = ask_pain()

    # --------------------------------------------------------
    # Don't save empty recordings
    # --------------------------------------------------------

    if not rows:

        print(
            "\nNo hand landmarks were recorded."
        )

        cv2.namedWindow(
            "Hand Movement Test",
            cv2.WINDOW_NORMAL,
        )

        return False

    # --------------------------------------------------------
    # Save test summary
    # --------------------------------------------------------

    save_test_summary(
        subject_id=subject_id,
        finger=finger,
        test_type=test_type,
        label=label,
        pain=pain,
        rows=rows,
    )

    # --------------------------------------------------------
    # Create filename
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    test_folder = get_test_folder(
        test_type
    )

    filename = os.path.join(
        test_folder,
        (
            f"{test_type}_"
            f"{finger}_"
            f"{label}_"
            f"{subject_id}_"
            f"{timestamp}.csv"
        ),
    )

    # --------------------------------------------------------
    # Save recording
    # --------------------------------------------------------

    success = save_recording(
        filename,
        rows,
    )

    if not success:
        return False

    print(
        f"\n[DATA SAVED] {filename}"
    )

    print(
        f"[PAIN SCORE] {pain}/10"
    )

    print(
        "\nReturning to the live webcam preview..."
    )

    # --------------------------------------------------------
    # Re-create OpenCV window
    # --------------------------------------------------------

    cv2.namedWindow(
        "Hand Movement Test",
        cv2.WINDOW_NORMAL,
    )

    return True