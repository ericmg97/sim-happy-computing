import scipy.stats as stats
import numpy as np
from random import random
from math import log


def next_exp(lmbda):
    U = random()
    lmbda = 1/lmbda
    return -log(1.0 - U)/lmbda


class HC_Simulation():

    def __init__(self, sellers, engineers, engineers_exp):
        self.serv_clients = stats.rv_discrete( values=([1, 2, 3, 4], [0.45, 0.25, 0.1, 0.2]))
        self.clients_queue = []
        self.sellers = sellers
        self.sellers_queue = []
        self.engineers = engineers
        self.engineers_queue = []
        self.engineers_exp = engineers_exp
        self.engineers_exp_queue = []

        self.gain = 0
        self.time = 0

    def start(self):
        self.clients_queue.append((next_exp(20), 4))

        for time in range(480):
            self.time = time
            if self.clients_queue[-1][0] <= time:
                # Tiempo para el sigiente cliente
                self.clients_queue.append(
                    (time + next_exp(20), self.serv_clients.rvs()))
                self.sellers_queue.append(self.clients_queue.pop(0))

            self._sellers_work()

            self._engineers_work()

            self._engineers_exp_work()

        return self.gain

    def _sellers_work(self):
        for i in range(len(self.sellers_queue) - 1):
            if self.sellers > 0 and self.sellers_queue[i][1] != 0:
                self.sellers -= 1
                actual = self.sellers_queue[i]

                # normal(5,2) -> tiempo que demora un vendedor en atender a un cliente
                self.sellers_queue[i] = (self.time + np.random.normal(5, 2), 0)

                # el cliente necesita reparacion de equipos
                if actual[1] == 1 or actual[1] == 2:
                    if self.engineers == 0 and self.engineers_exp > 0:
                        self.engineers_exp_queue.append(self.sellers_queue[i])
                    else:
                        self.engineers_queue.append(self.sellers_queue[i])

                # el cliente necesita cambio de equipo
                elif actual[1] == 3:
                    # es enviado con un especialista
                    self.engineers_exp_queue.append(self.sellers_queue[i])

                # el cliente va a comprar, lo atiende el vendedor
                elif actual[1] == 4:
                    self.gain += 750  # realizando servicio de venta de equipos

            else:
                if self.sellers_queue[i][0] <= self.time:
                    self.sellers_queue.remove(self.sellers_queue[i])
                    self.sellers += 1

    def _engineers_work(self):
        for i in range(len(self.engineers_queue) - 1):
            if self.engineers > 0 and self.engineers_queue[i][1] != 0:
                self.engineers -= 1
                actual = self.engineers_queue[i]

                # exp(20) -> tiempo que demora un especialista en atender a un cliente
                self.engineers_queue[i] = (self.time + next_exp(20), 0)

                if actual[1] == 2:
                    money += 350  # realizando servicio de reparacion sin garantia

            else:
                if self.engineers_queue[i][0] <= self.time:
                    self.engineers_queue.remove(self.engineers_queue[i])
                    self.engineers += 1

    def _engineers_exp_work(self):
        for i in range(len(self.engineers_exp_queue) - 1):
            if self.engineers_exp > 0 and self.engineers_exp_queue[i][1] != 0:
                self.engineers_exp -= 1
                actual = self.engineers_exp_queue[i]

                if actual[1] == 1:
                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    self.engineers_exp_queue[i] = (self.time + next_exp(20), 0)

                elif actual[1] == 2:  # hay que cobrar el servicio
                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    self.engineers_exp_queue[i] = (self.time + next_exp(20), 0)

                    money += 350  # realizando servicio de reparacion sin garantia
                elif actual[1] == 3:
                    # exp(15) -> tiempo que demora un especialista especializado en realizar cambio de equipos
                    self.engineers_exp_queue[i] = (self.time + next_exp(15), 0)

                    money += 500  # realizando servicio de cambio de equipo

            else:
                if self.engineers_exp_queue[i][0] <= self.time:
                    self.engineers_exp_queue.remove(self.engineers_exp_queue[i])
                    self.engineers_exp += 1


if __name__ == "__main__":
    # v = input("Cantidad de vendedores:")
    # t = input("Cantidad de Tecnicos:")
    # te = input("Cantidad de Tecnicos Especializados:")
    sim = HC_Simulation(2, 3, 1)
    print(sim.start())
