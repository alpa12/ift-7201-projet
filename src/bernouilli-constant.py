import numpy as np
from environment import Environment
from insurers import EGreedy
from insured import Insured
from distributions import Bernoulli, Constant


p_list = [0.8, 0.2]
s_list = [3, 4]
prem_list = [3, 3]

epsilon = 0.1
capital = 5

T = 100

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Bernoulli(p), sev=Constant(s), premium=prem) for p, s, prem in zip(p_list, s_list, prem_list)]
    insurer = EGreedy(epsilon=epsilon, K=len(prem_list), capital=capital)
    env = Environment(insureds=insureds, T=T)

    print(insurer.name)
    env.simul_plays(5, [insurer])
