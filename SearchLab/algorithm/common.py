from collections import deque
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
