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
    def reduceOperators(self, formula):
        print("reduceOperators is running...")
        if (isinstance(formula, str)):
            print("isinstance is called!")
            return formula

        operator = formula[0]
        literals = []
        propositions = []

        for index, item in enumerate(formula):
            if (index > 0):
                print("condition 03: index > 0")
                if (isinstance(item, str)):
                    print("condition 04")
                    literals.append(item)
                elif (isinstance(item, list)):
                    print("condition 05")
                    propositions.append(self.reduceOperators(item))

        newFormula = literals
        for item in propositions:
            if (isinstance(item, list) and item[0] == operator):
                print("condition 06")
                for i, clause in enumerate(item):
                    if (i > 0):
                        print("condition 07")
                        newFormula.append(clause)
            else:
                print("condition 08")
                newFormula.append(item)
        newFormula.insert(0, operator)
        return newFormula

    def vlrTOlvr(self, formula):
        if(len(formula)==3):
            if(len(formula[1]) == 3):
                self.vlrTOlvr(formula[1])
                print("({}){}({})".format(formula[1], formula[0], formula[2]))

            if (len(formula[2]) == 3):
                self.vlrTOlvr(formula[2])
                print("({}){}({})".format(formula[1], formula[0], formula[2]))

    # Removes duplicate elements from "and" and "or"
    # Example : ["and", "A", "A"] should be "A"
    def removeDuplicates(self, formula):
        if (isinstance(formula, str) or (
                isinstance(formula, list) and formula[0] == "not" and isinstance(formula[1], str))):
            return formula
        for i, checkItem in enumerate(formula):
            if (i > 0):
                for j, item in reversed(list(enumerate(formula))):
                    if (j > i):
                        if (isinstance(item, list)):
                            newItem = self.removeDuplicates(item)
                            formula.insert(j, newItem)
                            formula.remove(item)
                        if (checkItem == item):
                            formula.remove(item)
        if (isinstance(formula, list) and formula[0] != "not" and len(formula) < 3):
            return formula[1]
        return formula
