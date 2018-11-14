
class Time:

    time = 0
    delta_time = 0

    def __init__(self, current_time):
        self.time = current_time
        pass

    def update_time(self, current_time):
        """Update the current time"""
        self.delta_time = current_time - self.time
        self.time = current_time
