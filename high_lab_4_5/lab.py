class Lab:
    def __init__(self, name):
        self._name = name
        self.dead_line = "no-dead-line"
        self.descr = "difficult laboratory"
        self.passed_students = []

    def get_name(self):
        return self._name

    def __str__(self):
        return (f"name={self._name}, dead_line={self.dead_line},"
                f"descr={self.descr}, students={self.passed_students}")
