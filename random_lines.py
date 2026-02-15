import random
from pathlib import Path

INPUT_PATH = Path("files/RandomInput.txt")
OUTPUT_PATH = Path("files/RandomOutput.txt")


def main():
    lines = INPUT_PATH.read_text(encoding="utf-8").splitlines()
    random.shuffle(lines)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
