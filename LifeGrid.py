import random


class LifeGrid(list):
        global rules

        ##
        # @author Wouter Coppieters
        # @private
        # @name LifeGrid
        # @private @param rules

        ##
        # @param self the LifeGrid Object
        # @param width width of the canvas
        # @param height height of the canvas
        # @param rule name of rule set to apply, or a custom rule set in format:
        #     spawn_on/survive_on (e.g 3/23 == "life")
        def __init__(self, canvas, width=20, height=20, rule="life"):
            """The constructor."""
            self.rules = {
                "day_and_night": ([3, 6, 7, 8], [3, 4, 6, 7, 8]),
                "life": ([3], [2, 3]),
                "34": ([3, 4], [3, 4]),
                "highlife": ([3, 6], [2, 3]),
                "seeds": ([2], []),
                "life_without_death": ([3], [0, 1, 2, 3, 4, 5, 6])
                }

            self.dragAlive = 0
            self.width = width
            self.height = height
            self.rects = []
            self.canvas = canvas
            self.rectMap = {}
            self.fillGrid()
            rules = self.rules.get(rule, False)
            if rules:
                self.spawnOn, self.surviveOn = rules
            else:
                self.spawnOn, self.surviveOn = list(rule.split("/")[0]),

        def onObjectClick(self, event):
            clicked = event.widget.find_closest(event.x, event.y)
            x, y = self.rectMap[clicked[0]]
            self.dragAlive = self.toggleAlive(x, y)

        def onObjectDrag(self, event):
            dragged = event.widget.find_closest(event.x, event.y)
            x, y = self.rectMap[dragged[0]]
            if self.dragAlive:
                self.setAlive(x, y)
            else:
                self.setDead(x, y)

        def toggleAlive(self, x, y):
            self[x][y] *= -1
            self[x][y] += 1
            status = self[x][y]
            if status:
                try:
                    col = random.randint(0, 16777215)
                    col = "#%06x" % col

                    self.canvas.itemconfig(
                        self.rects[x][y],
                        fill="{}".format(col)
                        )
                except:
                    self.canvas.itemconfig(self.rects[x][y], fill="black")
            else:
                self.canvas.itemconfig(self.rects[x][y], fill="white")

            return status

        def setAlive(self, x, y):
            self[x][y] = 1
            col = random.randint(0, 16777215)
            col = "%x" % col
            col = col.ljust(6, '0')
            col = "#" + col
            self.canvas.itemconfig(self.rects[x][y], fill="{}".format(col))

        def setDead(self, x, y):
            self[x][y] = 0
            self.canvas.itemconfig(self.rects[x][y], fill="white")

        def fillGrid(self):
            cwidth = int(self.canvas.cget("width"))

            boxWidth = cwidth / self.width

            for x in range(0, self.width):
                self.append([])
                self.rects.append([])

                for y in range(0, self.height):
                    self[x].append(0)
                    rect = self.canvas.create_rectangle(
                        3 + (boxWidth * x),
                        3 + (boxWidth * y),
                        boxWidth * (x + 1) + 2,
                        boxWidth * (y + 1) + 2,
                        fill="white",
                        outline=""
                        )
                    self.canvas.tag_bind(rect, '<Button-1>', self.onObjectClick)
                    self.canvas.tag_bind(rect, '<B1-Motion>', self.onObjectDrag)
                    self.rects[x].append(rect)
                    self.rectMap[rect] = (x, y)

        def getNumberOfAliveNeighbours(self, x, y):

            neighbours = 0
            minX = x - 1
            maxX = x + 1
            minY = y - 1
            maxY = y + 1

            if(x <= 0):
                minX = 0
            if(x >= self.width - 1):
                maxX = self.width - 1
            if(y <= 0):
                minY = 0
            if(y >= self.height - 1):
                maxY = self.height - 1

            for nx in range(minX, maxX + 1):
                for ny in range(minY, maxY + 1):
                    if(x == nx and y == ny):
                        continue

                    neighbours += (self[nx][ny])

            return neighbours

        def tick(self):
            self.newState = {}

            toCheck = {}

            for x in range(0, self.width):
                for y in range(0, self.height):
                    cell = self[x][y]

                    if(cell):
                        minX = x - 1
                        maxX = x + 1
                        minY = y - 1
                        maxY = y + 1

                        if(x <= 0):
                            minX = 0
                        if(x >= self.width - 1):
                            maxX = self.width - 1
                        if(y <= 0):
                            minY = 0
                        if(y >= self.height - 1):
                            maxY = self.height - 1

                        for nx in range(minX, maxX + 1):
                            for ny in range(minY, maxY + 1):
                                toCheck[nx, ny] = True

            for x, y in toCheck:

                cell = self[x][y]
                neighbours = self.getNumberOfAliveNeighbours(x, y)

                if(cell and neighbours in self.surviveOn):
                        pass
                elif(not cell and neighbours in self.spawnOn):
                        self.newState[(x, y)] = 1
                else:
                    self.newState[(x, y)] = 0

            for pos, alive in self.newState.items():
                x, y = pos
                if alive:
                    self.setAlive(x, y)
                else:
                    self.setDead(x, y)
