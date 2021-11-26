import numpy as np
from environment import Environment
from insurers.e_greedy import EGreedy
from insurers.insurer import Insurer
from insured import Insured
from distributions.bernoulli import Bernoulli
from distributions.constant import Constant


p_list = [0.8, 0.2]
s_list = [3, 4]
prem_list = [1.1, 0.9]

epsilon = 0.1
capital = 5

T = 100

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Bernoulli(p), sev=Constant(s), premium=1) for p, s, prem in zip(p_list, s_list, prem_list)]
    insurer = EGreedy(epsilon, K=len(p_list), capital=capital)
    env = Environment(insureds, T)

    env.play(insurer)
