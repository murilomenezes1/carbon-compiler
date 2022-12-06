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

		if first_child[1] == "i32" and second_child[1] == "i32":

			if self.value == "+":

				return (first_child[0] + second_child[0], "i32")

			elif self.value == "-":

				return (first_child[0] - second_child[0], "i32")

			elif self.value == "*":

				return (first_child[0] * second_child[0], "i32")

			elif self.value == "/":

				return (first_child[0] // second_child[0], "i32")

			elif self.value == "==":

				return (int(first_child[0] == second_child[0]), "i32")

			elif self.value == ">":

				return (int(first_child[0] > second_child[0]), "i32")

			elif self.value == "<":

				return (int(first_child[0] < second_child[0]), "i32")

			elif self.value == "||":

				return (first_child[0] or second_child[0], "i32")

			elif self.value == "&&":

				return (first_child[0] and second_child[0], "i32")

			elif self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

		if first_child[1] == "String" and second_child[1] == "String":

			if self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

			if self.value == "==":

				return (int(str(first_child[0]) == str(second_child[0])), "i32")

			if self.value == "<":

				return (int(first_child[0]) < str(second_child[0]),"i32")

			if self.value == ">":

				return (int(first_child[0]) > str(second_child[0]),"i32")

		if first_child[1] == "String" or second_child[1] == "String":

			if self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

			if self.value == "==":

				return (int(first_child[0] == second_child[0]), "i32")



class UnOp(Node):


	def Evaluate(self):

		child = self.children[0].Evaluate()


		if child[1] == "i32":

			if self.value == "+":

				return (child[0],"i32")

			elif self.value == "-":

				return (-child[0], "i32")

			elif self.value == "!":

				return (not(child[0]), "i32")

		else:

			raise ValueError("Invalid Data Type (UnOp).")


class IntVal(Node):

	def Evaluate(self):

		return (int(self.value),"i32")

class StrVal(Node):

	def Evaluate(self):

		return (str(self.value),"String")

class VarDec(Node):

	def Evaluate(self):

		var = self.value
		for i in self.children:
			SymbolTable.creator(i.value,var)




class NoOp(Node):

	def Evaluate(self):

		pass

symbol_table = {}
class SymbolTable():

	@staticmethod
	def creator(var,type):

		if var in symbol_table:
			raise ValueError("Invalid ST.")
		else:

			symbol_table[var] = (None,type)

	@staticmethod
	def getter(k):

		return symbol_table[k]

	@staticmethod
	def setter(k,v):

		if k in symbol_table:
			if v[1] == symbol_table[k][1]:
				symbol_table[k] = v
			else:

				raise ValueError("Invalid Data Type in ST.")

		else:

			 raise ValueError("Var not in ST.")



class Identifier(Node):

	def Evaluate(self):

		st = SymbolTable.getter(self.value)

		return (st[0],st[1])


class Printer(Node):

	def Evaluate(self):


		print(self.children[0].Evaluate()[0])


class Block(Node):

	def Evaluate(self):

		for child in self.children:

			child.Evaluate()



class Assignment(Node):

	def Evaluate(self):

		SymbolTable.setter(self.children[0], self.children[1].Evaluate())

class Reader(Node):

	def Evaluate(self):
		return (int(input()),"i32")

class If(Node):

	def Evaluate(self):

		first_child = self.children[0]
		second_child = self.children[1]

		if first_child.Evaluate():
			second_child.Evaluate()

		elif len(self.children) > 2:
			self.children[2].Evaluate()


class While(Node):

	def Evaluate(self):
		
		first_child = self.children[0]
		second_child = self.children[1]

		while (first_child.Evaluate()[0]):
			second_child.Evaluate()






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
		words = ["Print", "Read","if","else","while","var","String","i32"]

		
		while self.position < len(self.source) and self.source[self.position] == " ":

			self.position += 1

		if self.position < len(self.source):

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
			and self.source[self.position] != "="
			and self.source[self.position] != "!"
			and self.source[self.position] != "<"
			and self.source[self.position] != ">"
			and self.source[self.position] != "|"
			and self.source[self.position] != "&"
			and self.source[self.position] != ":"
			and self.source[self.position] != "."
			and self.source[self.position] != ","
			and self.source[self.position] != "\""):

				if self.source[self.position].isalpha():
					while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):

						text += self.source[self.position]
						self.position += 1
					if text in words:
						if text == "String":
							self.next = Token("TYPE", "String")
							# self.position += 1
							return self.next

						elif text == "i32":
							self.next = Token("TYPE", "i32")
							# self.position += 1
							return self.next
						else:
							self.next = Token(text.upper(),text)
							# self.position +=1
							return self.next

					else:
						self.next = Token("IDENT", text)
						# self.position += 1
						return self.next

				if self.source[self.position].isdigit():
					num += self.source[self.position]

				if self.position != (len(self.source)-1):
					for i in range(self.position, len(self.source)):
						if not EON:
							if i != (len(self.source) - 1):
								if self.source[i+1] != '+' and self.source[i+1] != '-' and self.source[i+1] != "*" and self.source[i+1] != "/" and self.source[i+1] != "(" and self.source[i+1] != ")" and self.source[i+1] != "{" and self.source[i+1] != "}" and self.source[i+1] != ";" and self.source[i+1] != "=" and self.source[i+1] != ";" and self.source[i+1] != "<" and self.source[i+1] != ">" and self.source[i+1] != "|" and self.source[i+1] != "!" and self.source[i+1] != "&" and self.source[i+1] != ":" and self.source[i+1] != "." and self.source[i+1] != "\"":
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

				# if self.position + 1 < len(self.source):	
				# 	while self.source[self.position + 1] == " ":
				# 		self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "=":
				if self.source[self.position+1] == "=":
					self.next = Token("COMPARE", "==")
					self.position += 1
				else:
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

			elif self.source[self.position] == "!":
				self.next = Token("NOT", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == ">":
				self.next = Token("GREATER", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "<":
				self.next = Token("LESS", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == "|":
				if self.source[self.position+1] == "|":

					self.next = Token("OR", "||")

					if self.position + 1 < len(self.source):	
						while self.source[self.position + 1] == " ":
							self.position += 1

					self.position += 2

					return self.next

			elif self.source[self.position] == "&":
				if self.source[self.position+1] == "&":

					self.next = Token("AND", "&&")

					if self.position + 1 < len(self.source):	
						while self.source[self.position + 1] == " ":
							self.position += 1

					self.position += 2

					return self.next	

			elif self.source[self.position] == ":":
				self.next = Token("COLON", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == ".":
				self.next = Token("DOT", self.source[self.position])

				if self.position + 1 < len(self.source):	
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next

			elif self.source[self.position] == ",":
				self.next = Token("COMMA", self.source[self.position])

				if self.position + 1 < len(self.source):
					while self.source[self.position + 1] == " ":
						self.position += 1

				self.position += 1

				return self.next


			if self.source[self.position] == "\"":

				string = ""
				self.position += 1

				while self.source[self.position] != "\"":
					string += self.source[self.position]

					self.position += 1

				self.position += 1
				self.next = Token("STRING", string)

				return self.next	





			if num != "" and EON == True:

				self.next = Token("INT", int(num))
				self.position += len(num)
				num = ""
				EON = False
				return self.next

		
		else:
			self.next = Token("EOF", "EOF")
			return self.next

class Parser():


	@staticmethod
	def parseBlock(token):


		# token.selectNext()

		if token.next.data_type == "OPENBR":

			token.selectNext()

			nodes = Block("",[])

			while token.next.data_type != "CLOSEBR":

				if token.next.value == "EOF":
					raise ValueError("Missing }.")

				else:

					nodes.children.append(Parser.parseStatement(token))


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

				output = Assignment("=",[output,Parser.parseRelEx(token)])

				if token.next.data_type == "SEMI_C":

					token.selectNext()
					return output

				else:
					raise ValueError("Missing semi-colon token.")

			else:

				raise ValueError("Missing Value.")

		elif token.next.data_type == "PRINT":
			
			token.selectNext()

			if token.next.data_type == "OPENP":

				token.selectNext()

				exp = Parser.parseRelEx(token)


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

		elif token.next.data_type == "IF":
			token.selectNext()
			if token.next.data_type == "OPENP":
				token.selectNext()
				par1 = Parser.parseRelEx(token)

				if token.next.data_type == "CLOSEP":
					token.selectNext()
					par2 = Parser.parseStatement(token)


					if token.next.data_type == "ELSE":

						token.selectNext()
						par3 = Parser.parseStatement(token)


						output = If("",[par1,par2,par3])

					else:
						output = If("",[par1,par2])

					return output

				else:
					raise ValueError("Missing Closing Parenthesis.")

			else:
				raise ValueError("Missing Opening Parenthesis.")


		elif token.next.data_type == "WHILE":
			token.selectNext()
			if token.next.data_type == "OPENP":
				token.selectNext()
				par1 = Parser.parseRelEx(token)

				if token.next.data_type == "CLOSEP":

					token.selectNext()
					par2 = Parser.parseStatement(token)
					output = While("", [par1,par2])
					return output

				else:

					raise ValueError("Missing Closing Parenthesis.")

			else:

				raise ValueError("Missing Opening Parenthesis.")

		elif token.next.data_type == "VAR":
			token.selectNext()

			if token.next.data_type == "IDENT":

				var = [Identifier(token.next.value)]
				token.selectNext()

				while token.next.data_type == "COMMA":
					token.selectNext()
					if token.next.data_type == "IDENT":
						var.append(Identifier(token.next.value))


					else:

						raise ValueError("Invalid token [,].")

					token.selectNext()
				if token.next.data_type == "COLON":

					token.selectNext()

				else:

					raise ValueError("Missing ':'")

				if token.next.data_type == "TYPE":
					var_type = token.next.value

				token.selectNext()



				if token.next.data_type == "SEMI_C":
					token.selectNext()
					return VarDec(var_type,var)

				else:

					raise ValueError("Missing semi-colon")

			else:

				raise ValueError("Invalid var name.")

		else:

			return Parser.parseBlock(token)





	@staticmethod
	def parseTerm(token):

		output = Parser.parseFactor(token)


		while token.next.data_type == "MULT" or token.next.data_type == "DIV" or token.next.data_type == "AND":
			
			if token.next.data_type == "MULT":

				op = token.next.value

				token.selectNext()
				output = BinOp(op, [output, Parser.parseFactor(token)])

			elif token.next.data_type == "DIV":


				op = token.next.value
				token.selectNext()
				output = BinOp(op, [output, Parser.parseFactor(token)])

			elif token.next.data_type == "AND":

				op = token.next.value
				token.selectNext()
				output = BinOp(op, [output, Parser.parseFactor(token)])

		return output


	@staticmethod
	def parseExpression(token):

		output = Parser.parseTerm(token)

		while token.next.data_type == "PLUS" or token.next.data_type == "MINUS" or token.next.data_type == "OR":

			if token.next.data_type == "PLUS":

				op = token.next.value

				token.selectNext()
				output = BinOp(op, [output,Parser.parseTerm(token)])

			if token.next.data_type == "MINUS":

				op = token.next.value
				token.selectNext()
				output = BinOp(op, [output, Parser.parseTerm(token)])

			if token.next.data_type == "OR":

				op = token.next.value
				token.selectNext()
				output = BinOp(op,[output, Parser.parseTerm(token)])

		return output

	@staticmethod
	def parseFactor(token):

		if token.next.data_type == "INT":		
			
			output = IntVal(token.next.value, [token.next.value])
			token.selectNext()


		elif token.next.data_type == "STRING":

			value = token.next.value
			output = StrVal(value)
			token.selectNext()

			

		elif token.next.data_type == "PLUS":

			token.selectNext()
			output = UnOp("+", [Parser.parseFactor(token)])

		elif token.next.data_type == "MINUS":

			token.selectNext()
			output = UnOp("-", [Parser.parseFactor(token)])

		elif token.next.data_type == "OPENP":

			token.selectNext()
			output = Parser.parseRelEx(token)

			if 	token.next.data_type != "CLOSEP":

				raise ValueError("Missing Closing parenthesis.")

			token.selectNext()

		elif token.next.data_type == "CLOSEP":

			raise ValueError("Missing Opening Paranthesis.")


		elif token.next.data_type == "IDENT":

			output = Identifier(token.next.value)
			token.selectNext()


		elif token.next.data_type == "READ":

			token.selectNext()
			if token.next.data_type == "OPENP":
				token.selectNext()
				if token.next.data_type == "CLOSEP":
					token.selectNext()
					output = Reader("")
				else:
					raise ValueError("Missing Clsoing Parenthesis.")

			else:

				raise ValueError("Missing Opening Parenthesis.")


		elif token.next.data_type == "NOT":

			token.selectNext()
			output = UnOp("!",[Parser.parseFactor(token)])


		return output


	@staticmethod
	def parseRelEx(token):

		output = Parser.parseExpression(token)
		# print("output: ", output)

		while token.next.data_type == "GREATER" or token.next.data_type == "LESS" or token.next.data_type == "COMPARE" or token.next.data_type == "DOT":

			if token.next.data_type == "GREATER":
				op = token.next.value
				token.selectNext()
				output = BinOp(op,[output, Parser.parseExpression(token)])

			if token.next.data_type == "LESS":
				op = token.next.value
				token.selectNext()
				output = BinOp(op,[output, Parser.parseExpression(token)])

			if token.next.data_type == "COMPARE":
				op = token.next.value
				# print("op:",op)
				token.selectNext()
				# print(token.next.value)
				output = BinOp(op,[output, Parser.parseExpression(token)])

			if token.next.data_type == "DOT":

				op = token.next.value
				token.selectNext()
				output = BinOp(op,[output, Parser.parseExpression(token)])
		
		return output



	@staticmethod
	def run(code):

		string = PrePro.filter(code)
		token = Tokenizer(string)
		token.selectNext()

		result = Parser.parseBlock(token)

		if result != None and token.next.data_type == "EOF":
			
			
			result.Evaluate()

		else:

			raise ValueError("Invalid Expression")





class PrePro():

	@staticmethod
	def filter(code):
		f = re.sub(re.compile("//.*?\n"),"",code)

		f = re.sub("\s+"," ",f)
		return f.replace("\n","")

		






with open(sys.argv[1], "r") as file:

	Parser.run(file.read())













