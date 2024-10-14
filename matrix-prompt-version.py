
import random, time

class Matrix:
    
    SEQUENCE: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234456789.,;:/?|!@#$%¨&*()-+="
    NUMBER: str = "0123456789"

    def __init__(self, nodes: int | None=32, ground: int | None=30, column: int | None=120):
        self.position: str = "\033[{};{}H"
        self.clear: str = "\033[2J"
        self.promptHide: str = "\033[?25l"
        self.prompt: str = "\033[?25h"

        self.colorBright: str = "\033[1;{}m"
        self.colorDimmed: str = "\033[2;{}m"
        self.foreColors: dict = {"black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34, "magenta": 35, "cyan": 36, "white": 37, "none": 38, "default": 39, "reset": 0}
        self.colorReset: str = "\033[0m"

        self.nodes: int = nodes if nodes <= (column*.8) else int(column*.8)
        self.column: int = column
        self.ground: int = ground

    def locate(self, row, col):
        return f"\033[{row};{col}H"


    def clearScreen(self):
        print(self.clear, self.promptHide)


    def defaults(self):
        self.row: list[float] = [1.00]
        self.col: list[int] = []; self.col = [self.rangeColumn()]
        self.velocity: list[float] = [self.choiceVelocity()]
        self.trailNodes: list[list] = [[]]
        self.trailLength: list[int] = [self.rangeLength()]


    def resetNodes(self):
        self.row[self.id] = 1
        self.col[self.id] = self.rangeColumn()
        self.velocity[self.id] = self.choiceVelocity()


    def choiceVelocity(self) -> float:
        return random.choice(seq=[0.10, 0.20, 0.25, 0.50])


    def rangeColumn(self) -> int:
        while True:
            callColumn: int = random.randrange(start=1, stop=self.column, step=1)
            if callColumn not in self.col:
                break
        return callColumn


    def rangeLength(self) -> int:
        return random.randrange(start=4, stop=16, step=1)


    def createNode(self):
        self.row.append(1)
        self.col.append(self.rangeColumn())
        self.velocity.append(self.choiceVelocity())
        self.trailLength.append(self.rangeLength())
        self.trailNodes.append([])


    def trail(self):
        if len(self.trailNodes[self.id]) > self.trailLength[self.id]:
            del self.trailNodes[self.id][0]
        for i in range(len(self.trailNodes[self.id])):
            self.trailNodes[self.id][i][2] = random.choice(seq=self.NUMBER) if self.trailNodes[self.id][i][2] in self.NUMBER else self.trailNodes[self.id][i][2]
            print (self.locate(int(self.trailNodes[self.id][i][0]), self.trailNodes[self.id][i][1]) + self.colorDimmed.format(self.foreColors["green"]) + (self.trailNodes[self.id][i][2] if i != 0 else " ") + self.colorReset)


    def matrix(self):
        char: str = random.choice(seq=self.SEQUENCE)
        
        if self.row[self.id] == int(self.row[self.id]):
                self.trailNodes[self.id].append([int(self.row[self.id]), self.col[self.id], char])

        self.trail()

        print (self.locate(int(self.row[self.id]), self.col[self.id]) + self.colorBright.format(self.foreColors["white"]) + char + self.colorReset)


    def start(self):
        self.clearScreen()
        self.defaults()

        acelerate: int = 0
        sleep: bool = True

        while True:
            
            for self.id in range(int(acelerate)):
                self.matrix()
                self.row[self.id] = float("{:2f}".format(self.row[self.id] + self.velocity[self.id]))

                if self.row[self.id] >= self.ground:
                    self.resetNodes()
                if len(self.trailNodes) <= self.nodes:
                    self.createNode()
            
            if sleep:
                if acelerate < self.nodes:
                    acelerate += .2
                    time.sleep(abs(self.nodes-acelerate)/(self.nodes*100))
                else:
                    acelerate = self.nodes
                    sleep = False


matrix = Matrix()
matrix.start()