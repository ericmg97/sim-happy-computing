from tools import inverse_method, exponential, normal, daytime

class HC_Simulation():

    def __init__(self, sellers:int, engineers:int, engineers_exp:int):
        self.serv_clients = [(1, 0.45), (2, 0.25), (3, 0.1), (4, 0.2)]
        self.clients_queue = []

        self.sellers = int(sellers)
        self._sellers = self.sellers
        self.sellers_queue = []

        self.engineers = int(engineers)
        self._engineers = self.engineers
        self.engineers_queue = []

        self.engineers_exp = int(engineers_exp)
        self._engineers_exp = self.engineers_exp
        self.engineers_exp_queue = []

        self.report = [0]*5
        self.gain = 0

        self.time = 0

    def reset(self, sellers = None, engineers = None, engineers_exp = None):
        if sellers is None:
            sellers = self._sellers
        if engineers is None:
            engineers = self._engineers
        if engineers_exp is None:
            engineers_exp = self._engineers_exp

        self.__init__(sellers, engineers, engineers_exp)
    
    def start(self, total_time):
        # Cliente -----------> (Tiempo de llegada, Tipo de servicio, No. Cliente, En Espera)
        next_arrival = exponential(1/20)
        self.clients_queue.append( (next_arrival, inverse_method(self.serv_clients), 1, False))

        print()

        for time in range(total_time):
            self.time = time

            # 480min = 8horas Jornada Laboral
            if self.clients_queue[-1][0] <= self.time and self.time < 480:
                print(f"{ daytime(self.time) } -> Cliente {self.clients_queue[-1][2]} llega al taller.")
                self.report[0] += 1

                # Tiempo para la llegada del sigiente cliente
                next_arrival = self.time + exponential(1/20)
                    
                self.clients_queue.append((next_arrival, inverse_method(self.serv_clients), self.clients_queue[-1][2] + 1, False))
                self.sellers_queue.append(self.clients_queue.pop(0))

            self._sellers_work()

            self._engineers_work()

            self._engineers_exp_work()

        print()
        print(f"Se atendieron un total de {self.report[0]} clientes:")
        print(f"    {self.report[1]} reparaciones con garantia")
        print(f"    {self.report[2]} reparaciones sin garantia")
        print(f"    {self.report[3]} cambio de equipos")
        print(f"    {self.report[4]} venta de equipos \n")
        print(f"La ganancia fue de: {self.gain}")

    def _sellers_work(self):
        i = 0
        while True:
            if i >= len(self.sellers_queue):
                break

            if self.sellers > 0 and not self.sellers_queue[i][3]:
                self.sellers -= 1

                # normal(5,2) -> tiempo que demora un vendedor en atender a un cliente
                time_to_finish = self.time + normal(5, 2)

                actual = (time_to_finish, self.sellers_queue[i][1], self.sellers_queue[i][2], True)

                print(f"{ daytime(self.time) } -> Cliente {actual[2]} siendo atendido por vendedor. ")
                
                self.sellers_queue[i] = actual

                # el cliente va a comprar, lo atiende el vendedor
                if self.sellers_queue[i][1] == 4:
                    print(f"\t Cliente {self.sellers_queue[i][2]} comprando equipo.")
                    self.report[4] += 1
                    self.gain += 750  # realizando servicio de venta de equipos

            else:
                if self.sellers_queue[i][0] <= self.time and self.sellers_queue[i][3]:
                    print(f"{ daytime(self.time) } -> Cliente {self.sellers_queue[i][2]} fue atendido por vendedor.")

                    actual = (self.sellers_queue[i][0], self.sellers_queue[i][1], self.sellers_queue[i][2], False)

                    # el cliente necesita reparacion de equipos
                    if self.sellers_queue[i][1] == 1 or self.sellers_queue[i][1] == 2:
                        
                        if self.engineers == 0 and self.engineers_exp > 0:
                            for client in self.clients_queue:
                                if client[1] == 3:
                                    self.engineers_queue.append(actual)
                                    break
                            else:
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

                print(f"{ daytime(self.time) } -> Cliente {self.engineers_queue[i][2]} siendo atendido por tecnico. ")

                # exp(20) -> tiempo que demora un especialista en atender a un cliente
                time_to_finish = actual[0] + exponential(1/20)
                self.engineers_queue[i] = (time_to_finish, actual[1], actual[2], True)
                
                if actual[1] == 1: # realizando servicio de reparacion con garantia
                    print(f"\t Cliente {self.engineers_queue[i][2]} reparacion con garantia por tecnico.")
                    self.report[1] += 1
                elif actual[1] == 2: # realizando servicio de reparacion sin garantia
                    print(f"\t Cliente {self.engineers_queue[i][2]} reparacion sin garantia por tecnico.")
                    self.report[2] += 1
                    self.gain += 350

            else:
                if self.engineers_queue[i][0] <= self.time and self.engineers_queue[i][3]:
                    print(f"{ daytime(self.time) } -> Cliente {self.engineers_queue[i][2]} fue atendido por tecnico.")
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

                print(f"{ daytime(self.time) } -> Cliente {self.engineers_exp_queue[i][2]} siendo atendido por tecnico especialista. ")
                
                if actual[1] == 1:

                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    time_to_finish = actual[0] + exponential(1/20)
                    self.engineers_exp_queue[i] = (time_to_finish, actual[1], actual[2], True)

                    print(f"\t Cliente {self.engineers_exp_queue[i][2]} reparacion con garantia por tecnico especialista.")
                    self.report[1] += 1

                elif actual[1] == 2: # realizando servicio de reparacion sin garantia
                    # exp(20) -> tiempo que demora un especialista en atender a un cliente
                    time_to_finish = actual[0] + exponential(1/20)

                    self.engineers_exp_queue[i] = (time_to_finish, actual[1], actual[2], True)
                    print(f"\t Cliente {self.engineers_exp_queue[i][2]} reparacion sin garantia por tecnico especialista.")
                    self.report[2] += 1

                    self.gain += 350  
                elif actual[1] == 3: # realizando servicio de cambio de equipos
                    # exp(15) -> tiempo que demora un especialista especializado en realizar cambio de equipos
                    time_to_finish = actual[0] + exponential(1/15)
                    self.engineers_exp_queue[i] = (time_to_finish, actual[1], actual[2], True)

                    print(f"\t Cliente {self.engineers_exp_queue[i][2]} cambio de equipos.")
                    self.report[3] += 1

                    self.gain += 500

            else:
                if self.engineers_exp_queue[i][0] <= self.time and self.engineers_exp_queue[i][3]:
                    print(f"{ daytime(self.time) } -> Cliente {self.engineers_exp_queue[i][2]} fue atendido por tecnico especialista.")
                    self.engineers_exp_queue.remove(self.engineers_exp_queue[i])
                    self.engineers_exp += 1
                    i -= 1

            i += 1


if __name__ == "__main__":
    v = input("Cantidad de vendedores:")
    t = input("Cantidad de Tecnicos:")
    te = input("Cantidad de Tecnicos Especializados:")

    sim = HC_Simulation(v, t, te)

    sim.start(1000)
