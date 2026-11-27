from itertools import islice
from .common import Node, child_node, solution


def DFS(problem, trace):
    frontier = [Node(problem.initial_state)]
    seen = {problem.initial_state}
    trace.append((None, tuple(item.state for item in islice(reversed(frontier), 6)), len(frontier)))
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            trace.append((node.state, tuple(item.state for item in islice(reversed(frontier), 6)), len(frontier)))
            return solution(node)
        for action in reversed(problem.actions(node.state)):
            child = child_node(problem, node, action)
            if child.state not in seen:
                seen.add(child.state)
                frontier.append(child)
        trace.append((node.state, tuple(item.state for item in islice(reversed(frontier), 6)), len(frontier)))
    return None
