from random import random, randint, randrange, choice

learning_rate = 1
class out_node():
    global learning_rate
    def __init__(self, n_input):
        self.weights = [random() for i in range(n_input)] #random weights init
        self.bias = random() #random bias
        self.n_in = n_input

    def mutate(self):
        self.weights = [s + (random() - 0.5) * learning_rate for s in self.weights]
        self.bias += (random() - 0.5) * learning_rate

    def output(self, inputs):
        out = 0
        for i in range(self.n_in):
            out += inputs[i] * self.weights[i]

        return out + self.bias

    def crossover(self, node1, node2):
        for i in range(self.n_in):
            self.weights[i] = choice([node1.weights[i], node2.weights[i]])
        self.bias = choice([node1.bias, node2.bias])

class network():
    global learning_rate
    def __init__(self, n_inputs, n_outputs, learning):
        #Number of outputs and inputs

        learning_rate = learning
        self.n_out = n_outputs
        self.n_in = n_inputs

        self.out_nodes = [out_node()] * n_outputs #n_output number of output nodes, weights are attached to output nodes

    def mutate(self):
        for out in self.out_nodes:
            out.mutate()

    def output(self, inputs):
        return [out_node.output(inputs) for out_node in self.out_nodes]

    def crossover(self, p1, p2):
        for i in range(self.n_out):
            self.out_nodes[i].crossover(p1.out_nodes[i], p2.out_nodes[i])
