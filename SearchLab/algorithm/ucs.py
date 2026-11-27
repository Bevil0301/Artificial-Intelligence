from heapq import heappop, heappush
from itertools import count
from .common import Node, child_node, solution


def UCS(problem, trace):
    order = count()
    root = Node(problem.initial_state)
    frontier = [(0, next(order), root)]
    pending = {root.state: 0}
    explored = set()

    def next_nodes():
        preview = []
        while frontier and len(preview) < 6:
            entry = heappop(frontier)
            cost, _, node = entry
            if pending.get(node.state) == cost:
                preview.append(entry)
        for entry in preview:
            heappush(frontier, entry)
        return tuple(node.state for _, _, node in preview)

    trace.append((None, (root.state,), 1))
    while frontier:
        cost, _, node = heappop(frontier)
        if pending.get(node.state) != cost:
            continue
        del pending[node.state]
        explored.add(node.state)
        if problem.is_goal(node.state):
            trace.append((node.state, next_nodes(), len(pending)))
            return solution(node)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state in explored:
                continue
            new_cost = cost + problem.step_cost(node.state, action, child.state)
            if new_cost < pending.get(child.state, float("inf")):
                pending[child.state] = new_cost
                heappush(frontier, (new_cost, next(order), child))
        trace.append((node.state, next_nodes(), len(pending)))
    return None
