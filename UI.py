import tkinter as tk
from abc import abstractmethod
# def test(event):
#     col = int(event.x//133)
#     row = int(event.y//133)
#     print(row, col)

# wd = tk.Tk()
# wd.title('Tic Tac Toe')
# wd.geometry('800x500')

# canvas = tk.Canvas(wd, height = 400, width = 400, bg='white')
# canvas.place(x=50,y=50, anchor='nw')
# canvas.create_line(0,133,402,133)
# canvas.create_line(0,266,402,266)
# canvas.create_line(133,0,133,402)
# canvas.create_line(266,0,266,402)

# canvas.bind("<Button-1>", test)
# wd.mainloop()

class UI(tk.Frame):
    def __init__(self, piece):
        self.master = tk.Tk()
        super().__init__(self.master, width = 800, height=500)
        self.piece   = piece
        self.infoStr = tk.StringVar()
        self.curTurnUsername = tk.StringVar()
        self.inputUsername = tk.StringVar()

        self.clickCall = None

        self.master.title('Tic Tac Toe')
        # master.geometry('800x500')
        self.pack()

        self.initCanvas()
        self.initWidgets()
    
    def initCanvas(self):
        canvas = tk.Canvas(self, height = 400, width = 400, bg='white')
        canvas.place(x=50,y=50, anchor='nw')
        canvas.create_line(0,133,402,133)
        canvas.create_line(0,266,402,266)
        canvas.create_line(133,0,133,402)
        canvas.create_line(266,0,266,402)
        canvas.place(x=50,y=50, anchor='nw')
        canvas.bind("<Button-1>", self.boardClick)
        self.canvas = canvas

    def initWidgets(self):
        # b = tk.Button(self, command=self.clearBoard, text='test')
        # b.place(x = 600, y = 250)
        
        tk.Label(self, text='Information:', fg='black', width = 35, height = 1).place(x = 500, y = 50)
        tk.Label(self, textvariable=self.infoStr, bg='white', fg='black', width = 35, height = 10).place(x = 500, y = 70)

        tk.Label(self, text='Current player:', fg='black', width = 35, height = 1).place(x = 500, y = 265)
        tk.Label(self, textvariable=self.curTurnUsername, bg='white', fg='black', width = 35, height = 1 ).place(x = 500, y = 285)
        tk.Label(self, text='Your name:',  fg='black', width = 35, height = 1 ).place(x = 500, y = 320)
        
        e = tk.Entry(self, show=None, textvariable=self.inputUsername, width=35)
        e.place(x = 500, y = 340)

        tk.Button(self, text = 'Quit', command=self.master.destroy).place(x = 600, y = 400)


    def boardClick(self, event):
        col = int(event.x//133)
        row = int(event.y//133)
        self.clickCall(row, col)

    def clearBoard(self):
        self.canvas.destroy()
        self.initCanvas()

    def putTo(self, row, col, piece):
        c_x = int(133*col + 133/2)
        c_y = int(133*row + 133/2)
        if piece == 'o':
            self.canvas.create_oval(c_x-50, c_y-50, c_x+50, c_y+50, width=4)
        else:
            self.canvas.create_line(c_x-50, c_y-50, c_x+50, c_y+50, width=4)
            self.canvas.create_line(c_x-50, c_y+50, c_x+50, c_y-50, width=4)
    
    def getUsername(self):
        return self.inputUsername.get()

    def setClickCall(self, callable):
        self.clickCall = callable
