import fssa
import vssa
import math

# Define functions specifically needed for Question 1 and 2

def p1_infinity(C, N):
    """Given the number of states and penalty probabilities,
    return the probability of choosing each eaction"""
    D = [0, (1-C[1]), (1-C[2]) ]
    a = math.pow(C[1] / float(C[2]), N)
    b = (C[1] - D[1]) / float((C[2] - D[2]))
    c = (math.pow(C[2], N) - math.pow(D[2], N)) / float(math.pow(C[1], N) - math.pow(D[1], N))

    return 1 / float(1 + a * b * c)

def q12_bsearch(maxN, target, C):
    low = 1
    high = maxN

    while low <= high:
        mid = (low + high) // 2
        p1 = p1_infinity(C, mid)
        if p1 == target:
            return mid                  
        else:
            if target < p1:
                high = mid - 1
            else:
                low = mid + 1

    # Quickly check I haven't gone under
    if p1_infinity(C, high) < target and high < maxN:
        return high+1
    return high

def q3_bsearch(E, reps):
    high = 1
    low = 0.0005
    r = (low+high) / 2
    results = None

    while low <= high:
        r = (low+high) / 2
        f = lambda a,P,p: vssa.lri_f(a, P, p, r)
        g = lambda P: vssa.lri_g(P)
        results = vssa.absorbing_simulation(E,f,g,reps)
        p1 = results[0]

        if 0 <= p1 - 0.95 < 0.005:
            break
        else:
            if p1 < 0.95:
                high = r
            else:
                low = r
    return (r, results)

def question_1():
    # Question 1
    # Testing Tsettlin automata

    C = [0, 0.05, 0.7]
    reps = 50
    experiments = 10000
    tracked = 3000
    f = open("results/question1.csv", "w")
    f.write("$C_1$,$P_1(\infty)$ (Exact),N,\"P[1,2] Experimental\"\n")
    while C[1] <= 0.65:
        E = fssa.create_environment(C)
        N = (q12_bsearch(50, 0.95, C))
        f_t = lambda p, s: fssa.tsettlin_f(p, s, N)
        g_t = lambda s: fssa.tsettlin_g(s, N)
        count = fssa.ergodic_simulation(E, f_t, g_t, N, reps, experiments, tracked)

        print("============================")
        print("Simulation Parameters: \nGiven: C[1]={0:1.2f}, C[2]={1:1.2f}".format(C[1], C[2]))
        print("Binary Search N:",N,"states provides P1(infinity)={0:1.5f}".format(p1_infinity(C,N)))
        print("Experimental Results: P=[{0:2.2f}%, {1:2.2f}%]".format(count[1]*100,count[2]*100))
        print("============================")
        f.write("{0:1.2f},{1:1.4f},{2:2d},\"({3:1.4f},{4:1.4f})\"\n".format(C[1], p1_infinity(C,N), N, count[1], count[2]))
        C[1] += 0.1
    f.close()
def question_2():
    # Question 2
    # Krylov versus Tsettlin halved

    C = [0, 0.6, 0.8]
    C_T = [0, C[1]/2, C[2]/2]
    N = q12_bsearch(50, 0.95, C_T)
    f_t = lambda p, s: fssa.tsettlin_f(p, s, N)
    f_k = lambda p, s: fssa.krylov_f(p,s,N)
    g_t = lambda s: fssa.tsettlin_g(s, N)
    reps = 50
    experiments = 10000
    tracked = 3000
    f = open("results/question2.csv", "w")
    f.write("Scheme,\"[$C_1,C_2$]\",$P_1(\infty)$ (Exact),N,\"P[1,2]\" Experimental\n")

    print("# Question 2\n## Testing Krylov")
    E = fssa.create_environment(C)
    count = fssa.ergodic_simulation(E, f_k, g_t, N, reps, experiments, tracked)
    print("============================")
    print("Simulation Parameters: \nGiven: C[1]={0:1.2f}, C[2]={1:1.2f}".format(C[1], C[2]))
    print("Binary Search N:",N,"states provides P1(infinity)={0:1.5f}".format(p1_infinity(C_T,N)))
    print("Experimental Results: P=[{0:2.2f}%, {1:2.2f}%]".format(count[1]*100,count[2]*100))
    print("============================")

    f.write("{scheme:},\"[{0:1.2f},{1:1.4f}]\",{2:1.4f},{3:2d},\"({4:1.4f},{5:1.4f})\"\n".format(C[1], C[2], p1_infinity(C,N), N, count[1], count[2], scheme="Krylov"))

    print("# Question 2\n## Testing Tsettlin with C = [{0:0.3f},{1:0.3f}]".format(C_T[1], C_T[2]))
    E = fssa.create_environment(C_T)
    count = fssa.ergodic_simulation(E, f_t, g_t, N, reps, experiments, tracked)
    print("============================")
    print("Simulation Parameters: \nGiven: C[1]={0:1.2f}, C[2]={1:1.2f}".format(C_T[1], C_T[2]))
    print("Binary Search N:",N,"states provides P1(infinity)={0:1.5f}".format(p1_infinity(C_T,N)))
    print("Experimental Results: P=[{0:2.2f}%, {1:2.2f}%]".format(count[1]*100,count[2]*100))
    print("============================")
    f.write("{scheme:},\"[{0:1.2f},{1:1.4f}]\",{2:1.4f},{3:2d},\"({4:1.4f},{5:1.4f})\"\n".format(C_T[1], C_T[2], p1_infinity(C,N), N, count[1], count[2], scheme="Tsettlin"))

def question_3():
    # Question 3
    # Testing the L_RI VSSA

    print("## Question 3 ##\n")
    C = [0, 0.05, 0.7]
    reps = 1000
    f = open("results/question3.csv", "w")
    f.write("$C_1$,Reward,\"P[1,2] Experimental\",Mean Intervals\n")
    while C[1] <= 0.65:
        E = vssa.create_environment(C)
        results = q3_bsearch(E, reps)
        reward = results[0]
        results = results[1]
        print("============================")
        print("Simulation Parameters: \nGiven: C[1]={0:1.2f}, C[2]={1:1.2f}".format(C[1], C[2]))
        print("Binary Search, best reward found: {0:1.4f},".format(reward))
        print("Experimental Results: P=[{0:2.2f}%, {1:2.2f}%]".format(results[0]*100,results[1]*100))
        print("Mean number of iterations to convergence: {0:1.2f}".format(results[2]))
        print("Mean time to convergence:\t\t  {0:1.2f}ms".format(results[3]*1000))
        print("============================")
        f.write("{0:1.2f},{1:1.4f},\"({2:1.4f},{3:1.4f})\",{4:1.2f}\n".format(C[1], reward, results[0], results[1], results[2]))
        C[1] += 0.1
    f.close()
# question_1()
# question_2()
question_3()