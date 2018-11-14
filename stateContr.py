
class StateController:

    current_state = None

    states = {}

    def add_state(self, state_name, state_value):
        self.states[state_name] = state_value

    def set_state(self, state_name):
        self.current_state = state_name

    def get_state(self):
        return self.states[self.current_state]
