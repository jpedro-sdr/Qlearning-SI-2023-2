import random
from connection import connect, get_state_reward
import numpy as np
import time

tempo_maximo_segundos = 9000  # 2 horas
tempo_inicio = time.time()

#epsilon = 0.95
alfa = 0.1 # Coeficiente de aprendizado
gamma = 0.97 # Fator de desconto

class Estado:
    def __init__(self, esquerda: str, direita: str, pulo: str):
        self.esquerda = float(esquerda)
        self.direita = float(direita)
        self.pulo = float(pulo)


class AgenteQLearning:
    ACOES = ["left", "right", "jump"]

    def obter_acao(self, matriz: list[Estado], estado: str, epsilon: float) -> str:
        
        estado_agente = int(estado, 2)
        if random.random() > epsilon:
            valor_estado_agente = matriz[estado_agente]
            valor_acao = max(valor_estado_agente.esquerda, valor_estado_agente.direita, valor_estado_agente.pulo)

            if valor_acao == valor_estado_agente.esquerda:
                return "left"
            elif valor_acao == valor_estado_agente.direita:
                return "right"
            return "jump"

        # Se o valor de exploração  menor escolher uma ação aleatória entre left, right e jump
        return AgenteQLearning.ACOES[np.random.randint(3)]


    def q_learning(self, matriz: list[Estado], estado: str, ultimo_estado: str, acao: str, recompensa: int) -> list[Estado]:
        q_max = 0
        
        estado_agente = int(estado, 2)
        estado_ultimo_agente = int(ultimo_estado, 2)

        # Obtenção dos valores Q máximos para o estado atual
        linha_estado = matriz[estado_agente]
        q_max = max(linha_estado.esquerda, linha_estado.direita, linha_estado.pulo)
        # Atualização da matriz Q com base na ação tomada, recompensa e valor Q máximo
        if acao == "jump":
            matriz[estado_ultimo_agente].pulo += alfa * ((recompensa + (gamma * q_max)) - matriz[estado_ultimo_agente].pulo)
        elif acao == "left":
            matriz[estado_ultimo_agente].esquerda += alfa * ((recompensa + (gamma * q_max)) - matriz[estado_ultimo_agente].esquerda)
        else:
            matriz[estado_ultimo_agente].direita += alfa * ((recompensa + (gamma * q_max)) - matriz[estado_ultimo_agente].direita)

        return matriz


class Matriz:
    RESULTADO = './qtable.txt'

    def obter_matriz(self):
        with open(Matriz.RESULTADO, 'r') as arquivo:
            texto = arquivo.readlines()
            estados = [linha.strip().split() for linha in texto]
            matriz = [Estado(estado[0], estado[1], estado[2]) for estado in estados]
            return matriz

    def atualizar_matriz(self, matriz: list[Estado]):
        with open(Matriz.RESULTADO, "w") as arquivo:
            novos_estados = ""
            for estado in matriz:
                novos_estados += f'{estado.esquerda:.6f} {estado.direita:.6f} {estado.pulo:.6f}\n'
            arquivo.write(novos_estados)

class Amongois:
    def __init__(self, epsilon_decay_rate=0.00001):
        self.__carregador_matriz = Matriz()
        self.__agente = AgenteQLearning()
        self.__socket = connect(2037)
        self.epsilon_decay_rate = epsilon_decay_rate
        self.epsilon = 0.99

    def iniciar_jogo(self):
        matriz = self.__carregador_matriz.obter_matriz()
        while True:
            if time.time() - tempo_inicio > tempo_maximo_segundos:
                break

            ultimo_estado = '0000000'
            recompensa_ultimoEstado = -14

            while recompensa_ultimoEstado != 300:
                # Decaimento de epsilon
                self.epsilon = max(0.1, self.epsilon - self.epsilon_decay_rate)
                acao = self.__agente.obter_acao(matriz, ultimo_estado, self.epsilon)
                estado, recompensa = get_state_reward(self.__socket, acao)
                matriz = self.__agente.q_learning(matriz, estado, ultimo_estado, acao, recompensa)
                recompensa_ultimoEstado = recompensa
                ultimo_estado = estado
                print(recompensa)
            self.__carregador_matriz.atualizar_matriz(matriz)

# Cliente.py
if __name__ == "__main__":
    amongois = Amongois()
    amongois.iniciar_jogo()
