class Player:
  def __init__(self, id):
    self.id = id

  def play(self):
    pass

class LineChecker:

  def __init__(self, _id, board, width, height):
    self.board = board
    self._id = _id
    self.WIDTH = width
    self.HEIGHT = height

  def check(self):
    for c in range(self.WIDTH):
      for r in range(self.HEIGHT):
        if self.checkHorizontal(c, r) or self.checkVertical(c, r) or self.checkUpperDiagonal(c, r) or self.checkLowerDiagonal(c, r):
          return True

    return False

  def checkHorizontal(self, c, r):
    if c < self.WIDTH - 3:
      return self.board[c][r] == self.board[c + 1][r] == self.board[c + 2][r] == self.board[c + 3][r] == self._id
    return False

  def checkVertical(self, c, r):
    if r < self.HEIGHT - 3:
      return self.board[c][r] == self.board[c][r + 1] == self.board[c][r + 2] == self.board[c][r + 3] == self._id
    return False

  def checkUpperDiagonal(self, c, r):
    if c < self.WIDTH - 3 and r < self.HEIGHT - 3:
      return self.board[c][r] == self.board[c + 1][r + 1] == self.board[c + 2][r + 2] == self.board[c + 3][r + 3] == self._id
    return False

  def checkLowerDiagonal(self, c, r):
    if c >= 3 and r < self.HEIGHT - 3:
      return self.board[c][r] == self.board[c - 1][r + 1] == self.board[c - 2][r + 2] == self.board[c - 3][r + 3] == self._id
    return False  


class ConnectFourBoard:

  def __init__(self, width, height):
    self.WIDTH = width
    self.HEIGHT = height
    self.board = [[0 for y in range(height)]for x in range (width)]

  def place(self, column, id):
    """ Given the player and the column of the play, put a tile in the board """
    for i in range(self.HEIGHT):
      if self.board[column][i] == 0:
        self.board[column][i] = id
        break

  def canPlace(self, column):
    return self.board[column][-1] == 0

  def isEmpty(self, column):
    for i in self.board:
      for c in i:
        if c != 0:
          return False
    return True

  def remove(self, column, player):
    for i in range(self.HEIGHT):
      if self.board[column][self.HEIGHT - i - 1] != 0:
        self.board[column][self.HEIGHT - i - 1] = 0
        break

  def printGame(self):
    print("\n")
    for r in range(self.HEIGHT):
      print(r, end="| ")
      for c in range(self.WIDTH):
        print(self.mapChar(self.board[c][self.HEIGHT - r - 1]), end= " ")
      print("")
    print(" ", end="| ")
    for c in range(self.WIDTH):
      print("_", end=" ")
    print("")


    print(" ", end="  ")
    for c in range(self.WIDTH):
      print(str(c), end=" ")
    print("")

  def mapChar(self, inpt):
    if inpt == 0:
      return " "
    elif inpt == 1:
      return "X"
    elif inpt == 2:
      return "O"

  def isGameOver(self):
    return self.won(1) or self.won(2) or self.isTie()

  def won(self, _id):
    checker = LineChecker(_id, self.board, self.WIDTH, self.HEIGHT)
    return checker.check()

  def isTie(self):
    for col in self.board:
      for e in col:
        if e == 0:
          return False
    return True


class ConnectFour:

  def __init__(self, width, height):
    self.board = ConnectFourBoard(width, height)
    self.width = width
    self.height = height

  def getPlayerOne(self, id):
    return Player(id)

  def getPlayerTwo(self, id):
    return Player(id)

  def isGameOver(self):
    return self.board.isGameOver()

  def onGameOver(self):
    if (self.board.won(1)):
      print("Player ", 1, " won!!")
    elif (self.board.won(2)):
      print("Player ", 2, " won!!")
    else:
      print("Its a tie !!")

  def playerPlay(self, player):
    from copy import deepcopy
    board = deepcopy(self.board.board)

    self.board.printGame()
    selectedColumn = player.play(board)
    self.board.place(selectedColumn, player.id)

    return self.isGameOver()


  def play(self):
    playerOne = self.getPlayerOne(1)
    playerTwo = self.getPlayerTwo(2)

    while not (self.playerPlay(playerOne) or self.playerPlay(playerTwo)):
      pass

    self.board.printGame()
    self.onGameOver()


