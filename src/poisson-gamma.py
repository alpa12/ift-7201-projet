import numpy as np
from environment import Environment
from insurers import EGreedy
from insured import Insured
from distributions import Poisson, Gamma


lambda_list = [0.005, 0.05, 0.03]
alpha_list = [3, 1, 2]
theta_list = [55000, 7500, 6000]
prem_list = [600, 400, 400]

epsilon = 0.1
capital = 300000

T = 10000

if __name__ == "__main__":
    np.random.seed(2021)
    insureds = [Insured(freq=Poisson(_lambda), sev=Gamma(alpha, theta), premium=prem) \
        for _lambda, alpha, theta, prem in zip(lambda_list, alpha_list, theta_list, prem_list)]
    insurer = EGreedy(epsilon, K=len(prem_list), capital=capital)
    env = Environment(insureds, T)

    env.play()
