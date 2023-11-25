from engine import CNF

text = ["and", "A", ["and", "B", "C"]]
cnf1 = CNF(text)
print(cnf1.reduceOperators(text))