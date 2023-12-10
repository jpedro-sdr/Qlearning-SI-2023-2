import numpy as np
import random
import time
from collections import defaultdict
from connection import connect, get_state_reward

# Defina os parâmetros do Q-Learning
alpha = 0.1  # Taxa de aprendizado
gamma = 0.9  # Fator de desconto
epsilon = 0.1  # Exploração vs Exploração

# Defina o número de ações possíveis
actions = ["left", "right", "jump"]

# Função para escolher uma ação com base no estado atual e na política epsilon-greedy
def choose_action(q_values, state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(actions)
    else:
        return max(actions, key=lambda a: q_values[state][a])

# Função para atualizar os valores Q com base na recompensa e na próxima ação
def update_q_values(q_values, state, action, reward, next_state):
    max_next_q = max(q_values[next_state].values()) if next_state in q_values else 0
    q_values[state][action] += alpha * (reward + gamma * max_next_q - q_values[state][action])

# Função principal para executar o algoritmo Q-Learning
def q_learning(port):
    # Inicialize os valores Q para cada par estado-ação
    q_values = defaultdict(lambda: {a: 0 for a in actions})

    # Conecte-se ao servidor
    socket_conn = connect(port)

    # Laço principal de treinamento
    while True:

        # Obtenha o estado atual e a recompensa
        print("Antes de chamar get_state_reward")
        state, reward = get_state_reward(socket_conn, None)
        print("Após chamar get_state_reward")

        # Escolha uma ação com base na política epsilon-greedy
        action = choose_action(q_values, state)
        # Execute a ação e obtenha o próximo estado e recompensa
        next_state, next_reward = get_state_reward(socket_conn, action)

        # Atualize os valores Q com base na recompensa e na próxima ação
        update_q_values(q_values, state, action, reward, next_state)

        # Salve a Q-table em um arquivo .txt
        with open("q_table.txt", "w") as f:
            for state, actions in q_values.items():
                f.write(f"{state}: {actions}\n")

        # Aguarde um momento antes da próxima iteração (pode ser ajustado)
        time.sleep(0.1)

if __name__ == "__main__":
    # Substitua a porta abaixo pela porta correta do seu jogo
    porta_do_jogo = 2037
    q_learning(porta_do_jogo)