class GameState:
  def isTerminal(self):
    """ Returns True if the state is terminal, False otherwise """
    raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

  def getActionSuccessors(self, id):
    """ Return a list of the action taken and the successor for such action 

    For instance, let's say that actions are defined as a number from [0,3] and
    a successor is a game state in the form of a list of 4 elements with values
    'x', 'o', or 'b'

    Self is: ['b', 'b', 'b', 'b', 'b']
    Returns: 
      [
        (0, ['x', 'b', 'b', 'b']),
        (1, ['b', 'x', 'b', 'b']),
        (2, ['b', 'b', 'x', 'b']),
        (3, ['b', 'b', 'b', 'x'])
      ]

    Of course, any subclass would need to know if the successor is being filled with
    an 'x' or a 'o'. This should probably be stored in an instance variable and modified
    accordingly.

    Note that any class that calls this method will only care about the state but shouldn't
    be able to modify it. So state instances could be shared in order to optimize the algorithm
    if need be. 
    """
    raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))


class ConnectFourGameState(GameState):

  def __init__(self, width, height, board):
    self.board = ConnectFourBoard(width, height)
    self.board.board = board

  def isTerminal(self):
    return self.board.isGameOver()

  def getActionSuccessors(self, _id):
    for i in [3, 4, 2, 1, 5, 6, 0]:
      if self.board.canPlace(i):
        self.board.place(i, _id)
        yield (i, self)
        self.board.remove(i, _id)

  def size(self):
    acc = 0
    for i in self.board.board: 
      for e in i:
        if e != 0:
          acc += 1
    return acc

class BoundedMiniMax:

  def __init__(self, depth, id, opponent):
    self.MAX_DEPTH = depth
    self.id = id
    self.opponent = opponent

  def successorsScores(self, state, currentDepth, isMinimizer):
    """ Returns the score of each state in states.

    The 'score' is the result of evaluate() in each state.
    """
    scores = []
    for _, next in state.getActionSuccessors(self.id if not isMinimizer else self.opponent):
      scores.append(self.minimax(next, currentDepth + 1, not isMinimizer))
    return scores

  def minimax(self, state, currentDepth, isMinimizer):
    """ Performs a bounded MiniMax Algorithm. """
    if state.isTerminal():
      return self.evaluate(state, currentDepth)
    elif currentDepth == self.MAX_DEPTH:
      return self.evaluate(state, currentDepth)
    elif isMinimizer:
      return min(self.successorsScores(state, currentDepth, isMinimizer))
    else:
      return max(self.successorsScores(state, currentDepth, isMinimizer))

  def run(self, originalState):
    """ Call this method to run minmax on the given state.

    Returns:
    The next action to be taken. (I.e. the next move to play.)
    """
    nextAction = None
    nextScore = float("-inf")
    for action, state in originalState.getActionSuccessors(self.id):
      # Since the opponent is the minimizer, and we are making one move already
      # minmax should be called assuming that is the opponents (minimizer) turn.
      score = self.minimax(state, 1, True)
      if (score > nextScore):
        nextScore = score
        nextAction = action
    return nextAction

  def evaluate(self, state, depth):
    pass

class AlphaBetaMiniMax(BoundedMiniMax):
  def __init__(self, depth, _id, opponent):
    BoundedMiniMax.__init__(self, depth, _id, opponent)
    self.c = 1

  def successorsScores(self, state, currentDepth, isMinimizer, alpha, beta):
    """ Returns the score of each state in states.

    The 'score' is the result of evaluate() in each state.
    """
    raise NotImplementedError()

  def minimax(self, state, currentDepth, isMinimizer, alpha, beta):
    if state.isTerminal():
      score = self.evaluate(state, currentDepth)
      return (score, alpha, beta)
    elif currentDepth == self.MAX_DEPTH:
      score = self.evaluate(state, currentDepth)
      return (score, alpha, beta)

    v = float("-inf") if not isMinimizer else float("inf")
    s = False
    for action, next in state.getActionSuccessors(self.id if not isMinimizer else self.opponent):
      if not s: 
        score = self.minimax(next, currentDepth + 1, not isMinimizer, alpha, beta)[0]
        if not isMinimizer:
          v = max(v, score)
          alpha = max(v, alpha)
          if beta <= alpha:
            s = True
    
        else: 
          v = min(v, score)
          beta = min(beta, v)
          if beta <= alpha:
            s = True  
    return (v, alpha, beta)

  def run(self, originalState):
    nextAction = None
    v = float("-inf")

    nextAction = None
    alpha = float("-inf")
    beta = float("inf")
    s = False
    for action, state in originalState.getActionSuccessors(self.id):
      # Since the opponent is the minimizer, and we are making one move already
      # minmax should be called assuming that is the opponents (minimizer) turn.
      if not s: 
        score, alpha2, beta2 = self.minimax(state, 1, True, alpha, beta)
        if score > v:
          v = score
          nextAction = action
        v = max(v, score)
        alpha = max(v, alpha2)
    self.c += 2

    return nextAction

