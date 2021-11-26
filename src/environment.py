import numpy as np
from matplotlib import pyplot



class Environment():
    def __init__(self, insureds, T):
        self.insureds = insureds
        self.T = T


    def play(self, insurer):
        capital_list = [insurer.capital]
        for t in range(self.T):
            k = insurer.get_action()
            premium, claims = self.insureds[k].play()
            insurer.report_results(k, premium, claims)
            capital_list.append(insurer.capital)
            if insurer.is_ruined():
                print(f"L'assureur s'est ruiné au pas {t}")
                # return t
        return capital_list
            
        
    def simul_plays(self, N, insurers, a=0.1, b=0.9):
        insurer_name_list = []
        capital_mean_matrix = []
        capital_low_matrix = []
        capital_high_matrix = []
        for insurer in insurers:
            # insurer_name_list.append(insurer.name)
            capital_cumul = []
            for n in range(N):
                capital_cumul.append(self.play(insurer))
            capital_mean_matrix.append(np.mean(capital_cumul, axis=0))
            capital_low_list = []
            capital_high_list = []
            for t in range(len(capital_cumul[0])):
                tth_values = [capital_cumul[i][t] for i in range(len(capital_cumul))]
                print(tth_values)
                print(a)
                capital_low_list.append(self._compute_var(tth_values, alpha=a))
                capital_high_list.append(self._compute_var(tth_values, alpha=b))

            capital_low_matrix.append(capital_low_list)
            capital_high_matrix.append(capital_high_list)

            print(self._compute_var([1,2,3,4,5,6,7,8,9,10], 0.3))

        self.plot_capital(["abc"], capital_mean_matrix, capital_low_matrix, capital_high_matrix)

    def _compute_var(self, x, alpha):
        idx = int(len(x) * alpha) - 1
        return np.partition(x, idx)[idx]
            
            


    def plot_capital(self, insurer_name_list, capital_mean_matrix, capital_low_matrix, capital_high_matrix):
        for insurer_name, mean, low, high in zip(insurer_name_list, capital_mean_matrix, capital_low_matrix, capital_high_matrix):
            pyplot.plot(mean, label=insurer_name)
            pyplot.fill_between(np.arange(len(mean)), low, high, alpha=0.4)
        pyplot.legend()
        pyplot.savefig("outputs/test_output")
