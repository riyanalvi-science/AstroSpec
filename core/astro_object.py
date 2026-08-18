class AstroObject:

    def __init__(self, name):
        self.name = name
        self.observations = []
    def add_observation(self, observation):
        self.observations.append(observation)