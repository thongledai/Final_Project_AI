import math
import random
import time
from Core.Node import Node
from Core.Result import Solution
from Core.Utils import Is_Goal,Child_Nodes, Heuristic


def Simulated_Annealing_Search(
    initial_state,
    max_steps=5000,
    start_temperature=10.0,
    cooling_rate=0.995,
    seed=None,
):
    rng = random.Random(seed)
    start_time = time.time()
    current = Node(initial_state)
    best = current
    expanded_nodes = 0
    generated_nodes = 1
    temperature = start_temperature

    for _ in range(max_steps):
        if Is_Goal(current.state):
            return Solution(current, expanded_nodes, generated_nodes, start_time)

        children = Child_Nodes(current)
        expanded_nodes += 1
        generated_nodes += len(children)

        if not children or temperature <= 0.000001:
            break

        candidate = rng.choice(children)
        delta = Heuristic(current.state) - Heuristic(candidate.state)

        if delta > 0 or rng.random() < math.exp(delta / temperature):
            current = candidate
            if Heuristic(current.state) < Heuristic(best.state):
                best = current

        temperature *= cooling_rate

    return Solution(best, expanded_nodes, generated_nodes, start_time)


def Search(
    initial_state,
    max_steps=5000,
    start_temperature=10.0,
    cooling_rate=0.995,
    seed=None,
):
    return Simulated_Annealing_Search(
        initial_state,
        max_steps,
        start_temperature,
        cooling_rate,
        seed,
    )

