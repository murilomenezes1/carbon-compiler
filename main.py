import sys
import re


string = sys.argv[1].replace(" ","")
res = 0

vector = re.split("(\D)", string) #splits string on every non-digit char (+ or -)

for i in range(0, len(vector)):
	if i == 0 and (vector[i] != "+" and vector[i] != "-"):

		res += int(vector[i])

	elif vector[i] == "+":

		res += int(vector[i+1])

	elif vector[i] == "-":

		res -= int(vector[i+1])



print(res)










