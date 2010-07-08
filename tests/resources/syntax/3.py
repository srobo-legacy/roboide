from sr import *

def main():
    yield 5
    yield vision()
    yield (io.pin[0] == 1) & (io.pin[2] == 0)
    # is the same as:
    yield And(io.pin[0] == 1, io.pin[2] == 0)

    yield (io.pin[0] == 1) | (io.pin[2] == 0)
    # is the same as:
    yield Or(io.pin[0] == 1, io.pin[2] == 0)
    # is the same as:
    yield io.pin[0] == 1, io.pin[2] == 0
