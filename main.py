from utils import next_exp
import scipy.stats as stats
import numpy as np

class HC_Simulation():

    def __init__(self, sellers, engineers, engineers_exp):
        self.prices = {1: 0, 2: 350, 3: 500, 4: 750}
        self.serv_clients = stats.rv_discrete(values=([1,2,3,4],[0.45,0.25,0.1,0.2]))
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
                clients_queue.append((time + next_exp(20), self.serv_clients.rvs())) #Tiempo para el sigiente cliente
                sellers_queue.append(clients_queue.pop(0))

            for i in range(len(sellers_queue)):
                if self.sellers > 0 and sellers_queue[i][1] != 0:
                    self.sellers -= 1
                    actual = sellers_queue[i]
                    sellers_queue[i] = (time + np.random.normal(5, 2), 0)
                    
                    if actual[1] == 4:
                        pass #lo atiende el vendedor
                    elif actual[1] == 3:            
                        engineers_exp_queue.append(sellers_queue[i])
                    else:
                        pass #terminar
                else:
                    if sellers_queue[i][0] <= time:
                        sellers_queue.remove(sellers_queue[i])
                        self.sellers += 1

            if self.engineers > 0 and len(engineers_queue) > 0:
                pass

            if self.engineers_exp > 0 and len(engineers_exp_queue) > 0:
                pass
                        

if __name__ == "__main__":
    # v = input("Cantidad de vendedores:")
    # t = input("Cantidad de Tecnicos:")
    # te = input("Cantidad de Tecnicos Especializados:")
    sim = HC_Simulation(2, 3, 1)
    sim.start()
