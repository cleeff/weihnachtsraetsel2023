import numpy as np
import textwrap
import re
import functools
from tqdm import tqdm


def main():
    innerColor = textwrap.dedent(
        """\
    ckkggbbkckg
    cbbgbgkcbkg
    kckgbggggbc
    bckkkgbkcgb
    bbkcbkkgccb
    gbccccbbkkg
    gcckkkgkkkc
    cbgcgcckckb
    kbbbkbbbbgc
    """
    )

    outerColor = textwrap.dedent(
        """\
    gbckbkgbkgc
    bgkcgbgbcck
    ggbbkccckkk
    kbgbckcckck
    cccbkbckkgg
    ckkkggkccbc
    bbgccbbbggg
    bkkbckbbbgg
    gccgggkckck
    """
    )

    symbols = np.array(
        [
            [8, 9, 10, 11, 12, 9, 11, 8, 10, 12, 8],
            [9, 12, 11, 10, 8, 12, 12, 10, 8, 10, 10],
            [8, 1, 12, 9, 1, 1, 12, 7, 4, 12, 7],
            [10, 12, 4, 12, 11, 2, 10, 9, 9, 1, 12],
            [6, 12, 9, 4, 8, 5, 7, 9, 12, 3, 2],
            [1, 5, 6, 11, 12, 7, 10, 4, 11, 10, 9],
            [2, 11, 3, 8, 6, 5, 9, 1, 2, 10, 9],
            [12, 3, 2, 11, 3, 8, 10, 1, 6, 8, 2],
            [4, 11, 6, 5, 9, 10, 1, 4, 8, 7, 7],
        ]
    )

    innerColor = innerColor.replace("\n", "")
    outerColor = outerColor.replace("\n", "")
    innerColor = np.array(list(innerColor))
    outerColor = np.array(list(outerColor))
    symbols = symbols.reshape(-1)

    combined = np.array(list(zip(innerColor, outerColor, symbols)))
    # print(combined)

    letters = {
        ("k", "b", 1): "h",
        ("g", "c", 1): "d",
        ("k", "g", 2): "e",
        ("g", "b", 2): "o",
        ("b", "k", 3): "z",
        ("g", "c", 3): "u",
        ("k", "g", 4): "s",
        ("c", "b", 4): "a",
        ("b", "g", 5): "k",
        ("k", "b", 5): "e",
        ("k", "c", 6): "r",
        ("c", "b", 6): "r",
        ("c", "g", 7): "e",
        ("k", "c", 7): "n",
        #
        # doch die
        #
        # ("k", "b", 12): "o",
        # ("g", "b", 9): "c",
        # ("g", "c", 12): "i",
        #
        # doch die Sonne
        #
        # ("b", "k", 10): "n",
        # ("c", "b", 12): "e",
        # Sarkophagen
        # ("b", "c", 11): "a",
        # ("k", "g", 9): "o",
        # ("b", "g", 10): "p",
        # ("b", "k", 8): "g",
    }

    swapInnerOuter(innerColor, outerColor, symbols)

    for inner, outer, symbol in zip(innerColor, outerColor, symbols):
        a = letters.get((inner, outer, symbol), None)
        b = letters.get((outer, inner, symbol), None)
        c = a or b or "_"

        print(c, end="")
    print("")

    lines = ReadFile()
    pattern = (
        "d__hd_es_n__s__e___d_r__a_en__uoder__e_a___o_u_re_he___ze_u__hr_os_rk__ha_en"
    )
    pattern = "___ze_u__hr_os_rk__ha_en"
    end = pattern.replace("_", ".")
    for length in tqdm(range(7, 20)):
        for begin in range(len(end) - length + 1):
            sub = end[begin : begin + length]
            r = Regex(sub)
            for line in lines:
                if len(line) != length:
                    continue
                if r.match(line):
                    print(line, sub)


def RotateLetter(b):
    return chr((ord(b) - ord("a") + 13) % 26 + ord("a"))


def MirrorLetter(b):
    index = ord(b) - ord("a")
    return chr(25 - index + ord("a"))


def swapInnerOuter(inner, outer, symbols):
    for i in range(len(symbols)):
        if symbols[i] == 4 or symbols[i] == 7:
            inner[i], outer[i] = outer[i], inner[i]


def ReadFile():
    with open("wortliste.txt") as file:
        lines = file.readlines()
        lines = [line.lower() for line in lines]
        lines = [line.strip() for line in lines]
        return lines


@functools.cache
def Regex(pattern):
    return re.compile(pattern)


main()
