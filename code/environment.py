import numpy as np
from matplotlib import pyplot



class Environment():
    def __init__(self, insureds, T):
        self.insureds = insureds
        self.T = T

    def play(self, insurer):
        capitals = [insurer.capital]
        for t in range(self.T):
            k = insurer.get_action()
            premium, claims = self.insureds[k].play()
            insurer.report_results(k, premium, claims)
            capitals.append(insurer.capital)
            if insurer.is_ruined():
                print(f"L'assureur s'est ruiné au pas {t}")
                # return t
        self.plot_capital(capitals)

    def plot_capital(self, capitals):
        pyplot.plot(capitals, label="label")
        # pyplot.fill_between(np.arange(T), avg_cumul_regret, avg_cumul_regret+std_cumul_regret, alpha=0.4)
        pyplot.legend()
        pyplot.savefig("outputs/test_output")
