"""
FDP / FDS Hand Movement Dataset Collector.

Main entry point.

This file coordinates the different modules.
"""

import cv2

from config import (
    MIRROR_CAMERA,
    DATASET_FOLDER,

    RED,
    YELLOW,
    WHITE,
    CYAN,
)

from camera import open_webcam

from hand_tracking import (
    create_landmarker,
    detect_hand,
)

from feature_extraction import (
    get_angles,
)

from visualization import (
    put_text,
    draw_hand,
    highlight_finger,
)

from dataset import (
    create_dataset_folders,
)

from ui import (
    select_finger,
    select_test,
    select_label,
    get_subject_id,
)

from recorder import (
    record_test,
)


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n=============================================="
    )

    print(
        "      FDP / FDS HAND MOVEMENT COLLECTOR"
    )

    print(
        "=============================================="
    )

    print(
        "\n[WEBCAM ONLY]"
    )

    print(
        "Phone/IP camera is NOT being used."
    )

    # --------------------------------------------------------
    # Create dataset folders
    # --------------------------------------------------------

    create_dataset_folders()

    # --------------------------------------------------------
    # User selections
    # --------------------------------------------------------

    finger = select_finger()

    test_type = select_test()

    label = select_label()

    subject_id = get_subject_id()

    print(
        f"\nSubject : {subject_id}"
    )

    print(
        f"Finger  : {finger}"
    )

    print(
        f"Test    : {test_type}"
    )

    print(
        f"Label   : {label}"
    )

    # --------------------------------------------------------
    # Open webcam
    # --------------------------------------------------------

    try:

        cap = open_webcam()

    except RuntimeError as error:

        print(
            f"\nERROR: {error}"
        )

        input(
            "\nPress ENTER to exit..."
        )

        return

    # --------------------------------------------------------
    # Create MediaPipe landmarker
    # --------------------------------------------------------

    try:

        landmarker = (
            create_landmarker()
        )

    except Exception as error:

        print(
            "\nERROR: Could not initialize "
            "MediaPipe Hand Landmarker."
        )

        print(
            f"\nDetails: {error}"
        )

        cap.release()

        input(
            "\nPress ENTER to exit..."
        )

        return

    # --------------------------------------------------------
    # Open preview window
    # --------------------------------------------------------

    window_name = (
        "Hand Movement Test"
    )

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL,
    )

    print(
        "\n=============================================="
    )

    print(
        "LIVE PREVIEW"
    )

    print(
        "=============================================="
    )

    print(
        "\nShow your hand to the camera."
    )

    print(
        "Press SPACE to start the test."
    )

    print(
        "Press Q or ESC to quit."
    )

    try:
        last_timestamp_ms = -1

        while True:

            # ------------------------------------------------
            # Capture frame
            # ------------------------------------------------

            ret, frame = cap.read()

            if not ret:

                print(
                    "\nCould not read webcam frame."
                )

                break

            # ------------------------------------------------
            # Mirror camera
            # ------------------------------------------------

            if MIRROR_CAMERA:

                frame = cv2.flip(
                    frame,
                    1,
                )

            # ------------------------------------------------
            # MediaPipe timestamp
            # ------------------------------------------------

            timestamp_ms = int(
               cv2.getTickCount()
               / cv2.getTickFrequency()
               * 1000
            )

            if timestamp_ms <= last_timestamp_ms:
               timestamp_ms = last_timestamp_ms + 1

            last_timestamp_ms = timestamp_ms

            # ------------------------------------------------
            # Detect hand
            # ------------------------------------------------

            result = detect_hand(
                landmarker,
                frame,
                timestamp_ms,
            )

            # ------------------------------------------------
            # Hand detected
            # ------------------------------------------------

            if result.hand_landmarks:

                landmarks = (
                    result.hand_landmarks[0]
                )

                # --------------------------------------------
                # Draw hand
                # --------------------------------------------

                draw_hand(
                    frame,
                    landmarks,
                )

                # --------------------------------------------
                # Highlight selected finger
                # --------------------------------------------

                highlight_finger(
                    frame,
                    landmarks,
                    finger,
                    test_type,
                )

                # --------------------------------------------
                # Calculate angles
                # --------------------------------------------

                angles = get_angles(
                    landmarks,
                    finger,
                )

                # --------------------------------------------
                # Display information
                # --------------------------------------------

                put_text(
                    frame,
                    f"Finger: {finger}",
                    20,
                    35,
                    0.6,
                    CYAN,
                    2,
                )

                put_text(
                    frame,
                    f"Test: {test_type}",
                    20,
                    70,
                    0.6,
                    YELLOW,
                    2,
                )

                put_text(
                    frame,
                    (
                        f"MCP: "
                        f"{angles['mcp_angle']:.1f}"
                    ),
                    20,
                    110,
                    0.55,
                    WHITE,
                    1,
                )

                put_text(
                    frame,
                    (
                        f"PIP: "
                        f"{angles['pip_angle']:.1f}"
                    ),
                    20,
                    145,
                    0.55,
                    WHITE,
                    1,
                )

                put_text(
                    frame,
                    (
                        f"DIP: "
                        f"{angles['dip_angle']:.1f}"
                    ),
                    20,
                    180,
                    0.55,
                    WHITE,
                    1,
                )

            # ------------------------------------------------
            # Hand not detected
            # ------------------------------------------------

            else:

                put_text(
                    frame,
                    "Show your hand to the camera",
                    30,
                    50,
                    0.7,
                    RED,
                    2,
                )

            # ------------------------------------------------
            # Controls
            # ------------------------------------------------

            put_text(
                frame,
                "[SPACE = Start Test]  [Q = Quit]",
                25,
                frame.shape[0] - 25,
                0.6,
                YELLOW,
                2,
            )

            # ------------------------------------------------
            # Show frame
            # ------------------------------------------------

            cv2.imshow(
                window_name,
                frame,
            )

            key = (
                cv2.waitKey(1)
                & 0xFF
            )

            # ------------------------------------------------
            # SPACE = start recording
            # ------------------------------------------------

            if key == 32:

                success = record_test(
                    cap,
                    landmarker,
                    finger,
                    test_type,
                    subject_id,
                    label,
                )

                if success:

                    print(
                        "\nTest completed successfully."
                    )

                else:

                    print(
                        "\nTest cancelled."
                    )

                print(
                    "\nReturning to live preview."
                )

            # ------------------------------------------------
            # Q / ESC = quit
            # ------------------------------------------------

            elif key in [
                ord("q"),
                ord("Q"),
                27,
            ]:

                break

    finally:

        # ----------------------------------------------------
        # Cleanup
        # ----------------------------------------------------

        print(
            "\nClosing program..."
        )

        landmarker.close()

        cap.release()

        cv2.destroyAllWindows()

    print(
        "\n=============================================="
    )

    print(
        "PROGRAM CLOSED"
    )

    print(
        "=============================================="
    )

    print(
        f"\nDataset folder:"
        f"\n{DATASET_FOLDER}"
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()