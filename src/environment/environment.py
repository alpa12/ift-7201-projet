import numpy as np
from matplotlib import pyplot
from datetime import datetime
from tqdm import tqdm


class Environment():
    def __init__(self, insureds, T):
        self.insureds = insureds
        self.T = T


    def play(self, insurer):
        has_been_ruined = False
        capital_list = [insurer.capital]
        for t in range(self.T):
            k = insurer.get_action()
            premium, claims = self.insureds[k].play()
            insurer.report_results(k, premium, claims)
            capital_list.append(insurer.capital)
            if insurer.is_ruined() and not has_been_ruined:
                has_been_ruined = True
                # print(f"L'assureur s'est ruiné au pas {t}")
                # return t
        return capital_list
            
        
    def simul_plays(self, N, insurers, a=0.01, b=0.99):
        capital_mean_matrix = []
        capital_low_matrix = []
        capital_high_matrix = []
        for insurer in insurers:
            print(f"--- Playing with insurer {insurer.name} ---")
            capital_cumul = []

            # Simulate N experiences
            for n in tqdm(range(N)):
                insurer.reset()
                capital_cumul.append(self.play(insurer))

            # Compute results for plot
            capital_mean_matrix.append(np.mean(capital_cumul, axis=0))
            capital_low_list = []
            capital_high_list = []
            for t in range(len(capital_cumul[0])):
                tth_values = [capital_cumul[n][t] for n in range(len(capital_cumul))]
                capital_low_list.append(self._compute_var(tth_values, alpha=a))
                capital_high_list.append(self._compute_var(tth_values, alpha=b))
            capital_low_matrix.append(capital_low_list)
            capital_high_matrix.append(capital_high_list)
            print("\n")

        self.plot_capital([i.name for i in insurers], capital_mean_matrix, capital_low_matrix, capital_high_matrix)

    def _compute_var(self, x, alpha):
        idx = int(len(x) * alpha) - 1
        return np.partition(x, idx)[idx]
            
            
    def plot_capital(self, insurer_name_list, capital_mean_matrix, capital_low_matrix, capital_high_matrix, filename=datetime.now().strftime("%d_%H:%M:%S")):
        for insurer_name, mean, low, high in zip(insurer_name_list, capital_mean_matrix, capital_low_matrix, capital_high_matrix):
            pyplot.plot(mean, label=insurer_name)
            pyplot.fill_between(np.arange(len(mean)), low, high, alpha=0.4)
        pyplot.title("Capital de l'assureur en fonction du temps")
        pyplot.xlabel("Pas de temps")
        pyplot.ylabel("Capital ($)")
        pyplot.legend()
        pyplot.savefig(f"outputs/{filename}") # TODO: Ajouter titre et nom d'assureur
