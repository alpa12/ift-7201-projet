import numpy as np
from matplotlib import pyplot
from datetime import datetime
from tqdm import tqdm
from distributions import Gamma, LogNormal, Pareto, Poisson, Bernoulli
from environment import Insured, Environment



class Wild(Environment):
    def __init__(self, K, T):
        self.K = K
        self.T = T

    def play(self, insurer):
        ruin_time_step = self.T + 1
        capital_list = [insurer.capital]
        for t in range(self.T):
            k = insurer.get_action()
            premium, claims = self.insureds[k].play()
            insurer.report_results(k, premium, claims)
            capital_list.append(insurer.capital)
            if insurer.is_ruined():
                ruin_time_step = t
                capital_list[-1] = 0
                capital_list += [0] * (self.T - t - 1)
                return capital_list, ruin_time_step

        return capital_list, ruin_time_step
            
        
    def simul_plays(self, N, insurers, a=0.01, b=0.99, filename=datetime.now().strftime("%d_%H:%M:%S")):
        capital_mean_matrix = []
        capital_low_matrix = []
        capital_high_matrix = []
        ruin_proportion_matrix = []

        # Simul N * K insureds
        insured_matrix = []
        print(f"Generating {N} * {self.K} insureds")
        for _ in tqdm(range(N)):
            insured_list = []
            for _ in range(self.K):
                freq = Poisson(_lambda=np.random.uniform(2, 5))
                sev = np.random.choice([
                    # Each severity has expected value in [50, 100]
                    Gamma(alpha=np.random.uniform(10, 15), theta=np.random.uniform(5, 100/15)),
                    LogNormal(mu=np.random.uniform(0.5, 1), sigma=np.random.uniform(np.sqrt(2 * (np.log(50) - 0.5)), np.sqrt(2 * (np.log(100) - 1)))),
                    Pareto(alpha=np.random.uniform(5, 10), _lambda=np.random.uniform(50/9, 100/4))
                ])
                insured_list.append(Insured(freq=freq, sev=sev, premium=np.random.choice([0.95, 0.97, 1, 1.01]) * freq.get_mean() * sev.get_mean()))
            insured_matrix.append(insured_list)

        for insurer in insurers:
            print(f"--- Playing with insurer {insurer} ---")
            capital_cumul = []
            ruin_time_step_list = []

            # Simulate N experiences
            for n in tqdm(range(N)):
                insurer.reset()
                self.insureds = insured_matrix[n]
                capital_list, ruin_time_step = self.play(insurer)
                capital_cumul.append(capital_list)
                ruin_time_step_list.append(ruin_time_step)

            # Compute results for capital plot
            capital_mean_matrix.append(np.mean(capital_cumul, axis=0))
            capital_low_list = []
            capital_high_list = []
            for t in range(self.T + 1): # 1 capital datapoint for each time step + 1 for initial capital
                tth_values = [capital_cumul[n][t] for n in range(N)]
                capital_low_list.append(self._compute_var(tth_values, alpha=a))
                capital_high_list.append(self._compute_var(tth_values, alpha=b))
            capital_low_matrix.append(capital_low_list)
            capital_high_matrix.append(capital_high_list)
            
            
            # Compute results for ruin plot
            ruin_time_step_list = np.array(ruin_time_step_list)
            ruin_proportion_list = []
            for t in range(self.T):
                ruin_proportion_list.append(np.mean(ruin_time_step_list < t))
            ruin_proportion_matrix.append(ruin_proportion_list)

            print("\n")

        self.plot_capital(insurers, capital_mean_matrix, capital_low_matrix, capital_high_matrix, filename)
        self.plot_ruin_probability(insurers, ruin_proportion_matrix, filename)
