import numpy as np
from environment import Wild
from insurers import ETGreedy, RiskAware, UCB, Insurer
from risk_measures import VaR, TVaR, PoR


filename = "experiment7_wild"

K = 50

prior = None


capital = 500
interest_rate = 0.00

T = 500
M = 10000


if __name__ == "__main__":
    np.random.seed(2021)

    insurers = []
    insurers.append(ETGreedy(K=K, capital=capital, interest_rate=interest_rate)) # ETGreedy strategy with epsilon = 1 / sqrt(t)
    insurers.append(Insurer(K=K, capital=capital, interest_rate=interest_rate)) # Chooses insured randomly
    insurers.append(RiskAware(A=100, K=K, risk_measure=VaR(kappa=0.95, prior=prior), capital=capital, interest_rate=interest_rate))
    insurers.append(RiskAware(A=100, K=K, risk_measure=TVaR(kappa=0.95, prior=prior), capital=capital, interest_rate=interest_rate))
    insurers.append(RiskAware(A=100000, K=K, risk_measure=PoR(prior=prior), capital=capital, interest_rate=interest_rate))
    insurers.append(UCB(K=K, capital=capital, interest_rate=interest_rate))
    env = Wild(K=K, T=T)

    env.simul_plays(M, insurers, a = 0.5, b = 0.5, filename=filename)
