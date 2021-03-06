# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        print legalMoves

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        print scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currGameState, pacManAction):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        nextGameState = currGameState.generatePacmanSuccessor(pacManAction)
        # print nextGameState
        newPos = nextGameState.getPacmanPosition()
        # print newPos
        oldFood = currGameState.getFood()
        # print currGameState
        # print oldFood
        newGhostStates = nextGameState.getGhostStates()
        # print newGhostStates[0]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print newScaredTimes

        "*** YOUR CODE HERE ***"
        totalScore = 0.0
        for ghost in newGhostStates:
            d = manhattanDistance(ghost.getPosition(), newPos)
            if (d <= 1):
                if (ghost.scaredTimer != 0):
                    totalScore += 2000
                else:
                    # if ghost in that direction is very near, will not go that direction
                    totalScore -= 200

        for capsule in currGameState.getCapsules():
            d = manhattanDistance(capsule, newPos)
            if (d == 0):
                totalScore += 100
            else:
                totalScore += 10.0 / d

        # every time, pacman will move to a direction with most probability of food by 1/(x^2) distribution
        for x in xrange(oldFood.width):
            for y in xrange(oldFood.height):
                if (oldFood[x][y]):
                    d = manhattanDistance((x, y), newPos)
                    if (d == 0):
                        totalScore += 100
                    else:
                        totalScore += 1.0 / (d * d)
        return totalScore
        # return nextGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='betterEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, currGameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          currGameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          Directions.STOP:
            The stop direction, which is always legal

          currGameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          currGameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        legalMoves = currGameState.getLegalActions(0)
        maxValue = float('-Inf')
        chosenMove = ''
        # choose a move that maximizing minFunc
        for move in legalMoves:
            currentDepth = 0
            currentMax = self.minFunc(currGameState.generateSuccessor(0, move), currentDepth, 1)
            if currentMax > maxValue:
                maxValue = currentMax
                chosenMove = move
        return chosenMove

    def maxFunc(self, currGameState, depth):
        # goal test
        depth = depth + 1
        if currGameState.isWin() or currGameState.isLose() or depth == self.depth:
            return self.evaluationFunction(currGameState)

        v = float('-Inf')
        for move in currGameState.getLegalActions(0):
            v = max(v, self.minFunc(currGameState.generateSuccessor(0, move), depth, 1))
        return v

    def minFunc(self, currGameState, depth, agentNumber):
        # goal test
        if currGameState.isWin() or currGameState.isLose():
            return self.evaluationFunction(currGameState)

        v = float('Inf')
        for move in currGameState.getLegalActions(agentNumber):
            if agentNumber == currGameState.getNumAgents() - 1:
                v = min(v, self.maxFunc(currGameState.generateSuccessor(agentNumber, move), depth))
            else:
                v = min(v, self.minFunc(currGameState.generateSuccessor(agentNumber, move), depth, agentNumber + 1))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, currGameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = currGameState.getLegalActions(0)
        maxValue = float('-Inf')
        alpha = float('-Inf')
        beta = float('Inf')
        chosenMove = ''
        # choose a move that maximizing minFunc
        for move in legalMoves:
            currentDepth = 0
            currentMax = self.minFunc(currGameState.generateSuccessor(0, move), alpha, beta, currentDepth, 1)
            if currentMax > maxValue:
                maxValue = currentMax
                chosenMove = move
        return chosenMove

    def maxFunc(self, currGameState, alpha, beta, depth):
        # goal test
        depth = depth + 1
        if currGameState.isWin() or currGameState.isLose() or depth == self.depth:
            return self.evaluationFunction(currGameState)

        v = float('-Inf')
        for move in currGameState.getLegalActions(0):
            v = max(v, self.minFunc(currGameState.generateSuccessor(0, move), alpha, beta, depth, 1))
            if v >= beta:
                return v;
            alpha = max(alpha, v)
        return v

    def minFunc(self, currGameState, alpha, beta, depth, agentNumber):
        # goal test
        if currGameState.isWin() or currGameState.isLose():
            return self.evaluationFunction(currGameState)

        v = float('Inf')
        for move in currGameState.getLegalActions(agentNumber):
            if agentNumber == currGameState.getNumAgents() - 1:
                v = min(v, self.maxFunc(currGameState.generateSuccessor(agentNumber, move), alpha, beta, depth))
            else:
                v = min(v, self.minFunc(currGameState.generateSuccessor(agentNumber, move), alpha, beta, depth, agentNumber + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, currGameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    #get the ghosts' states
    ghostStates = [gameState for gameState in currentGameState.getGhostStates()]
    #get the ghosts' positions
    ghostPositionList = [ gameState.getPosition() for gameState in ghostStates]
    #get the coordinates of current food
    foodList = currentGameState.getFood().asList()
    #get pacman's position
    pacmanPosition = currentGameState.getPacmanPosition()
    #get the times of pellet
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    distToFood = 0.0001
    foodWeight = 20
    ghostWeight = -0.5
    currentScore = currentGameState.getScore()
    powerPelletFactor = 0

    #get the sum of distance from pacman to nearer ghost and the distance between two ghosts
    distToGhost = minDistanceToGoal(pacmanPosition,ghostPositionList)

    #calculate the distance between each food to pacman
    foodToPacmanDistList = []
    for food in foodList:
        foodToPacmanDistList.append(manhattanDistance(food,pacmanPosition))

    #sort the distance
    foodToPacmanDistList.sort(cmp=None, key=None, reverse=False)

    #count the k nearest food's distances to pacman and sum them up
    knn = 4

    if len(foodToPacmanDistList) < knn:
        knn = len(foodToPacmanDistList)

    for i in range(knn):
        distToFood += foodToPacmanDistList[i]

    #if the power pellet is actived, the pacman is the most powerful agent
    if newScaredTimes[0] != 0 :
        powerPelletFactor = 999999
    return currentScore + 1.0/distToFood * foodWeight + powerPelletFactor + distToGhost * ghostWeight

def minDistanceToGoal(pacmanPosition, foodList):
    xy1 = pacmanPosition
    distance = 0.0

    if(len(foodList) == 0):
      return distance

    #calculate which food is the nearest one to the pacman
    minDistanceFood = foodList[0]
    minDistanceToFood =  abs(xy1[0] - minDistanceFood[0]) + abs(xy1[1] - minDistanceFood[1])

    for food in foodList:
        xy2 = food
        tmpDistance =  abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
        if(tmpDistance < minDistanceToFood):
            minDistanceToFood = tmpDistance
            minDistanceFood = xy2

    foodList.remove(minDistanceFood)


    #calculate which food is the nearest to the minDistanceFood,for example, FoodA
    #then, calculate which food is the nearest food to FoodA, and so on...
    while len(foodList)>0:
        dist = 999999
        fd = []
        for food in foodList:
            tmpDist = abs(food[0]-minDistanceFood[0]) + abs(food[1]-minDistanceFood[1])
            if(dist > tmpDist):
                dist = tmpDist
                fd = food
        minDistanceToFood += dist
        minDistanceFood = fd
        foodList.remove(fd)

    return minDistanceToFood

# Abbreviation
better = betterEvaluationFunction
