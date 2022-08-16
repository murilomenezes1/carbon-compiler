import sys
import re


string = sys.argv[1].replace(" ","")
res = 0

for i in range(0,len(string)):

	if (i == 0) and (string[i] == "+" or string[i] == "-"):

		sys.stderr.write("String must begin with a number.\n")
		raise ValueError

	if (i == 0) and (string[i] != "+" and string[i] != "-"): 

		res += int(string[i])

	elif string[i] == "+" and (string[i+1] != "+" and string[i+1] != "-"):

		res += int(string[i+1])

	elif string[i] == "-" and (string[i+1] != "+" and string[i+1] != "-"):

		res -= int(string[i+1])



print(res)






