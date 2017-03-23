import random
import math

def tsettlin_f(penalty, state, N):
    """State selection for Tsettlin"""
    if penalty:
        if state % N != 0:      # In neither N nor 2N
            state = state + 1   # Weaken
        else:
            if state == N:      # Swap sides
                state = 2*N
            else:
                state = N
    else:
        if state % N != 1:      # In neither N nor 2N
            state = state - 1   # Strengthen
    return state

# Krylov is very similar to Tsettlin, however it stochastically moves on penalty
def krylov_f(penalty, state, N):
    """State selection for Krylov"""
    if penalty and random.uniform(0, 1) <= 0.5:
        penalty = not penalty
    if penalty:
        if state % N != 0:      # In neither N nor 2N
            state = state + 1   # Weaken
        else:
            if state == N:      # Swap sides
                state = 2*N
            else:
                state = N
    else:
        if state % N != 1:      # In neither N nor 2N
            state = state - 1   # Strengthen
    return state

def tsettlin_g(state, N):
    """Action selection"""
    action = 2
    if 1 <= state <= N:
        action = 1
    return action

def environment(action, C):
    """Generic environment; takes in an action and responds with penalty or reward"""
    penalty = 0
    if random.uniform(0, 1) < C[action]:
        penalty = 1
    return penalty

def automaton(N, C, g, f, state):
    """Selects an action and state according to the G and F"""
    action = g(state, N)
    penalty = environment(action, C)
    state = f(penalty, state, N)
    return state

def p_1_infy(N, C): 
    """Returns the accuracy given number of states and penalty probs"""
    # I've broken up the pieces of the equation for readability
    D = [ 0, (1-C[1]), (1-C[2]) ]           # Padded to conform to C_1, D_1 algorithm
    
    a = math.pow(C[1] / float(C[2]), N)
    b = (C[1] - D[1]) / float((C[2] - D[2]))
    c = (math.pow(C[2], N) - math.pow(D[2], N)) / float(math.pow(C[1], N) - math.pow(D[1], N))

    return 1 / float(1 + a * b * c)

def p_1_bsearch(maxN, target, C):
    low = 1
    high = maxN

    while low <= high:
        mid = (low + high) // 2
        p1 = p_1_infy(mid, C)
        if p1 == target:
            return mid                  # Found it exactly? Unlikely, but sure
        else:
            if target < p1:
                high = mid - 1
            else:
                low = mid + 1

    # Quickly check I haven't gone under
    if p_1_infy(high, C) < target and high < maxN:
        return high+1
    return high

def simulation(f, g, C, N):
    print("==================================")
    print("Testing C=[{0:1.2f}, {1:1.2f}]".format(C[1], C[2]))
    print("Simulation: 27k experiments, then record 3k experiments, over 50 repetitions\n")
    print("Given C1={0:1.2f}, P1(∞)={1:1.4f}, N={2:1d}".format(C[1], p_1_infy(N, C), N))

    # Over 50 repetitions...
    count = [0, 0, 0]
    for _ in range(50):
        # Get the automata into a converged state with 27000 tests.
        state = N if (random.random() <= 0.5) else 2*N

        for i in range(27000):
            state = automaton(N, C, g, f, state)
        # Track the states
        for _ in range(3000):
            state = automaton(N, C, g, f, state)
            count[g(state, N)] += 1
    
    print("P = [{0:1.5f},{1:1.5f}]".format(count[1]/(3000*50), count[2]/(3000*50)))

    print("==================================\n\n")

def question_1():
    """This is Question 1 a, b, and c: 
    Test with c2 = 0.7 and c1 = 0.05 .. 0.65 in 0.1 increments
    P1 is derived from binary search, exactly, to determine suitable N for 95% accuracy
    """

    # Give ourselves some easy to pass around lambdas to keep the functions general
    g = lambda s, n: tsettlin_g(s, n)
    f = lambda b, s, c: tsettlin_f(b, s, c)
    c_max = 0.65
    C = [0, 0.05, 0.7]
    max_states = 50
    target_accuracy = 0.95

    # Perform our simulation by finding the optimal number of states, N
    print("# Question 1: Testing Tsettlin")
    while C[1] <= c_max:
        N = (p_1_bsearch(max_states, target_accuracy, C))
        simulation(f, g, C, N)
        C[1] += 0.1

def question_2():
    """Question 2
    Pick any one environment. Interact with the environment with halved probabilities
    Then run the original, non-halved probabilities with Krylov
    """
    # Krylov uses Tsettlin for G, so it does not need to be redefined
    g = lambda s, n: tsettlin_g(s, n)
    f = lambda b,s,c: krylov_f(b, s, c)
    f_t = lambda b,s,c: tsettlin_f(b, s, c)
    max_states = 50
    target_accuracy = 0.95
    C = [0, 0.6, 0.8]
    C_T = [0, C[1]/2, C[2]/2]
    N = (p_1_bsearch(max_states, target_accuracy, C_T))

    print("# Question 2\n## Testing Krylov with C = [{0:0.3f},{1:0.3f}]".format(C[1], C[2]))
    simulation(f, g, C, N)

    N = (p_1_bsearch(max_states, target_accuracy, C_T))

    print("# Question 2\n## Testing Tsettlin with C = [{0:0.3f},{1:0.3f}]".format(C_T[1], C_T[2]))
    simulation(f_t, g, C_T, N)

def question_3():
    pass

#question_1()
question_2()
