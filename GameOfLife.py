from Tkinter import *
from LifeGrid import *
import tkSimpleDialog as tks


master = Tk()
canvas = Canvas(master, height=1000, width=1000)


def setup_ui():
    global master, canvas, job, skip

    job = None
    skip = False

    menubar = Menu(master)
    master.config(menu=menubar)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=new_game, accelerator='Command-n')
    filemenu.add_command(label="Quit", command=master.quit, accelerator="Cmd-Q")
    menubar.add_cascade(label="File", menu=filemenu)

    startButton = Button(master, text="Start", command=start)
    stopButton = Button(master, text="Stop", command=stopGame)

    startButton.pack()
    stopButton.pack()
    canvas.pack()

    master.bind('<space>', toggle)
    master.bind('<Command-n>', start_new_game)


def loop():
        global stop
        if stop:
            return
        grid.tick()
        master.after(60, loop)


def start():
    global stop
    stop = False
    master.after(60, loop)


def stopGame():
    global stop
    stop = True


def start_new_game(N=None):
    master.after(60, new_game)


def toggle(N=None):
    global stop
    if(stop):
        start()
    else:
        stopGame()


def new_game(caller=None):
    global grid, skip, canvas, boardSize, tks

    stopGame()
    canvas.delete("all")

    boardSize = tks.askinteger("Width of the board", "Board size? (5-250)", minvalue=5.0, maxvalue=250.0, initialvalue=50)
    rule = tks.askstring("Game Rules", """Which life rule do you want to use? Valid options are:
        day_and_night
        life
        34
        highlife
        seeds
        OR a custom born/survive format, e.g:
        16/23
        123/46
        """, initialvalue="life")
    grid = LifeGrid(canvas, width=boardSize, height=boardSize, rule=rule)

    if(skip):
        return

    skip = True
    mainloop()


setup_ui()
new_game(None)