class ConnectFourMiniMax(AlphaBetaMiniMax):



  def __init__(self, MAX_DEPTH, _id, opponent):
    AlphaBetaMiniMax.__init__(self, MAX_DEPTH, _id, opponent)
    self._id = _id
    self.opponent = opponent
    self.TABLE = [[3, 4, 5, 5, 4, 3], [4, 6, 8, 8, 6, 4], [5, 8, 11, 11, 8, 5], [7, 10, 13, 13, 10, 7], \
                  [5, 8, 11, 11, 8, 5], [4, 6, 8, 8, 6, 5], [3, 4, 5, 5, 4, 3]] 

  def evaluate(self, state, depth):
    checker = LineChecker(self._id, state.board.board, state.board.WIDTH, state.board.HEIGHT)
    if checker.check(): 
      return 1000 - depth
    checker = LineChecker(self.opponent, state.board.board, state.board.WIDTH, state.board.HEIGHT)
    if checker.check():
      return - 1000 - depth
    acc = 0
    for c in range(state.board.WIDTH):
      for r in range(state.board.HEIGHT):
        if state.board.board[c][r] == self._id:
          acc += self.TABLE[c][r]
        elif state.board.board[c][r] == self.opponent:
          acc -= self.TABLE[c][r]

    return acc    

class MiniMaxPlayer(Player):
  def __init__(self, _id, width, height):
    Player.__init__(self, _id)
    DEPTH = 6
    self.minimax = ConnectFourMiniMax(DEPTH, _id, 2 if _id == 1 else 1)
    self.width = width
    self.height = height

  def play(self, board):
    state = ConnectFourGameState(self.width, self.height, board)
    return self.minimax.run(state)

class ConsolePlayer(Player):
  def __init__(self, id):
    Player.__init__(self, id)

  def play(self, board):
    v = int(input("Select the column [1-7]: "))
    return v

