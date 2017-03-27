import random

def create_environment(C):
    return lambda a: 1 if random.uniform(0, 1) < C[a] else 0

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

def tsettlin_g(state, N):
    """Action selection"""
    action = 2
    if 1 <= state <= N:
        action = 1
    return action

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

def ergodic_simulation(environment, f, g, N, reps, converge, tracked):
    count = [0, 0, 0]
    for _ in range(reps):
        state = N if (random.random() <= 0.5) else 2*N

        for _ in range(converge):
            action = g(state)
            penalty = environment(action)
            state = f(penalty, state)
        for _ in range(tracked):
            action = g(state)
            penalty = environment(action)
            state = f(penalty, state)
            count[action] += 1
    return [c/(tracked*reps) for c in count] 
