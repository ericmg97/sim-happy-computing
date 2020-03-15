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
        self.clients_queue.append((next_exp(20), self.serv_clients.rvs(), 1, False))

        for time in range(1000):
            self.time = time
            if self.clients_queue[-1][0] <= time and time < 480:
                print(f"{self.time}min -> LLegada de cliente {self.clients_queue[-1][2]}")

                # Tiempo para el sigiente cliente
                self.clients_queue.append( (self.time + next_exp(20), self.serv_clients.rvs(), self.clients_queue[-1][2] + 1, False))
                self.sellers_queue.append(self.clients_queue.pop(0))

            self._sellers_work()

            self._engineers_work()

            self._engineers_exp_work()

        return self.gain

    def _sellers_work(self):
        i = 0
        while True:
            if i >= len(self.sellers_queue):
                break         

            if self.sellers > 0 and not self.sellers_queue[i][3]:
                self.sellers -= 1
                time_to_finish = self.time + np.random.normal(5, 2)

                actual = (time_to_finish, self.sellers_queue[i][1], self.sellers_queue[i][2], True)

                print(f"{self.time}min -> Cliente {actual[2]} siendo atendido por vendedor. {self.sellers, self.engineers, self.engineers_exp}")
                # normal(5,2) -> tiempo que demora un vendedor en atender a un cliente
                self.sellers_queue[i] = actual

                # el cliente va a comprar, lo atiende el vendedor
                if self.sellers_queue[i][1] == 4:
                    print(f"Cliente {self.sellers_queue[i][2]} comprando equipo.")
                    self.gain += 750  # realizando servicio de venta de equipos

            else:
                if self.sellers_queue[i][0] <= self.time and self.sellers_queue[i][3]:
                    print(f"{self.time}min -> Cliente {self.sellers_queue[i][2]} fue atendido por vendedor. {self.sellers + 1, self.engineers, self.engineers_exp}")

                    actual = (self.sellers_queue[i][0], self.sellers_queue[i][1], self.sellers_queue[i][2], False)

                    # el cliente necesita reparacion de equipos
                    if self.sellers_queue[i][1] == 1 or self.sellers_queue[i][1] == 2:
                        if self.engineers == 0 and self.engineers_exp > 0:
                            self.engineers_exp_queue.append(actual)
                        else:
                            self.engineers_queue.append(actual)

                    # el cliente necesita cambio de equipo
                    elif self.sellers_queue[i][1] == 3:
                        # es enviado con un especialista
                        self.engineers_exp_queue.append(actual)

                    self.sellers_queue.remove(self.sellers_queue[i])
                    self.sellers += 1
                    i -= 1

            i += 1

    def _engineers_work(self):
        i = 0

        while True:
            if i >= len(self.engineers_queue):
                break

            if self.engineers > 0 and not self.engineers_queue[i][3]:
                self.engineers -= 1
                actual = self.engineers_queue[i]

                print(f"{self.time}min -> Cliente {self.engineers_queue[i][2]} siendo atendido por tecnico. {self.sellers, self.engineers, self.engineers_exp}")

                # exp(20) -> tiempo que demora un especialista en atender a un cliente
                self.engineers_queue[i] = (actual[0] + next_exp(20), actual[1], actual[2], True)
                if actual[1] == 1:
                    print(f"Cliente {self.engineers_queue[i][2]} reparacion con garantia por tecnico.")
                elif actual[1] == 2:
                    print(f"Cliente {self.engineers_queue[i][2]} reparacion sin garantia por tecnico.")
                    self.gain += 350  # realizando servicio de reparacion sin garantia

            else:
                if self.engineers_queue[i][0] <= self.time and self.engineers_queue[i][3]:
                    print(f"{self.time}min -> Cliente {self.engineers_queue[i][2]} fue atendido por tecnico. {self.sellers, self.engineers + 1, self.engineers_exp}")
                    self.engineers_queue.remove(self.engineers_queue[i])
                    self.engineers += 1
                    i -= 1
            
            i += 1

    def _engineers_exp_work(self):
        i = 0
        while True:
            if i >= len(self.engineers_exp_queue):
                break

            if self.engineers_exp > 0 and not self.engineers_exp_queue[i][3]:
                self.engineers_exp -= 1
                actual = self.engineers_exp_queue[i]

                print(f"{self.time}min -> Cliente {self.engineers_exp_queue[i][2]} siendo atendido por tecnico especialista. {self.sellers, self.engineers, self.engineers_exp}")

                if actual[1] == 1:
                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    self.engineers_exp_queue[i] = (actual[0] + next_exp(20), actual[1], actual[2], True)
                    print(f"Cliente {self.engineers_exp_queue[i][2]} reparacion sin garantia por tecnico especialista.")

                elif actual[1] == 2:  # hay que cobrar el servicio
                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    self.engineers_exp_queue[i] = (actual[0] + next_exp(20), actual[1], actual[2], True)
                    print(f"Cliente {self.engineers_exp_queue[i][2]} reparacion con garantia por tecnico especialista.")

                    self.gain += 350  # realizando servicio de reparacion sin garantia
                elif actual[1] == 3:
                    # exp(15) -> tiempo que demora un especialista especializado en realizar cambio de equipos
                    self.engineers_exp_queue[i] = (actual[0] + next_exp(15), actual[1], actual[2], True)
                    print(f"Cliente {self.engineers_exp_queue[i][2]} cambio de equipos.")

                    self.gain += 500  # realizando servicio de cambio de equipo

            else:
                if self.engineers_exp_queue[i][0] <= self.time and self.engineers_exp_queue[i][3]:
                    print(f"{self.time}min -> Cliente {self.engineers_exp_queue[i][2]} fue atendido por tecnico especialista. {self.sellers, self.engineers, self.engineers_exp + 1}")
                    self.engineers_exp_queue.remove(self.engineers_exp_queue[i])
                    self.engineers_exp += 1
                    i -= 1

            i += 1


if __name__ == "__main__":
    # v = input("Cantidad de vendedores:")
    # t = input("Cantidad de Tecnicos:")
    # te = input("Cantidad de Tecnicos Especializados:")
    sim = HC_Simulation(2, 3, 1)
    print(sim.start())
