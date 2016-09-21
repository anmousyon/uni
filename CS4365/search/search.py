# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

from game import Directions
dirs = {
    (0, -1): Directions.SOUTH,
    (0, 1): Directions.NORTH,
    (1, 0): Directions.EAST,
    (-1, 0): Directions.WEST,
    (0, 0): Directions.STOP
}

def get_goal(problem):
    def  dfs(problem, start):
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                new = set([x[0] for x in problem.getSuccessors(vertex)])
                stack.extend(new - visited)
        return visited
    goal = None
    for x in dfs(problem, problem.getStartState()):
        if problem.isGoalState(x):
            goal = x
    return goal

def get_actions(path):
    current = path[0]
    path.remove(path[0])
    actions = []
    for action in path:
        w, x = current
        y, z = action
        direction = dirs[(y-w, z-x)]
        actions.append(direction)
        current = action
    actions.append(dirs[(0,0)])
    return actions

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    goal = get_goal(problem)

    def dfs_path(problem, start, goal):
        stack = [(start, [start])]
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                new = list(set([x[0] for x in problem.getSuccessors(vertex)]))
                for nexts in new:
                    stack.append((nexts, path+[nexts]))

    return get_actions(dfs_path(problem, problem.getStartState(), goal))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    goal = get_goal(problem)

    def bfs_paths(problem, start, goal):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            new = set([x[0] for x in problem.getSuccessors(vertex)])
            for next in list(set(new) - set(path)):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))
    def sp(problem, start, goal):
        try:
            return next(bfs_paths(problem, start, goal))
        except StopIteration:
            return None
    return get_actions(sp(problem, problem.getStartState(), goal))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    goal = get_goal(problem)
    def ucs(problem):
        node = problem.getStartState(problem)
        frontier = util.PriorityQueue()
        frontier.push(node)
        explored = []
        while True:
            if frontier.isEmpty():
                return False
            node = frontier.pop()
            if node.state == goal:
                return #path
            explored.append(node.state)
            new = set([x[0] for x in problem.getSuccessors(node.state)])
            for next in new - explored:
                child = node(problem, node, set([x[0] for x in problem.getSuccessors(node.state)]))
                if not child.state in explored and not child.state in frontier:
                    frontier.push(child)
                elif child.state in frontier and child.cost > node.cost:
                    node = child

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
