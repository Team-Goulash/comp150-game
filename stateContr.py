
class StateController:

    current_state = None

    states = {}

    def add_state(self, state_name, state_value):
        """Adds a state to the list of states"""
        self.states[state_name] = state_value

    def set_state(self, state_name):
        """Set the current state"""
        self.current_state = state_name

    def get_state(self):
        """return the current state"""
        return self.states[self.current_state]
