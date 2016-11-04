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

def get_actions(path):
    dirs = {
        (0, -1): Directions.SOUTH,
        (0, 1): Directions.NORTH,
        (1, 0): Directions.EAST,
        (-1, 0): Directions.WEST,
        (0, 0): Directions.STOP
    }
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

def translate(path):
    dirs = {
        'South': Directions.SOUTH,
        'North': Directions.NORTH,
        'East': Directions.EAST,
        'West': Directions.WEST
    }
    actions = []
    for action in path:
        actions.append(dirs[action])
    actions.remove(actions[-1])
    actions.append(Directions.STOP)
    print 'actions', actions
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
    def dfs_path(problem, start):
        stack = util.Stack()
        stack.push((start, [start]))
        visited = set()
        while not stack.isEmpty():
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if problem.isGoalState(vertex):
                    return path
                visited.add(vertex)
                new = problem.getSuccessors(vertex)
                for x in new:
                    if x[0] in visited:
                        new.remove(x)
                for next in new:
                    stack.push((next[0], path+[next[1]]))

    actions = dfs_path(problem, problem.getStartState())
    actions.remove(actions[0])
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    def bfs_paths(problem, start):
        queue = util.Queue()
        queue.push((start, [start]))
        explored = []
        while not queue.isEmpty():
            (current, path) = queue.pop()
            new = problem.getSuccessors(current)
            for x in new:
                if x[0] in explored:
                    new.remove(x)
            for next in new:
                explored.append(next[0])
                if problem.isGoalState(next[0]):
                    yield path + [next[1]]
                else:
                    queue.push((next[0], path + [next[1]]))

    def sp(problem, start):
        try:
            return next(bfs_paths(problem, start))
        except StopIteration:
            print 'ERROR'
            return [start]
    
    def pfa(start, actions):
        dirs = {
            Directions.SOUTH: (0, -1),
            Directions.NORTH: (0, 1),
            Directions.EAST: (1, 0),
            Directions.WEST: (-1, 0),
            Directions.STOP: (0, 0)
        }
        print actions
        path = []
        for action in actions:
            x, y = start
            dx, dy = dirs[action]
            start = (x+dx, y+dy)
            path.append(start)
        return start

    start = problem.getStartState()
    goals = problem.isGoalState(start)
    actions = []
    total_path = []
    if goals:
        for goal in goals:
            new_actions = sp(problem, start)
            new_actions.remove(new_actions[0])        
            actions += new_actions
            start = pfa(start, new_actions)
    else:
        actions = sp(problem, problem.getStartState())
        actions.remove(actions[0])
    
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    def ucs(problem, start):
        frontier = util.PriorityQueue()
        frontier.push(start, 0)
        came_from = {}
        total_cost = {}
        came_from[start] = None
        total_cost[start] = 0
        explored = []
        goal = None

        while not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current[0]):
                goal = current[0]
                break
            if current != start:
                current_c = current[0]
            else:
                current_c = start
            new = problem.getSuccessors(current_c)
            for x in new:
                if x[0] in explored:
                    new.remove(x)
            for next in new:
                new_cost = total_cost[current_c] + next[2]
                explored.append(next[0])
                if not next[0] in total_cost or new_cost < total_cost[next[0]]:
                    explored.append(next[0])
                    total_cost[next[0]] = new_cost
                    priority = new_cost
                    frontier.push(next, priority)
                    if current != start:
                        came_from[next[0]] = [current[0], next[1]]
                    else:
                        came_from[next[0]] = [current, next[1]]
        return came_from, start, goal
    
    def path(came_from, start, goal):
        current = goal
        path = [goal]
        while current != start:
            path.append(came_from[current][1])
            current = came_from[current][0]
        path.reverse()
        path.remove(path[-1])
        return path

    start = problem.getStartState()

    came_from, start, goal = ucs(problem, start)

    return path(came_from, start, goal)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def a_star_search(problem, start):
        frontier = util.PriorityQueue()
        frontier.push(start, 0)
        came_from = {}
        total_cost = {}
        came_from[start] = start
        total_cost[start] = 0
        goal = None
        explored = []

        while not frontier.isEmpty():
            current = frontier.pop()
            if problem.isGoalState(current[0]):
                goal = current[0]
                break
            if current != start:
                current_c = current[0]
            else:
                current_c = start
            new = problem.getSuccessors(current_c)
            for x in new:
                if x[0] in explored:
                    new.remove(x)
            for next in new:
                new_cost = total_cost[current_c] + next[2]
                explored.append(next[0])
                if not next[0] in total_cost or new_cost < total_cost[next[0]]:
                    total_cost[next[0]] = new_cost
                    priority = new_cost + heuristic(next[0], problem)
                    frontier.push(next, priority)
                    if current != start:
                        came_from[next[0]] = [current[0], next[1]]
                    else:
                        came_from[next[0]] = [current, next[1]]
        return came_from, start, goal
    
    def path(came_from, start, goal):
        current = goal
        path = [goal]
        while current != start:
            path.append(came_from[current][1])
            current = came_from[current][0]
        path.reverse()
        path.remove(path[-1])
        return path

    start = problem.getStartState()
    test = problem.getSuccessors(start)
    goals = problem.isGoalState((100,100))
    total_path = []
    if goals:
        for goal in goals:
            came_from, start, goal = a_star_search(problem, start)
            total_path += path(came_from, start, goal)
            start = total_path[-1]
    else:
        came_from, start, goal = a_star_search(problem, start)
        return path(came_from, start, goal)
    
    return total_path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
