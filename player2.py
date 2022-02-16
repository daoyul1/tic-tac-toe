from UI import UI
from gameboard import BoardClass
import tkinter as tk
import tkinter.messagebox as messagebox
import socket
import threading

class Player2:
    def __init__(self):
        self.piece = 'o'
        self.username = 'player2'
        self.user2 = ''

        self.ui = UI(self.piece)

        self.s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.ip   = tk.StringVar()
        self.port = tk.StringVar()

        self.isConnect = False

        self.board = None

        self.ui.setClickCall(self.callWhenClick)
        self.yourturn = False
        self.lastmv = '?'

        self.s.bind(('127.0.0.1', 9999))
        self.s.listen(1)
        self.sock = None
        t = threading.Thread(target=self.tcpLink, args=())
        t.setDaemon(1)
        t.start()

    def showStats(self, lastmv):
        self.ui.infoStr.set('''
            Username:\t%s
            Last move:\t%s
            Number of games:\t%d
            Number of wins:\t%d
            Number of losses:\t%d
            Number of ties:\t%d
        '''%(self.username, lastmv, self.board.numOfPlay, self.board.numOfWins, self.board.numOfLosses, self.board.numOfTies))

    def tcpLink(self):
        self.sock, _ = self.s.accept()
        while 1:
            try:
                data = self.sock.recv(1024)
                data = data.decode('utf8')
                if data[:2] == 'un':
                    self.user2 = data[2:]
                    self.play()
                    self.sock.send(b'un'+self.username.encode('utf8'))
                elif data[:2] == 'mv':
                    row = int(data[2])
                    col = int(data[3])
                    piece = data[4]
                    
                    self.ui.putTo(row,col,piece)
                    self.board.updateGameBoard(row, col, piece)

                    win = self.board.isWinner()
                    if win == '.':
                        self.board.boardIsFull()

                    self.yourturn = 1
                    self.ui.curTurnUsername.set(self.username)
                    self.lastmv = self.user2
                    self.showStats(self.lastmv)
                elif data == 'Play Again':
                    self.board.resetGameBoard()
                    self.board.updateGamesPlayed()
                    self.ui.clearBoard()
                    self.yourturn = 0
                    self.ui.curTurnUsername.set(self.user2)
                    self.showStats(self.lastmv)
                
                elif data == 'Fun Times':
                    self.board.printStats(self.lastmv)
                    self.s.close()
            except:
                pass


    def callWhenClick(self, row, col):
        if not self.yourturn:
            return
        isValid = self.board.updateGameBoard(row, col, self.piece)
        if isValid:
            self.ui.putTo(row, col, self.piece)
            data = "mv%d%d%c"%(row,col,self.piece)
            self.sock.send(data.encode('utf8'))
            
            
            self.yourturn = 0
            self.lastmv = self.username
            self.showStats(self.lastmv)
            self.ui.curTurnUsername.set(self.user2)

            win = self.board.isWinner()
            if win == '.':
                self.board.boardIsFull()

    def play(self):
        # self.username = self.ui.getUsername()
        self.board = BoardClass(self.piece, self.username, self.user2)
        self.ui.curTurnUsername.set(self.user2)
        self.showStats(self.lastmv)
        # self.ui.curTurnUsername.set(self.username)
    
    def run(self):
        self.ui.mainloop()

p1 = Player2()
p1.run()
