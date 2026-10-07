"""
User interface utilities.

Handles:
- Subject ID
- Finger selection
- Test selection
- Label selection
- Pain score
- Test instructions
- Recording countdown
"""

import time

import cv2

from config import (
    FINGERS,
    TESTS,

    MIRROR_CAMERA,

    RECORDING_SECONDS,
    COUNTDOWN_SECONDS,

    DARK,
    CYAN,
    GREEN,
    YELLOW,
    WHITE,
)

from visualization import put_text


# ============================================================
# SUBJECT ID
# ============================================================

def get_subject_id():
    """
    Ask for subject ID.
    """

    while True:

        subject_id = input(
            "\nEnter subject ID: "
        ).strip()

        if subject_id:

            return subject_id

        print(
            "Subject ID cannot be empty."
        )


# ============================================================
# FINGER SELECTION
# ============================================================

def select_finger():
    """
    Ask the user to select a finger.
    """

    fingers = list(
        FINGERS.keys()
    )

    print(
        "\nSelect finger:"
    )

    for index, finger in enumerate(
        fingers,
        start=1,
    ):

        print(
            f"{index}. {finger}"
        )

    while True:

        choice = input(
            "\nEnter choice: "
        ).strip()

        if choice.isdigit():

            index = int(
                choice
            )

            if (
                1 <= index
                <= len(fingers)
            ):

                return fingers[
                    index - 1
                ]

        print(
            "Invalid choice. "
            "Please select a valid finger."
        )


# ============================================================
# TEST SELECTION
# ============================================================

def select_test():
    """
    Ask the user to select FDP or FDS.
    """

    tests = list(
        TESTS.keys()
    )

    print(
        "\nSelect test:"
    )

    for index, test in enumerate(
        tests,
        start=1,
    ):

        print(
            f"{index}. {test}"
        )

    while True:

        choice = input(
            "\nEnter choice: "
        ).strip()

        if choice.isdigit():

            index = int(
                choice
            )

            if (
                1 <= index
                <= len(tests)
            ):

                return tests[
                    index - 1
                ]

        print(
            "Invalid choice. "
            "Please select a valid test."
        )


# ============================================================
# LABEL SELECTION
# ============================================================

def select_label():
    """
    Ask for the movement/injury label.
    """

    while True:

        label = input(
            "\nEnter label: "
        ).strip()

        if label:

            return label

        print(
            "Label cannot be empty."
        )


# ============================================================
# PAIN SCORE
# ============================================================

def ask_pain():
    """
    Ask for pain score from 0 to 10.

    Decimal values are allowed.

    Pressing ENTER gives 0.
    """

    print(
        "\n================================"
    )

    print(
        "PAIN SCORE"
    )

    print(
        "================================"
    )

    print(
        "0 = no pain"
    )

    print(
        "10 = worst pain"
    )

    while True:

        value = input(
            "Pain score "
            "(0-10, ENTER = 0): "
        ).strip()

        # ENTER = 0
        if value == "":
            return 0.0

        try:

            pain = float(
                value
            )

            if 0 <= pain <= 10:

                return pain

        except ValueError:
            pass

        print(
            "Please enter a number "
            "between 0 and 10."
        )


# ============================================================
# TEST INSTRUCTIONS
# ============================================================

def show_instructions(
    cap,
    finger,
    test_type,
):
    """
    Display instructions before recording.

    SPACE = start
    ESC   = cancel
    """

    test = TESTS[
        test_type
    ]

    while True:

        ret, frame = cap.read()

        if not ret:

            return False

        if MIRROR_CAMERA:

            frame = cv2.flip(
                frame,
                1,
            )

        height, width = (
            frame.shape[:2]
        )

        # ----------------------------------------------------
        # Dark overlay
        # ----------------------------------------------------

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (width, height),
            DARK,
            -1,
        )

        frame = cv2.addWeighted(
            overlay,
            0.75,
            frame,
            0.25,
            0,
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        put_text(
            frame,
            test["title"],
            40,
            55,
            0.9,
            CYAN,
            2,
        )

        put_text(
            frame,
            f"Finger: {finger}",
            40,
            95,
            0.65,
            GREEN,
            2,
        )

        # ----------------------------------------------------
        # Instructions
        # ----------------------------------------------------

        y = 150

        for number, instruction in enumerate(
            test["instructions"],
            start=1,
        ):

            put_text(
                frame,
                f"{number}. {instruction}",
                40,
                y,
                0.58,
                WHITE,
                1,
            )

            y += 42

        # ----------------------------------------------------
        # Controls
        # ----------------------------------------------------

        put_text(
            frame,
            (
                "[SPACE = Start "
                f"{RECORDING_SECONDS}-sec recording]"
            ),
            40,
            height - 70,
            0.65,
            YELLOW,
            2,
        )

        put_text(
            frame,
            "ESC = Cancel",
            40,
            height - 35,
            0.5,
            WHITE,
            1,
        )

        cv2.imshow(
            "Hand Movement Test",
            frame,
        )

        key = (
            cv2.waitKey(1)
            & 0xFF
        )

        if key == 32:

            return True

        if key == 27:

            return False


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(
    cap,
    finger,
    test_type,
):
    """
    Display countdown before recording.
    """

    start_time = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:

            return False

        if MIRROR_CAMERA:

            frame = cv2.flip(
                frame,
                1,
            )

        elapsed = (
            time.time()
            - start_time
        )

        remaining = (
            COUNTDOWN_SECONDS
            - int(elapsed)
        )

        if remaining <= 0:

            return True

        height, width = (
            frame.shape[:2]
        )

        put_text(
            frame,
            f"{test_type} - {finger}",
            30,
            45,
            0.7,
            CYAN,
            2,
        )

        put_text(
            frame,
            "GET READY",
            30,
            90,
            0.7,
            YELLOW,
            2,
        )

        cv2.putText(
            frame,
            str(remaining),
            (
                width // 2 - 35,
                height // 2,
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            WHITE,
            5,
            cv2.LINE_AA,
        )

        cv2.imshow(
            "Hand Movement Test",
            frame,
        )

        key = (
            cv2.waitKey(1)
            & 0xFF
        )

        if key == 27:

            return False