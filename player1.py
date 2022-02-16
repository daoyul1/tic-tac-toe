from UI import UI
from gameboard import BoardClass
import tkinter as tk
import tkinter.messagebox as messagebox
import socket
import threading

class Player1:
    def __init__(self):
        self.piece = 'x'
        self.username = ''
        self.user2 = ''

        self.ui = UI(self.piece)

        self.s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.ip   = tk.StringVar()
        self.port = tk.StringVar()
        self.ip.set('127.0.0.1')
        self.port.set('9999')

        self.isConnect = False

        self.prompt()
        self.board = None

        self.ui.setClickCall(self.callWhenClick)
        self.yourturn = True
        self.lastmv = '?'

        self.t = threading.Thread(target=self.tcpLink, args=())
        self.t.setDaemon(1)


    def showStats(self, lastmv):
        self.ui.infoStr.set('''
            Username:\t%s
            Last move:\t%s
            Number of games:\t%d
            Number of wins:\t%d
            Number of losses:\t%d
            Number of ties:\t%d
        '''%(self.username, lastmv, self.board.numOfPlay, self.board.numOfWins, self.board.numOfLosses, self.board.numOfTies))

    def playAgain(self):
        message='Do you want to play again?'
        answer = messagebox.askyesno(title='Play again?', message=message)
        if answer:
            self.board.updateGamesPlayed()
            self.board.resetGameBoard()
            self.ui.clearBoard()
            self.s.send(b'Play Again')
            self.yourturn = True
            self.ui.curTurnUsername.set(self.username)
            self.showStats(self.lastmv)
        else:
            self.s.send(b'Fun Times')
            self.ui.master.destroy()

    def tcpLink(self):
        while 1:
            try:
                data = self.s.recv(1024)
                data = data.decode('utf8')
            except:
                pass
            if data[:2] == 'un':
                self.user2 = data[2:]
                self.play()
            elif data[:2] == 'mv':
                row = int(data[2])
                col = int(data[3])
                piece = data[4]

                self.ui.putTo(row,col,piece)
                self.board.updateGameBoard(row, col, piece)

                win = self.board.isWinner()
                if win == '.':
                    if self.board.boardIsFull():
                        self.playAgain()
                else:
                    self.playAgain()


                self.yourturn = 1
                self.lastmv = self.user2
                self.showStats(self.lastmv)
                self.ui.curTurnUsername.set(self.username)

    def callWhenClick(self, row, col):
        if not self.yourturn:
            return

        isValid = self.board.updateGameBoard(row, col, self.piece)
        if isValid:
            self.ui.putTo(row, col, self.piece)
            data = "mv%d%d%c"%(row,col,self.piece)
            self.s.send(data.encode('utf8'))
            self.yourturn = 0
            self.ui.curTurnUsername.set(self.user2)
            self.lastmv = self.username
            self.showStats(self.lastmv)

            win = self.board.isWinner()
            if win == '.':
                if self.board.boardIsFull():
                    self.playAgain()
            else:
                self.playAgain()

    def play(self):
        self.board = BoardClass(self.piece, self.username, self.user2)
        self.ui.curTurnUsername.set(self.username)
        self.showStats(self.lastmv)
        # self.ui.curTurnUsername.set(self.username)
    
    def run(self):
        self.ui.mainloop()

    def prompt(self):
        pmt = tk.Toplevel(self.ui.master)
        pmt.geometry('300x150')
        pmt.title('Host ip and port')
        tk.Label(pmt,text='IP address:').pack()
        tk.Entry(pmt,textvariable=self.ip,show=None).pack()
        tk.Label(pmt,text='Port:').pack()
        tk.Entry(pmt,textvariable=self.port,show=None).pack()

        def dumbPromptCall():
            ip, port = self.ip.get(), self.port.get()
            try:
                self.s.connect((ip, int(port)))
                self.isConnect = True
                pmt.destroy()
                self.username = self.ui.getUsername()
                self.s.send(b'un' + self.username.encode('utf8'))
                self.play()
                self.t.start()
            except:
                answer = messagebox.askyesno(title='Connection Failed', message='Cannot connect to the host, please try again.')
                if not answer:
                    self.ui.master.destroy()
        tk.Button(pmt, text='connect', command=dumbPromptCall).pack()

    

p1 = Player1()
p1.run()
if(p1.board):
    p1.board.printStats(p1.lastmv)
