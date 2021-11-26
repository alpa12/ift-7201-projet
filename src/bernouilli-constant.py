import numpy as np
from environment import Environment
from insurers import EGreedy, Insurer
from insured import Insured
from distributions import Bernoulli, Constant


p_list = [0.45, 0.55]
s_list = [.55, .45]
prem_list = [0.1, 0.1]

epsilon = 0.05
capital = 5

T = 100

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Bernoulli(p), sev=Constant(s), premium=prem) for p, s, prem in zip(p_list, s_list, prem_list)]
    insurer1 = EGreedy(epsilon=epsilon, name="EGreedy e=0.01", K=len(prem_list), capital=capital)
    env = Environment(insureds=insureds, T=T)

    env.simul_plays(100, [insurer1])
