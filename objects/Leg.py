from datetime import date


class Leg:
    def __init__(self, schedule_id, origin, destination, departure_date, arrival_date, voyage):
        self.schedule_id = schedule_id
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.duration = self.calculate_duration()
        self.voyage = voyage

    def calculate_duration(self):
        start = date.fromisoformat(self.departure_date)
        end = date.fromisoformat(self.arrival_date)
        return end - start
