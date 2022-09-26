import sys
import re




class Node():

	def __init__(self,variant,nodes = []):

		self.value = variant
		self.children = nodes

	def Evaluate(self):

		pass




class BinOp(Node):

	def Evaluate(self):

		first_child = self.children[0].Evaluate()
		second_child = self.children[1].Evaluate()


		if self.value == "+":

			return first_child + second_child

		elif self.value == "-":

			return first_child - second_child

		elif self.value == "*":

			return first_child * second_child

		elif self.value == "/":

			return first_child // second_child

class UnOp(Node):


	def Evaluate(self):

		child = self.children[0].Evaluate()

		if self.value == "+":

			return child

		elif self.value == "-":

			return -child


class IntVal(Node):

	def Evaluate(self):

		return int(self.value)


class NoOp(Node):

	def Evaluate(self):

		pass

symbol_table = {}
class SymbolTable():

	@staticmethod
	def getter(k):

		return symbol_table[k]

	@staticmethod
	def setter(k,v):

		symbol_table[k] = v



class Identifier(Node):

	def Evaluate(self):

		return SymbolTable.getter(self.value)


class Printer(Node):

	def Evaluate(self):

		print(self.children[0].Evaluate())


class Assignment(Node):

	def Evaluate(self):

		SymbolTable.setter(self.children[0], self.children[1].Evaluate())



class Token():

	def __init__(self, data_type, value):
		self.data_type = data_type
		self.value = value

