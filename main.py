from engine import CNF
import time

# Start timer
start_time = time.time()

text = ["and", ["or", ["->", "B", "A"], ["->", "D", "C"]], ["or", ["->", "E", "F"], ["->", "G", "H"]]]

cnf1 = CNF(text)
print(cnf1.convert(text))
# End timer
end_time = time.time()
# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: {}s".format(elapsed_time))