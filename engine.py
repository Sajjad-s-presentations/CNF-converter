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

    # Sorts the literals and lists in the formula (will be used for removing duplicate items in list)
    # The literals are in the beginning followed by lists. And the "and" list is present in the end
    def sort(self, formula):
        if (isinstance(formula, str)):
            return formula
        operator = formula[0]
        if (operator == "implies"):
            return formula
        literals = []
        propositions = []
        for index, item in enumerate(formula):
            if (index > 0):
                if (isinstance(item, str)):
                    literals.append(item)
                elif (isinstance(item, list)):
                    propositions.append(self.sort(item))
        if (len(literals) > 0):
            literals.sort()
        if (len(propositions) > 0):
            propositions = sorted(propositions, key=lambda proposition: proposition[0], reverse=True)
        newFormula = literals + propositions
        newFormula.insert(0, operator)
        return newFormula

    # Converts to CNF by taking different cases separately
    def convert(self, formula):
        if (isinstance(formula, str)):
            return formula
        elif (isinstance(formula, list)):
            # A => B    --->    ~A | B
            if (formula[0] == "implies"):
                return self.convert(["or", self.convert(["not", self.convert(formula[1])]), self.convert(formula[2])])
            # A <=> B   --->    (~A | B) & (A | ~B)
            elif (formula[0] == "iff"):
                return self.convert("and", self.convert(["or", self.convert(["not", formula[1]]), formula[2]]), self.convert(["or", formula[1], self.convert(["not", self.formula[2]])]))
            elif (formula[0] == "not"):
                # ~p
                if (isinstance(formula[1], str)):
                    return formula
                # ~~p   --->    p
                elif (isinstance(formula[1], list) and (formula[1])[0] == "not"):
                    return self.convert((formula[1])[1])
                # ~(A & B & C & ...)  --->    ~A | ~B | ~C | ....
                elif (isinstance(formula[1], list) and (formula[1])[0] == "and"):
                    disjuncts = []
                    for index, item in enumerate(formula[1]):
                        if (index > 0):
                            disjuncts.append(self.convert(["not", item]))
                    disjuncts.insert(0, "or")
                    return self.convert(disjuncts)
                # ~(A | B | C | ...)  --->    ~A & ~B & ~C & ....
                elif (isinstance(formula[1], list) and (formula[1])[0] == "or"):
                    conjuncts = []
                    for index, item in enumerate(formula[1]):
                        if (index > 0):
                            conjuncts.append(self.convert(["not", item]))
                    conjuncts.insert(0, "and")
                    return self.convert(conjuncts)
                # ~(A => B)	--->	A & ~B
                elif (isinstance(formula[1], list) and ((formula[1])[0] == "implies")):
                    return self.convert(["and", self.convert((formula[1])[1]), ["not", self.convert((formula[1][2]))]])
                elif (isinstance(formula[1], list) and (formula[1])[0] == "iff"):
                    return self.convert(["not", self.convert(formula[1])])
            elif (formula[0] == "or"):
                # A | A  --->    A
                formula = self.sort(formula)
                formula = self.removeDuplicates(formula)
                # Handling the case ["or", "A", ["or", "B", "C"]]
                formula = self.reduceOperators(formula)
                # The order will be messed up when the redundant operators are removed
                # Handling the case when the formula is reduced.
                # For instance A or A is reduced to A
                formula = self.sort(formula)
                if (len(formula) == 1):
                    return formula
                if ((isinstance(formula[-1], list) and (formula[-1])[0] == "and")):
                    # A | (B & C & D & ...)  --->  (A | B) & (A | C) & (A | D) & ...
                    conjuncts = []
                    for i, item in enumerate(formula[-1]):
                        if (i > 0):
                            conjuncts.append(["or", formula[-2], item])
                    conjuncts.insert(0, "and")
                    # If only 2 items, then remove them and also remove OR
                    if (len(formula) < 4):
                        return self.convert(conjuncts)
                    else:
                        formula.remove(formula[-1])
                        formula.remove(formula[-1])
                    formula.append(conjuncts)
                    return self.convert(formula)
                # Case A OR B,
                elif ((isinstance(formula[1], str) and isinstance(formula[2], str)) or (
                        isinstance(formula[1], str) and isinstance(formula[2], list) and (formula[2])[
                    0] == "not" and isinstance((formula[2])[1], str)) or (
                              isinstance(formula[2], str) and isinstance(formula[1], list) and (formula[1])[
                          0] == "not" and isinstance((formula[1])[1], str))):
                    formula.append(["or", formula[1], formula[2]])
                    formula.remove(formula[1])
                    formula.remove(formula[1])

                    formula = reduceOperators(formula)
                    formula = sort(formula)
                    return formula
                # Case !A OR !B
                elif (isinstance(formula[1], list) and (formula[1])[0] == "not" and isinstance((formula[1])[1],
                                                                                               str) and isinstance(
                        formula[2], list) and (formula[2])[0] == "not" and isinstance((formula[2])[1], str)):
                    return formula
                # For any other operator compute the inner operator after or
                else:
                    disjuncts = []
                    for i, item in enumerate(formula):
                        if (i > 0):
                            disjuncts.append(convert(item))
                    disjuncts.insert(0, "or")
                    return convert(disjuncts)

            elif (formula[0] == "and"):
                # Handling the case ["and", "A", ["or", "C", "D"], ["or", "D", "C"]]
                formula = sort(formula)
                formula = removeDuplicates(formula)
                # Handling the case ["and", "A", ["and", "B", "C"]]
                formula = reduceOperators(formula)
                # The order will be messed up when the redundant operators are removed
                formula = sort(formula)
                if (len(formula) == 1):
                    return formula
                disjuncts = []
                for i, item in enumerate(formula):
                    if (i > 0):
                        disjuncts.append(convert(item))
                disjuncts.insert(0, "and")

                disjuncts = reduceOperators(disjuncts)
                return disjuncts
