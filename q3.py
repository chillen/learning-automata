import random
import math
import time

# TODO Do a damn cumulative distribution at some point, numpy has it built into choice
def g(P):
    """How actions are selected"""
    rng = random.random()
    if rng < P[1]:
        return 1
    return 2

def f(action, penalty, r, P):
    """How P is updated"""
    if penalty:
        return P
    P[action] = P[action] + r * (1 - P[action])
    for j in range(1, len(P)):
        if j != action:
            P[j] = P[j] - r * P[j]
    return P

def environment(action, C):
    """Generic environment; takes in an action and responds with penalty or reward"""
    penalty = 0
    if random.uniform(0, 1) < C[action]:
        penalty = 1
    return penalty

def automaton(r, C, P):
    """Selects an action and P according to the G and F"""
    action = g(P)
    penalty = environment(action, C)
    P = f(action, penalty, r, P)
    return P

def simulation(r, C):
    count = [0, 0, 0]
    total = 0
    iterations = 0
    num = 200
    elapsed = 0
    for _ in range(num):
        P = [0, 0.5, 0.5]
        # Get the automata into a converged state
        iterations = 0
        start = time.time()
        while P[1] < 0.99999999999999 and P[2] < 0.99999999999999:
            P = automaton(r, C, P)
            iterations += 1
        elapsed += time.time() - start
        count[0] += P[0]
        count[1] += P[1]
        count[2] += P[2]
        total += iterations
    return (count[1]/num, total / num, elapsed / num)


C = [0, 0.05, 0.7]
P = [0, 0.5, 0.5]

c_max = 0.65
r_max = 1
r_min = 0.00005
target = 0.95

while C[1] <= c_max:
    high = r_max
    low = r_min
    r = (low+high) / 2
    results = None
    while low <= high:
        r = (low+high) / 2
        results = simulation(r, C)
        p1 = results[0]
        
        if 0 <= p1 - target < 0.005:
            break
        else:
            if p1 < target:
                high = r - r_min
            else:
                low = r + r_min
    # Just in case low overcomes high, we'll make sure we're still at our best.
    if p1 < target:
        r += r_min
    print("==================================")
    print("Testing C=[{0:1.2f}, {1:1.2f}] with learning rate r={2:0.3f}".format(C[1], C[2], r))
    print("Simulation achieved {0:1.3f} accuracy with a mean time of {1:6.2f} iterations, or {2:3.6f}s.".format(results[0], results[1], results[2]))
    print("==================================")

    C[1] += 0.1

