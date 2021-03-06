import numpy as np
from matplotlib import pyplot
from datetime import datetime
from tqdm import tqdm


class Environment():
    def __init__(self, insureds, T):
        self.insureds = insureds
        self.T = T


    def play(self, insurer):
        ruin_time_step = self.T + 1
        capital_list = [insurer.capital]
        for t in range(self.T):
            k = insurer.get_action()
            premium, claims = self.insureds[k].play()
            insurer.report_results(k, premium, claims)
            capital_list.append(insurer.capital)
            if insurer.is_ruined() and ruin_time_step == self.T + 1:
                ruin_time_step = t
                # print(f"L'assureur s'est ruiné au pas {t}")
                # return t
        return capital_list, ruin_time_step
            
        
    def simul_plays(self, N, insurers, a=0.01, b=0.99, filename=datetime.now().strftime("%d_%H:%M:%S")):
        capital_mean_matrix = []
        capital_low_matrix = []
        capital_high_matrix = []
        ruin_proportion_matrix = []
        for insurer in insurers:
            print(f"--- Playing with insurer {insurer} ---")
            capital_cumul = []
            ruin_time_step_list = []

            # Simulate N experiences
            for n in tqdm(range(N)):
                insurer.reset()
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

    def _compute_var(self, x, alpha):
        idx = int(len(x) * alpha) - 1
        return np.partition(x, idx)[idx]
            
            
    def plot_capital(self, insurers, capital_mean_matrix, capital_low_matrix, capital_high_matrix, filename=datetime.now().strftime("%d_%H:%M:%S")):
        pyplot.clf()
        for insurer, mean, low, high in zip(insurers, capital_mean_matrix, capital_low_matrix, capital_high_matrix):
            pyplot.plot(mean, label=insurer)
            pyplot.fill_between(np.arange(len(mean)), low, high, alpha=0.4)
        pyplot.title("Capital de l'assureur en fonction du temps")
        pyplot.xlabel("Pas de temps")
        pyplot.ylabel("Capital ($)")
        lgd = pyplot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                            fancybox=True, shadow=True, ncol=int(np.ceil(len(insurers) / 3)))
        pyplot.savefig(f"outputs/capital_{filename}", bbox_extra_artists=(lgd,), bbox_inches='tight')

    def plot_ruin_probability(self, insurers, ruin_matrix, filename=datetime.now().strftime("%d_%H:%M:%S")):
        pyplot.clf()
        for insurer, ruin in zip(insurers, ruin_matrix):
            pyplot.plot(ruin, label=insurer)
        pyplot.title("Proportion des ruines en fonction du temps")
        pyplot.xlabel("Pas de temps")
        pyplot.ylabel("Proportion des ruines (%)")
        lgd = pyplot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                           fancybox=True, shadow=True, ncol=int(np.ceil(len(insurers) / 3)))
        pyplot.savefig(f"outputs/ruin_{filename}", bbox_extra_artists=(lgd,), bbox_inches='tight')
