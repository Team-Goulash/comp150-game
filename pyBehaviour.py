
class PyBehaviour:

    def update(self, inputs):
        """Update PyBehaviour

        :param inputs: user inputs
        """
        
        if inputs["forwards"]:
            self.forwards()

        if inputs["right"]:
            self.right()

        if inputs["backwards"]:
            self.backwards()

        if inputs["left"]:
            self.left()

    def forwards(self):
        pass

    def right(self):
        pass

    def backwards(self):
        pass

    def left(self):
        pass


class Transform(PyBehaviour):

    position = [0, 0]
    rotation = 0
    scale = [0, 0]