class ConnectFourDFS():

  def __init__(self, _id):
    self._id = _id

  def playOnBoard(self,board,posX,player):
      if posX > 6:
          return False

      for y in range (5,-1,-1):
          if board[posX][y] == 0:
              if player == 1:
                  board[posX][y] = "X"
              else:
                  board[posX][y] = "O"
              return True

      return False

  def checkWinBot(self,board,symbol):
      lineSize = 0

      #revisan filas
      for y in range (0,6):
          for x in range (0,7):
              if board[x][y] == symbol:
                  lineSize += 1
              else:
                  lineSize = 0
              if lineSize == 4:
                  return True
          lineSize = 0

      #revisan columnas
      for x in range (0,7):
          for y in range (0,6):
              if board[x][y] == symbol:
                  lineSize += 1
              else:
                  lineSize = 0
              if lineSize == 4:
                  return True
          lineSize = 0

      #revisan diagonales
      diagonals = [[0,3,4],[0,4,5],[0,5,6],[0,6,6],[1,6,5],[2,6,4]]

      for i in range (0,6):
          y = diagonals[i][0]
          x = diagonals[i][1]
          count = diagonals [i][2]
          for j in range (0,count):
              if board[x][y] == symbol:
                  lineSize += 1
              else:
                  lineSize = 0
              x -= 1
              y += 1
              if lineSize == 4:
                  return True
          lineSize = 0

      diagonals = [[2,0,4],[1,0,5],[0,0,6],[0,1,6],[0,2,5],[0,3,4]]

      for i in range (0,6):
          y = diagonals[i][0]
          x = diagonals[i][1]
          count = diagonals [i][2]
          for j in range (0,count):
              if board[x][y] == symbol:
                  lineSize += 1
              else:
                  lineSize = 0
              x += 1
              y += 1
              if lineSize == 4:
                  return True
          lineSize = 0
      return False

  #funcion para revisar si hay empate
  def checkTie(self,board):
      spaces = 0
      for x in range (0,7):
          for y in range (0,6):
              if board[x][y] == 0:
                  spaces += 1
      if spaces == 0:
          return True
      else:
          return False

  def run(self, board):
      queue = []
      state = 0

      if self._id == 0:
          originalSymbol = "X"
          rivalSymbol = "O"
      else:
          originalSymbol = "O"
          rivalSymbol = "X"

      originalPlayer = self._id

      #se hacen los posibles hijos (movimientos) del estado actual
      for i in range (0,7):
          from copy import deepcopy
          state = deepcopy(board)

          if self.playOnBoard(state,i,originalPlayer):
              queue.insert(0,state)

          originalState = deepcopy(state)
          column = i

          finish = False

          #mientras siga habiendo hijos se sigue buscando un estado de victoria
          while queue:
              #si se llega a victoria dle rival se deshecha el estado
              if self.checkWinBot(state,rivalSymbol) == True:
                  state = queue.pop(0)
              #si se llega al estado de victoria se regresa al movimiento original
              elif self.checkWinBot(state,originalSymbol) == True:
                  finish = True
                  break
              #si no hay victoria alguna de hace el movimiento del rival
              else:
                  opponentTurn = False
                  #movimiento aleatorio del rival
                  while opponentTurn == False:
                      from random import randint
                      opponentChip = randint(0,6)
                      if self._id == 1:
                          opponentTurn = self.playOnBoard (state,opponentChip,1)
                          #se revisa si se hace un empate para ignorar el estado
                          if self.checkTie(state):
                              break
                      else:
                          #se revisa si se hace un empate para ignorar el estado
                          opponentTurn = self.playOnBoard (state,opponentChip,0)
                          if self.checkTie(state):
                              break
                  state2 = 0
                  #se crean los hijos del estado actual con los movimientos posibles
                  for i in range (0,7):
                      from copy import deepcopy
                      state2 = deepcopy(state)
                      if self.playOnBoard(state2,i,self._id):
                          queue.insert(0,state2)
                  state = queue.pop(0)

          #se regresa el estado (movimiento) siguiente
          if finish == True:
              return column

      return column

class DFSPlayer(Player):
    def __init__(self, id):
      Player.__init__(self, id)
      self.dfs = ConnectFourDFS(id)

    def play(self, board):
      v = self.dfs.run(board)
      return v

class MiConnectFour(ConnectFour):
  def __init__(self, width, height, playerOne, playerTwo):
    ConnectFour.__init__(self, width, height)
    self.playerOne = playerOne
    self.playerTwo = playerTwo

  def getPlayerOne(self, _id):
    self.playerOne.id = _id
    return self.playerOne

  def getPlayerTwo(self, _id):
    self.playerTwo.id = _id
    return self.playerTwo

def main():
  from optparse import OptionParser

  usage = "usage: %prog [options]"
  parser = OptionParser(usage=usage)
  parser.add_option("-1", "--one", dest="one", type="string", default="",
    help="Set the player one type: informed")
  parser.add_option("-2", "--two", dest="two", type="string", default="",
    help="Set the player one type: informed or notinformed")
  options, args = parser.parse_args()

  WIDTH = 7
  HEIGHT = 6

  playerOne = ConsolePlayer("1")
  playerTwo = ConsolePlayer("2")

  if options.one == "informed":
    playerOne = MiniMaxPlayer("1", WIDTH, HEIGHT)
    
  if options.two == "informed":
    playerTwo = MiniMaxPlayer("2", WIDTH, HEIGHT)
  elif options.two == "notinformed":
    playerTwo = DFSPlayer("2")


  conectaTec = MiConnectFour(WIDTH, HEIGHT, playerOne, playerTwo)
  conectaTec.play()


if __name__ == '__main__':
  main()