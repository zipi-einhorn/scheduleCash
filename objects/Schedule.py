class Schedule:
    def __init__(self, carrier_id):
        self.carrier_id = carrier_id
        self.legs = []

    def add_leg(self, leg):
        self.legs.append(leg)