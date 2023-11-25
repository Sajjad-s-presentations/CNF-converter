class CNF:
    def __init__(self, propositional):
        self.propositional = propositional
        print("Constructor is called for '{}'".format(propositional))

    def __str__(self):
        print("String is called!")

    def __contains__(self):
        print("Contains is called!")

    # Reduces the operators, if "and" is present inside "and" or "or" inside "or"
    # Example : ["and", "A", ["and", "B", "C"]] should be ["and", "A", "B", "C"]
    def reduceOperators(self):
        if (isinstance(self.propositional, str)):
            return self.propositional
        operator = self.propositional[0]
        literals = []
        propositions = []
        for index, item in enumerate(self.propositional):
            if (index > 0):
                if (isinstance(item, str)):
                    literals.append(item)
                elif (isinstance(item, list)):
                    propositions.append(self.reduceOperators(item))
        newFormula = literals
        for item in propositions:
            if (isinstance(item, list) and item[0] == operator):
                for i, clause in enumerate(item):
                    if (i > 0):
                        newFormula.append(clause)
            else:
                newFormula.append(item)
        newFormula.insert(0, operator)
        return newFormula