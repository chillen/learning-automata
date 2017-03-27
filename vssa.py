import random
import time

def create_environment(C):
    return lambda a: 1 if random.uniform(0, 1) < C[a] else 0

def lri_g(P):
    """How actions are selected"""
    rng = random.random()
    if rng < P[1]:
        return 1
    return 2

def lri_f(action, penalty, P, r):
    """How P is updated"""
    if penalty:
        return P
    P[action] = P[action] + r * (1 - P[action])
    for j in range(1, len(P)):
        if j != action:
            P[j] = P[j] - r * P[j]
    return P

def absorbing_simulation(environment, f, g, reps):
    count = [0, 0, 0]
    total = 0
    iterations = 0
    elapsed = 0
    for _ in range(reps):
        P = [0, 0.5, 0.5]
        # Get the automata into a converged state
        iterations = 0
        start = time.time()
        while P[1] < 0.98 and P[2] < 0.98:
            action = g(P)
            penalty = environment(action)
            P = f(action, penalty, P)
            iterations += 1
        elapsed += time.time() - start
        count[0] += P[0]
        count[1] += P[1]
        count[2] += P[2]
        total += iterations
    return (count[1] / reps, count[2] / reps, total / reps, elapsed / reps)