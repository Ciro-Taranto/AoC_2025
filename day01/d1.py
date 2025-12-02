class Dial:
    def __init__(self):
        self.position = 50
        self.zeros = 0

    def move(self, instruction: str) -> None:
        sign, clicks = self.parse_instruction(instruction)
        self.position = (self.position + sign * clicks) % 100
        if self.position == 0:
            self.zeros += 1

    @staticmethod
    def parse_instruction(instruction: str) -> tuple[int, int]:
        if instruction[0] == "L":
            sign = -1
        elif instruction[0] == "R":
            sign = +1
        else:
            raise ValueError
        clicks = int(instruction[1:])
        if clicks == 0:
            raise ValueError
        return sign, clicks


class DialP2(Dial):
    def move(self, instruction: str) -> None:
        sign, clicks = self.parse_instruction(instruction)
        old = self.position
        new = old + sign * clicks
        self.zeros += abs(new // 100 - old // 100)
        self.position = new % 100

    def move_brute_force(self, instructions: str) -> None:
        sign, clicks = self.parse_instruction(instructions)
        for _ in range(clicks):
            self.position += sign
            self.position = self.position % 100
            self.zeros += self.position == 0


if __name__ == "__main__":
    from pathlib import Path

    with open(Path(__file__).parent / "input.txt", "r") as f:
        instructions = f.readlines()

    dial = Dial()
    for instruction in instructions:
        dial.move(instruction.replace("\n", ""))
    print(dial.zeros)
    dial2 = DialP2()
    dial3 = DialP2()
    for i, instruction in enumerate(instructions):
        dial2.move(instruction.replace("\n", ""))
        dial3.move_brute_force(instruction.replace("\n", ""))
        if dial2.zeros != dial3.zeros:
            # print(
            #     instruction.strip(),
            #     dial2.position,
            #     dial3.position,
            #     dial2.zeros,
            #     dial3.zeros,
            # )
            # print(i)
            # break
            ...

    print(dial2.zeros)
    print(dial3.zeros)
