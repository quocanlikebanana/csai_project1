import random

EX_1 = 255
EX_2 = 255**2
EX_3 = 255**3

BASE_COLOR = {
    "GRAY": (127, 127, 127),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    ### =====
    "DARK_GRAY": (63, 63, 63),  # BLOCKED (when button is in app)
    "BLUE": (0, 0, 255),  # START
    "PINK": (255, 0, 255),  # END
    "GREEN": (0, 255, 0),  # OPENED
    "RED": (255, 0, 0),  # CLOSED
    "YELLOW": (255, 255, 0),  # DONE
    "TEAL": (0, 128, 128),  # PICKUP
}


def genColor(red: int, green: int, blue: int):
    return (red, green, blue)


def isCloseColor(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> bool:
    DIFF = 24 * 3
    if (
        abs(color1[0] - color2[0])
        + abs(color1[1] - color2[1])
        + abs(color1[2] - color2[2])
        < DIFF
    ):
        return True
    return False


def encodeRGB(color: tuple[int, int, int]):
    return color[0] + color[1] * EX_1 + color[2] * EX_2


def decodeRGB(code):
    red = code % EX_1
    green = (code // EX_1) % EX_1
    blue = (code // EX_2) % EX_1
    return (red, green, blue)


# Generate random color that differ from pre-defined ones and distinct
def genRandomDistinctColor(n):
    reds = list(range(0, 255))
    greens = list(range(0, 255))
    blues = list(range(0, 255))
    random.shuffle(reds)
    random.shuffle(greens)
    random.shuffle(blues)

    bannedColor = list(BASE_COLOR.values())
    chosenColor = []
    validflag = True
    index = random.randrange(0, EX_3)
    while len(chosenColor) < n:
        validflag = True
        colorIndex = decodeRGB(index % EX_3)
        color = genColor(
            reds[colorIndex[0]], greens[colorIndex[1]], blues[colorIndex[2]]
        )
        for banned in bannedColor:
            if isCloseColor(banned, color):
                index += 1
                validflag = False
                break
        if validflag:
            for chosen in chosenColor:
                if isCloseColor(chosen, color):
                    index += 1
                    validflag = False
                    break
        if validflag or index // EX_3 >= 2:
            chosenColor.append(color)
    return chosenColor
