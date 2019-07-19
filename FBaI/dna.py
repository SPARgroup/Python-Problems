import numpy
import random as rand

generation = []

class ai:
    """Components:
        1. Chromosomes
        2. Generation
        3. Selection
        4. Crossover
        5. Mutation

        Number of inputs: Distance, Height from pipe gap"""

    def __init__(self, chromosome):
        self.set(chromosome)
        self.mutate()

    def playMove(self, inputs):
        """Inputs: """
        activation = 0

        for i in range(3):
            activation += self.weights[i] * inputs[i]

        activation += self.bias

        if activation >= 0:
            return True
        else:
            return False

    def crossover(self, parent1, parent2):
        crossPoint = rand.randint(0, len(self.weights)) #L = 0, U = 2 (inclusive)
        p1 = parent1.chromosome[0:crossPoint]
        p2 = parent2.chromosome[crossPoint +1:]
        self.set(p1 + p2)

    def set(self, chromosome):
        self.weights = chromosome[0:len(chromosome) - 1]
        self.bias=chromosome[-1]
        self.chromosome = self.weights + [self.bias]

    def mutate(self):
        new = []
        for gene in self.chromosome:
            new.append(gene + rand.random())
        pass

def select():
    pass