from collections import deque
from heapq import heappop, heappush
from itertools import count, islice
from types import SimpleNamespace


def Node(state, parent=None, action=None):
    node = SimpleNamespace()
    node.state = state
    node.parent = parent
    node.action = action
    return node


def Queue():
    queue = deque()
    return queue


def enqueue(queue, node):
    queue.append(node)


def dequeue(queue):
    if is_empty(queue):
        return None
    return queue.popleft()


def is_empty(queue):
    if len(queue) == 0:
        return True
    else:
        return False


def child_node(problem, parent, action):
    new_state = problem.result(parent.state, action)
    child = Node(
        state=new_state,
        parent=parent,
        action=action
    )
    return child


def solution(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path


def unit_cost(state, action, next_state):
    return 1


def Problem(initial_state, goal_condition, actions, result, step_cost=unit_cost):
    problem = SimpleNamespace()
    problem.initial_state = initial_state
    problem.goal_condition = goal_condition
    problem.actions = actions
    problem.step_cost = step_cost
    problem.result = result
    problem.is_goal = goal_condition
    return problem


def BFS(problem, trace):
    node = Node(problem.initial_state)
    if problem.is_goal(node.state):
        trace.append((None, (), 0))
        return solution(node)
    frontier = Queue()
    enqueue(frontier, node)
    explored = set()
    queued = {node.state}
    trace.append((None, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
    while not is_empty(frontier):
        node = dequeue(frontier)
        queued.remove(node.state)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in queued:
                if problem.is_goal(child.state):
                    trace.append((node.state, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
                    return solution(child)
                queued.add(child.state)
                enqueue(frontier, child)
        trace.append((node.state, tuple(item.state for item in islice(frontier, 6)), len(frontier)))
    return None


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


ALGORITHMS = {"BFS": BFS, "DFS": DFS, "UCS": UCS}
