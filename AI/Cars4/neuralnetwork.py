import GeneticNetwork as gn
inps = 7 #Number of inputs = 6 lines, speed
outs = 2 #Number of outputs = acc, ang vel

class Brain(gn.network):
    def __init__(self, learn_rate):
        gn.network.__init__(self, inps, outs, learn_rate)

    def Drive(self, inputs):
        self.output(inputs)

    def Reproduce(self, parent1, parent2):
        self.crossover(parent1, parent2)




