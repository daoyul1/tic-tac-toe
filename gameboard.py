class BoardClass:
    def __init__(self, piece, user1, user2):
        self.username = user1
        self.rivalname = user2
        self.lastTurnUsername = ''
        self.numOfPlay = 0
        self.numOfWins = 0
        self.numOfTies = 0
        self.numOfLosses = 0

        self.piece = piece

        self.status = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

    def updateGamesPlayed(self):
        self.numOfPlay += 1

    def resetGameBoard(self):
        self.status = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

    def updateGameBoard(self, row, col, piece):
        if self.status[row][col] != '.':
            return False
        self.status[row][col] = piece
        return True

    def isWinner(self):
        allPossible = []
        for i in range(3):
            allPossible.append(''.join(self.status[i]))
            allPossible.append(''.join(j[i] for j in self.status))
        allPossible.append(''.join(self.status[i][i] for i in range(3)))
        allPossible.append(''.join(self.status[i][2-i] for i in range(3)))

        winner = '.'
        for pattern in allPossible:
            if pattern[0] == pattern[1] and pattern[0] == pattern[2] and pattern[0] != '.':
                winner = pattern[0]
                break

        if winner != '.':
            if winner == self.piece:
                self.numOfWins += 1
            else:
                self.numOfLosses += 1
        return winner

    def boardIsFull(self):
        isFull = True
        for i in range(3):
            for j in range(3):
                if self.status[i][j] == '.':
                    isFull = False

        if isFull:
            self.numOfTies += 1
        return isFull

    def printStats(self, lastmv):
        s = '''
        Username:\t%s
        Last move:\t%s
        Num of games:\t%d
        Num of wins:\t%d
        Num of losses:\t%d
        Num of ties:\t%d
        ''' % (self.username, lastmv, self.numOfPlay, self.numOfWins, self.numOfLosses, self.numOfTies)
        print('----------------------------------------------')
        print(s)
        print('----------------------------------------------')

            # b = BoardClass()
            # b.isWinner()
