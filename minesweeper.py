import random
import tkinter as tk
import time

class MinesweeperUI:
    def __init__(self, master):

        self.master = master
        self.cellSize = 30 #60
        self.width = 30 #15
        self.height = 20 #10
        self.colours = ['#00c800', '#00a000', '#007800', '#593e10', '#592b10', '#591910', '#300808', '#24100a']
        self.furthest = self.width if self.width > self.height else self.height
        self.board = [[[0, 1] for x in range(self.width)] for y in range(self.height)]
        self.neighbourCount = [[0] * self.width for x in range(self.height)]
        self.madeBoard = False

        self.canvas = tk.Canvas(master, height=self.height * self.cellSize, width=self.width * self.cellSize)

        self.startButton = tk.Button(master, text="Start", font=("Arial", 25), width=40, height=12, command=self.start)
        self.startButton.pack()

        self.loseText = tk.Label(master, text="You Lost", font=("Arial", 25), width=40, height=6)
        self.winText = tk.Label(master, text="You Won!!", font=("Arial", 25), width=40, height=6)

        self.restartButton = tk.Button(master, text="Home", font=("Arial", 25), width=30, height=4, borderwidth=10, pady=1, padx=5, command=self.restartGame)

        self.canvas.bind("<Button-1>", self.uncoverCell)
        self.canvas.bind("<Button-3>", self.toggleFlagCell)
    
    def uncoverCell(self, event):

        x = int(event.x / self.cellSize)
        y = int(event.y / self.cellSize)

        if self.madeBoard == False:
            self.randomBoard(x, y)
            self.madeBoard = True

        if self.board[y][x][1] != 2:

            if 0 <= x < self.width and 0 <= y < self.height:
                self.board[y][x][1] = 0
            
            if self.board[y][x][0] == 0 and self.neighbourCount[y][x] == 0:
                self.checkDirectNeighbours(x, y)
            
            self.drawBoard()

            if self.board[y][x][0] == 1:
                self.drawBoard()
                self.loseGame()
            
            if self.checkWin():
                self.winGame()
            
        
    def toggleFlagCell(self, event):

        x = int(event.x / self.cellSize)
        y = int(event.y / self.cellSize)

        if 0 <= x < self.width and 0 <= y < self.height:
            if self.board[y][x][1] == 2:
                self.board[y][x][1] = 1
            elif self.board[y][x][1] == 1:
                self.board[y][x][1] = 2
        
        self.drawBoard()
    
    def loseGame(self):

        time.sleep(0.5)
        self.loseText.pack()
        self.canvas.destroy()
        self.restartButton.pack()
    
    def winGame(self):

        self.winText.pack()
        self.canvas.destroy()
        self.restartButton.pack()

    
    def restartGame(self):

        self.restartButton.destroy()
        self.loseText.destroy()
        self.winText.destroy()
        game = MinesweeperUI(self.master)

    def start(self):
        
        self.startButton.destroy()
        self.canvas.pack()
        self.drawBoard()
    
    def checkDirectNeighbours(self, x, y):

        if 0 <= y + 1 < self.height and 0 <= x < self.width:
            if self.board[y + 1][x][0] == 0 and self.board[y + 1][x][1] != 0:
                self.board[y + 1][x][1] = 0
                self.checkWin()
                if self.neighbourCount[y + 1][x] == 0:
                    self.checkDirectNeighbours(x, y + 1)

        if 0 <= y - 1 < self.height and 0 <= x < self.width:
            if self.board[y - 1][x][0] == 0 and self.board[y - 1][x][1] != 0:
                self.board[y - 1][x][1] = 0
                self.checkWin()
                if self.neighbourCount[y - 1][x] == 0:
                    self.checkDirectNeighbours(x, y - 1)

        if 0 <= y < self.height and 0 <= x + 1 < self.width:
            if self.board[y][x + 1][0] == 0 and self.board[y][x + 1][1] != 0:
                self.board[y][x + 1][1] = 0
                self.checkWin()
                if self.neighbourCount[y][x + 1] == 0:
                    self.checkDirectNeighbours(x + 1, y)

        if 0 <= y < self.height and 0 <= x - 1 < self.width:
            if self.board[y][x - 1][0] == 0 and self.board[y][x - 1][1] != 0:
                self.board[y][x - 1][1] = 0
                self.checkWin()
                if self.neighbourCount[y][x - 1] == 0:
                    self.checkDirectNeighbours(x - 1, y)
    
    def checkWin(self):

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x][0] == 0 and self.board[y][x][1] != 0:
                    return False
        
        return True
    
    def drawBoard(self):

        self.canvas.delete("all")

        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cellSize
                x2 = x1 + self.cellSize
                y1 = y * self.cellSize
                y2 = y1 + self.cellSize

                if self.board[y][x][1] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                elif self.board[y][x][1] == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                    self.canvas.create_polygon(x1 + self.cellSize / 5, y1 + self.cellSize / 10, x2 - self.cellSize / 5, y2 - self.cellSize / 2 - self.cellSize / 8, x1 + self.cellSize / 5, y2 - self.cellSize / 10 - self.cellSize / 4, fill="red")
                    self.canvas.create_line(x1 + self.cellSize / 5, y1 + self.cellSize / 10, x1 + self.cellSize / 5, y2 - self.cellSize / 10, fill="black", width=self.cellSize / 16)
                elif self.board[y][x][0] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif self.neighbourCount[y][x] > 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colours[self.neighbourCount[y][x] - 1])
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text = str(self.neighbourCount[y][x]), font=(50))
                elif self.board[y][x][0] == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def randomBoard(self, x, y):

        for x in range(int((self.width * self.height) / 10)):

            randomY = random.randint(0, self.height - 1)
            randomX = random.randint(0, self.width - 1)
            while True:
                if self.board[randomY][randomX][0] == 0: 
                    if randomX < (x - 1) or randomX > (x + 1):
                        if randomY < (y - 1) or randomY > (y + 1):
                            break
                randomY = random.randint(0, self.height - 1)
                randomX = random.randint(0, self.width - 1)
            
            self.board[randomY][randomX][0] = 1

            if randomX != 0:
                self.neighbourCount[randomY][randomX - 1] += 1
            if randomY != 0:
                self.neighbourCount[randomY - 1][randomX] += 1
            if randomX != self.width - 1:
                self.neighbourCount[randomY][randomX + 1] += 1
            if randomY != self.height - 1:
                self.neighbourCount[randomY + 1][randomX] += 1
            if randomX != 0 and randomY != 0:
                self.neighbourCount[randomY - 1][randomX - 1] += 1
            if randomX != self.width - 1 and randomY != self.height - 1:
                self.neighbourCount[randomY + 1][randomX + 1] += 1
            if randomX != 0 and randomY != self.height - 1:
                self.neighbourCount[randomY + 1][randomX - 1] += 1
            if randomX != self.width - 1 and randomY != 0:
                self.neighbourCount[randomY - 1][randomX + 1] += 1
            
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("MineSweeper")

    game = MinesweeperUI(root)

    root.mainloop()
