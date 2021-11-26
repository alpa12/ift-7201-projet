from environment import Environment
from insurers.e_greedy import EGreedy
from insurers.insurer import Insurer
from insured import Insured
from distributions.bernoulli import Bernoulli
from distributions.constant import Constant

ps = [0.8, 0.2]
insureds = [Insured(freq=Constant(1), sev=Bernoulli(p)) for p in ps]

insurer = Insurer(K=len(ps))

env = Environment(insureds, insurer, T=10)

env.play()