class Tokenizer():

	def __init__(self, source):
		self.source = source
		self.position = 0
		self.next = None

	def selectNext(self):

		num = ""
		text = ""
		EON = False

		if self.position < len(self.source):


			while self.source[self.position] == " ":

				self.position += 1

			if (self.source[self.position] != '+' 
			and self.source[self.position] != '-' 
			and self.source[self.position] != " " 
			and self.source[self.position] != "*" 
			and self.source[self.position] != "/"
			and self.source[self.position] != "("
			and self.source[self.position] != ")"
			and self.source[self.position] != "{"
			and self.source[self.position] != "}"
			and self.source[self.position] != ";"
			and self.source[self.position] != "="):

				if self.source[self.position].isalpha():
					while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):

						text += self.source[self.position]
						self.position += 1

					if text == "Print":

						self.next = Token("PRINT", text)

					else:

						self.next = Token("IDENT", text)

					return self.next

				if self.source[self.position].isdigit():
					num += self.source[self.position]

				if self.position != (len(self.source)-1):
					for i in range(self.position, len(self.source)):
						if not EON:
							if i != (len(self.source) - 1):
								if self.source[i+1] != '+' and self.source[i+1] != '-' and self.source[i+1] != "*" and self.source[i+1] != "/" and self.source[i+1] != "(" and self.source[i+1] != ")" and self.source[i+1] != "{" and self.source[i+1] != "}" and self.source[i+1] != ";" and self.source[i+1] != "=":
									if not self.source[i+1].isdigit():
										EON = True

									else:
										num += self.source[i+1]

								else:

									EON = True

							else:

								EON = True
				else:

					EON = True

			elif self.source[self.position] == '+':

				self.next = Token("PLUS", self.source[self.position])

				while self.source[self.position + 1] == " ":
					self.position += 1

				self.position += 1

				return self.next


			elif self.source[self.position] == "-":

				self.next = Token("MINUS", self.source[self.position])

				while self.source[self.position + 1] == " ":
					self.position += 1

				self.position += 1
				return self.next

			elif self.source[self.position] == " ":
				self.next= Token("BLANK", self.source[self.position])


				while self.source[self.position + 1] == " ":
					self.position += 1
				
				self.position += 1

				return self.next

			elif self.source[self.position] == "*":
				self.next = Token("MULT", self.source[self.position])


				while self.source[self.position + 1] == " ":
					self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "/":
				self.next = Token("DIV", self.source[self.position])

				while self.source[self.position + 1] == " ":
					self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "(":
				self.next = Token("OPENP", self.source[self.position])

				while self.source[self.position + 1] == " ":
					self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == ")":
				self.next = Token("CLOSEP", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "{":
				self.next = Token("OPENBR", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "}":
				self.next = Token("CLOSEBR", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "=":
				self.next = Token("EQUAL", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == ";":
				self.next = Token("SEMI_C", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			if num != "" and EON == True:

				self.next = Token("INT", int(num))
				self.position += len(num)
				num = ""
				EON = False
				return self.next

		

		self.next = Token("EOF", "EOF")
		return self.next

class Parser():


	@staticmethod
	def parseBlock(token):

		nodes = []
		# token.selectNext()

		if token.next.data_type == "OPENBR":

			token.selectNext()

			while token.next.data_type != "CLOSEBR":

				nodes.append(Parser.parseStatement(token))

		token.selectNext()
		return nodes

	@staticmethod
	def parseStatement(token):

		output = NoOp(None)

		if token.next.data_type == "IDENT":

			output = token.next.value
			token.selectNext()

			if token.next.data_type == "EQUAL":

				token.selectNext()

				output = Assignment("=",[output,Parser.parseExpression(token)])

				if token.next.data_type == "SEMI_C":

					# token.selectNext()
					return output

				else:
					raise ValueError("Missing semi-colon token.")

			else:

				raise ValueError("Missing Value.")

		elif token.next.data_type == "PRINT":
			
			token.selectNext()

			if token.next.data_type == "OPENP":

				token.selectNext()
				exp = Parser.parseExpression(token)

				if token.next.data_type == "CLOSEP":

					output = Printer("PRINT", [exp])
					token.selectNext()

					if token.next.data_type == "SEMI_C":

						token.selectNext()
						return output

					else:

						raise ValueError("Missing semi-colon token.")

				else:

					raise ValueError("Missing Closing Parenthesis")

			else:

				raise ValueError("Syntax Error (Printf).")


		elif token.next.data_type == "SEMI_C":

			token.selectNext()
			return output

		else:

			raise ValueError("Invalid Expression.")





	@staticmethod
	def parseTerm(token):

		output = Parser.parseFactor(token)

		while token.next.data_type == "MULT" or token.next.data_type == "DIV":
			
			if token.next.data_type == "MULT":

				op = token.next.value

				token.selectNext()
				output = BinOp(op, [output, Parser.parseFactor(token)])

			elif token.next.data_type == "DIV":

				op = token.next.value
				token.selectNext()
				output = BinOp(op, [output, Parser.parseFactor(token)])

		return output


	@staticmethod
	def parseExpression(token):

		output = Parser.parseTerm(token)

		while token.next.data_type == "PLUS" or token.next.data_type == "MINUS":

			if token.next.data_type == "PLUS":

				op = token.next.value

				token.selectNext()
				output = BinOp(op, [output,Parser.parseTerm(token)])

			if token.next.data_type == "MINUS":

				op = token.next.value
				token.selectNext()
				output = BinOp(op, [output, Parser.parseTerm(token)])


		return output

	@staticmethod
	def parseFactor(token):

		if token.next.data_type == "INT":		
			
			output = IntVal(token.next.value, [token.next.value])
			token.selectNext()
			

		elif token.next.data_type == "PLUS":

			token.selectNext()
			output = UnOp("+", [Parser.parseFactor(token)])

		elif token.next.data_type == "MINUS":

			token.selectNext()
			output = UnOp("-", [Parser.parseFactor(token)])

		elif token.next.data_type == "OPENP":

			token.selectNext()
			output = Parser.parseExpression(token)

			if 	token.next.data_type != "CLOSEP":

				raise ValueError("Missing Closing parenthesis.")

			token.selectNext()

		elif token.next.data_type == "CLOSEP":

			raise ValueError("Missing Opening Paranthesis.")


		elif token.next.data_type == "IDENT":

			output = Identifier(token.next.value)
			token.selectNext()


		return output



	@staticmethod
	def run(code):

		string = PrePro.filter(code)
		token = Tokenizer(string)
		token.selectNext()

		result = Parser.parseBlock(token)

		if result != None and token.next.data_type == "EOF":
			
			for i in result:
				i.Evaluate()

		else:

			raise ValueError("Invalid Expression")





class PrePro():

	@staticmethod
	def filter(code):
		f = re.sub(re.compile("//.*?\n"),"",code)

		f = re.sub("\s+","",f)
		return f.replace("\n","")

		






with open(sys.argv[1], "r") as file:

	Parser.run(file.read())













