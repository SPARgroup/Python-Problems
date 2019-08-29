import track as vs
import neuralnetwork as nn

""""Script 3000¹"""#Respect++ Mission passed (with flying colors)
class Car(nn.Brain):
    def __init__(self):
        self.s = 0
        self.w = 0
        self.a =0
        self.image = vs.Images.car
        self.body = self.image.get_rect()
        self.theta = 0




track = vs.trackEditor()

