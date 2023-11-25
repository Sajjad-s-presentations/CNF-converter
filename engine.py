class CNF:
    def __init__(self, propositional):
        self.propositional = propositional
        print("Constructor is called for '{}'".format(propositional))

    def __str__(self):
        print("String is called!")

    def __contains__(self):
        print("Contains is called!")