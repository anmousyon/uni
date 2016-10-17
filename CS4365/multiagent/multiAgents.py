# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index, score in enumerate(scores) if score == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldPos = currentGameState.getPacmanPosition()
        pellets = currentGameState.getCapsules()

        evaluation = -currentGameState.getScore()

        if newPos == oldPos:
            evaluation -= 10

        num_pellets = len(pellets)
        num_ghosts = len(newGhostStates)
        grid_size = newFood.width*newFood.height
        num_food = newFood.count(True)
        if num_food == 0:
            return 100000

        for foodx, row in enumerate(newFood):
            for foody, col in enumerate(row):
                if col:
                    old_dist = util.manhattanDistance(oldPos, (foodx, foody))
                    new_dist = util.manhattanDistance(newPos, (foodx, foody))
                    if new_dist <= grid_size/(num_food+1):
                        dist = new_dist if new_dist else old_dist
                        evaluation += (old_dist-new_dist) * (grid_size/(dist*num_food))

        for pellet_pos in pellets:
            old_dist = util.manhattanDistance(oldPos, pellet_pos)
            new_dist = util.manhattanDistance(newPos, pellet_pos)
            if new_dist <= grid_size/(num_pellets+(num_food+1)):
                dist = new_dist if new_dist else old_dist
                evaluation += (old_dist-new_dist) * (grid_size/(num_pellets*dist))

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            old_dist = util.manhattanDistance(oldPos, ghostPos)
            new_dist = util.manhattanDistance(newPos, ghostPos)
            if new_dist <= grid_size/(num_ghosts+(num_food+1)):
                dist = new_dist if new_dist else old_dist
                evaluater = (old_dist-new_dist) * (grid_size/(num_ghosts*dist))
                if ghost.scaredTimer > 1:
                    evaluation += evaluater
                else:
                    evaluation -= evaluater

        return evaluation + successorGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        agents = gameState.getNumAgents()

        def minimax(state, depth):
            if depth == self.depth*agents:
                return (None, self.evaluationFunction(state))
            agent = depth%agents
            if agent:
                return minormax(state, depth, agent, 1)
            else:
                return minormax(state, depth, agent, -1)

        def minormax(state, depth, agent, mom):
            best = (None, (float('inf') * mom))
            actions = state.getLegalActions(agent)
            if not actions:
                return (None, self.evaluationFunction(state))
            for action in actions:
                child = state.generateSuccessor(agent, action)
                result = minimax(child, depth+1)
                if mom > 0:
                    if result[1] < best[1]:
                        best = (action, result[1])
                else:
                    if result[1] > best[1]:
                        best = (action, result[1])
            return best

        return minimax(gameState, 0)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """ 
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()

        def minimax(state, depth, alpha, beta):
            if depth == self.depth*agents:
                return (None, self.evaluationFunction(state))
            agent = depth%agents
            if agent:
                return minormax(state, depth, agent, 1, alpha, beta)
            else:
                return minormax(state, depth, agent, -1, alpha, beta)

        def minormax(state, depth, agent, mom, alpha, beta):
            best = (None, (float('inf') * mom))
            actions = state.getLegalActions(agent)
            if not actions:
                return (None, self.evaluationFunction(state))
            for action in actions:
                child = state.generateSuccessor(agent, action)
                result = minimax(child, depth+1, alpha, beta)
                if mom > 0:
                    if result[1] < best[1]:
                        best = (action, result[1])
                    if best[1] < alpha:
                        return best
                    beta = min(beta, best[1])
                else:
                    if result[1] > best[1]:
                        best = (action, result[1])
                    if best[1] > beta:
                        return best
                    alpha = max(best[1], alpha)
            return best

        return minimax(gameState, 0, -float('inf'), float('inf'))[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()

        def minimax(state, depth):
            if depth == self.depth*agents:
                return (None, self.evaluationFunction(state))
            agent = depth%agents
            if agent:
                return expormax(state, depth, agent, 0)
            else:
                return expormax(state, depth, agent, -1)

        def expormax(state, depth, agent, mom):
            best = (None, (float('inf') * mom))
            exp = 0
            actions = state.getLegalActions(agent)
            if not actions:
                return (None, self.evaluationFunction(state))
            prob = 1.0/len(actions)
            for action in actions:
                child = state.generateSuccessor(agent, action)
                result = minimax(child, depth+1)
                if mom >= 0:
                    exp += result[1] * prob
                else:
                    if result[1] > best[1]:
                        best = (action, result[1])
            return best if abs(mom) else (None, exp)

        return minimax(gameState, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
        I get the current score that I start at and all the information I need
        I take any possible chance to win (setting evaluation super high)
        I am comparing the current position to the location of all the food, pellets and ghosts
        I subtract the amount of food from the evaluation so that large amounts of food dont overpower the ghost weights
        then I am doing a weighted addition to the evaluation based on those distances
        then I am dividing by the amount of food left
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()    
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghost.scaredTimer for ghost in ghostStates]
    pellets = currentGameState.getCapsules()

    evaluation = currentGameState.getScore()

    num_ghosts = len(ghostStates)
    num_food = food.count(True)
    if num_food == 0:
        return 100000

    grid_size = food.width*food.height
    for foodx, row in enumerate(food):
        for foody, col in enumerate(row):
            if col:
                food_dist = util.manhattanDistance(pos, (foodx, foody))
                if food_dist <= grid_size/(num_food*num_ghosts):
                    if food_dist:
                        evaluater = abs(grid_size/(food_dist*num_food))
                    else:
                        evaluater = 1000
                    evaluation += evaluater

    evaluation -= num_food

    num_pellets = len(pellets)
    for pellet_pos in pellets:
        pellet_dist = util.manhattanDistance(pos, pellet_pos)
        if pellet_dist <= grid_size/(num_food*num_pellets):
            if pellet_dist:
                evaluater = abs(grid_size/(num_pellets*pellet_dist))
            else:
                evaluater = abs(grid_size/(num_pellets*1))
            evaluation += evaluater

    for ghost in ghostStates:
        ghost_pos = ghost.getPosition()
        ghost_dist = util.manhattanDistance(pos, ghost_pos)
        if ghost_dist <= grid_size/(num_food*num_ghosts):
            if ghost_dist:
                evaluater = abs(grid_size/(num_ghosts*ghost_dist))
            else:
                evaluater = 10000

            if ghost.scaredTimer > 1:
                evaluation += evaluater
            else:
                evaluation -= evaluater
    return evaluation/num_food
# Abbreviation
better = betterEvaluationFunction
