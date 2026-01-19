import sys
import io 

input_buffer = io.StringIO()

input_buffer.write("2\n"+"3\n"+"5\n")
input_buffer.seek(0)
sys.stdin = input_buffer

input1 = input("Input 1:\n")
input2 = input("Input 2:\n")
input3 = input("Input 3:\n")

print("Printing Output")
print(input1)
print(input2)

