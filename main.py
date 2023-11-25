from engine import CNF
import time

# Start timer
start_time = time.time()

text = ["and", "A", ["and", "B", "C"]]
text2 = ["or", ["and", "B", "A"], ["and", "B", "C"]]
cnf1 = CNF(text)
print(cnf1.reduceOperators(text))
print(cnf1.vlrTOlvr(text2))
# End timer
end_time = time.time()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: {}s".format(elapsed_time))