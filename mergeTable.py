import numpy as np

# Carregue as duas Q-tables
qtable1 = np.loadtxt('resultadoPlat0.txt')
qtable2 = np.loadtxt('resultadoPlat20.txt')

weight_factor = 0.5

# Calcule a média ponderada das duas Q-tables
merged_qtable = (1 - weight_factor) * qtable1 + weight_factor * qtable2
e
np.savetxt('qtable.txt', merged_qtable)
