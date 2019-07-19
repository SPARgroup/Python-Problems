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
        set(chromosome)
        mutate()
    def playMove(self, inputs):
        """Inputs: """
    def crossover(self, parent1, parent2):
        crossPoint = rand.randint(0, len(self.weights) - 1) #L = 0, U = 2 (inclusive)
        p1 = parent1.chromosome[0:crossPoint]
        p2 = parent2.chromosome[crossPoint +1:]

        set(p1 + p2)

    def set(self, chromosome):
        self.weights=chromosome[0:len(chromosome) - 1]
        self.bias=chromosome[-1]
        self.chromosome = self.weights + [self.bias]

    def mutate(self):
        pass

def select():
    pass