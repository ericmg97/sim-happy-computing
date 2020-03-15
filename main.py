from utils import next_exp
import scipy.stats as stats
import numpy as np


class HC_Simulation():

    def __init__(self, sellers, engineers, engineers_exp):
        self.prices = {1: 0, 2: 350, 3: 500, 4: 750}
        self.serv_clients = stats.rv_discrete(
            values=([1, 2, 3, 4], [0.45, 0.25, 0.1, 0.2]))
        self.sellers = sellers
        self.engineers = engineers
        self.engineers_exp = engineers_exp

    def start(self):
        time = 0
        money = 0
        clients_queue = []
        sellers_queue = []
        engineers_queue = []
        engineers_exp_queue = []

        clients_queue.append((next_exp(20), 4))

        for time in range(480):
            if clients_queue[-1][0] <= time:
                # Tiempo para el sigiente cliente
                clients_queue.append(
                    (time + next_exp(20), self.serv_clients.rvs()))
                sellers_queue.append(clients_queue.pop(0))

            for i in range(len(sellers_queue) - 1):
                if self.sellers > 0 and sellers_queue[i][1] != 0:
                    self.sellers -= 1
                    actual = sellers_queue[i]

                    # normal(5,2) -> tiempo que demora un vendedor en atender a un cliente
                    sellers_queue[i] = (time + np.random.normal(5, 2), 0)

                    # el cliente necesita reparacion de equipos
                    if actual[1] == 1 or actual[1] == 2:
                        if self.engineers == 0 and self.engineers_exp > 0:
                            engineers_exp_queue.append(sellers_queue[i])
                        else:
                            engineers_queue.append(sellers_queue[i])

                    # el cliente necesita cambio de equipo
                    elif actual[1] == 3:
                        # es enviado con un especialista
                        engineers_exp_queue.append(sellers_queue[i])

                    # el cliente va a comprar, lo atiende el vendedor
                    elif actual[1] == 4:
                        money += 750  # realizando servicio de venta de equipos

                else:
                    if sellers_queue[i][0] <= time:
                        sellers_queue.remove(sellers_queue[i])
                        self.sellers += 1

            for i in range(len(engineers_queue) - 1):
                if self.engineers > 0 and engineers_queue[i][1] != 0:
                    self.engineers -= 1
                    actual = engineers_queue[i]

                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    engineers_queue[i] = (time + next_exp(20), 0)

                    if actual[1] == 2:
                        money += 350  # realizando servicio de reparacion sin garantia

                else:
                    if engineers_queue[i][0] <= time:
                        engineers_queue.remove(engineers_queue[i])
                        self.engineers += 1

            for i in range(len(engineers_exp_queue) - 1):
                if self.engineers_exp > 0 and engineers_exp_queue[i][1] != 0:
                    self.engineers_exp -= 1
                    actual = engineers_exp_queue[i]

                    if actual[1] == 1:
                        # exp(20) -> tiempo que demora un especialista en atender a un cliente
                        engineers_exp_queue[i] = (time + next_exp(20), 0)

                    elif actual[1] == 2:  # hay que cobrar el servicio
                        # exp(20) -> tiempo que demora un especialista en atender a un cliente
                        engineers_exp_queue[i] = (time + next_exp(20), 0)

                        money += 350  # realizando servicio de reparacion sin garantia
                    elif actual[1] == 3:
                        # exp(15) -> tiempo que demora un especialista especializado en realizar cambio de equipos
                        engineers_exp_queue[i] = (time + next_exp(15), 0)

                        money += 500  # realizando servicio de cambio de equipo

                else:
                    if engineers_exp_queue[i][0] <= time:
                        engineers_exp_queue.remove(engineers_exp_queue[i])
                        self.engineers_exp += 1

        return money


if __name__ == "__main__":
    # v = input("Cantidad de vendedores:")
    # t = input("Cantidad de Tecnicos:")
    # te = input("Cantidad de Tecnicos Especializados:")
    sim = HC_Simulation(2, 3, 1)
    print(sim.start())
