import sys
import re




class Node():

	i = 0

	def __init__(self,variant,nodes = []):

		self.value = variant
		self.children = nodes

	def Evaluate(self):

		pass

	def newId():

		Node.i += 1

		return Node.i




class BinOp(Node):

	def Evaluate(self):

		self.id = Node.newId()
		first_child = self.children[0].Evaluate()
		assembler.addOutput("PUSH EBX")
		second_child = self.children[1].Evaluate()
		assembler.addOutput("POP EAX")

		if first_child[1] == "i32" and second_child[1] == "i32":

			if self.value == "+":

				assembler.addOutput("ADD EAX, EBX")
				assembler.addOutput("MOV EBX, EAX")

				return (first_child[0] + second_child[0], "i32")

			elif self.value == "-":

				assembler.addOutput("SUB EAX, EBX")
				assembler.addOutput("MOV EBX, EAX")

				return (first_child[0] - second_child[0], "i32")

			elif self.value == "*":


				assembler.addOutput("IMUL EBX")
				assembler.addOutput("MOV EBX, EAX")
				return (first_child[0] * second_child[0], "i32")

			elif self.value == "/":

				assembler.addOutput("IDIV EBX")
				assembler.addOutput("MOV EBX, EAX")
				return (first_child[0] // second_child[0], "i32")

			elif self.value == "==":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_je")
				return (int(first_child[0] == second_child[0]), "i32")

			elif self.value == ">":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_jg")
				return (int(first_child[0] > second_child[0]), "i32")

			elif self.value == "<":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_jl")
				return (int(first_child[0] < second_child[0]), "i32")

			elif self.value == "||":

				assembler.addOutput("OR EBX, EAX")
				return (first_child[0] or second_child[0], "i32")

			elif self.value == "&&":

				assembler.addOutput("AND EBX, EAX")
				return (first_child[0] and second_child[0], "i32")

			elif self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

		if first_child[1] == "String" and second_child[1] == "String":

			if self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

			if self.value == "==":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_je")
				return (int(str(first_child[0]) == str(second_child[0])), "i32")

			if self.value == "<":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_jl")
				return (int(str(first_child[0]) < str(second_child[0])),"i32")

			if self.value == ">":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_jg")
				return (int(str(first_child[0]) > str(second_child[0])),"i32")

		if first_child[1] == "String" or second_child[1] == "String":

			if self.value == ".":

				return (str(str(first_child[0]) + str(second_child[0])),"String")

			if self.value == "==":

				assembler.addOutput("CMP EAX, EBX")
				assembler.addOutput("CALL binop_je")
				return (int(first_child[0] == second_child[0]), "i32")



class UnOp(Node):


	def Evaluate(self):

		child = self.children[0].Evaluate()


		if child[1] == "i32":

			if self.value == "+":

				assembler.addOutput("ADD EBX, 0")
				return (child[0],"i32")

			elif self.value == "-":

				assembler.addOutput("MOV EAX, {}".format(child[0]))
				assembler.addOutput("MOV EBX, -1")
				assembler.addOutput("IMUL EBX")
				assembler.addOutput("MOV EBX, EAX")
				return (-child[0], "i32")

			elif self.value == "!":

				assembler.addOutput("NEG EBX")
				return (not(child[0]), "i32")

		else:

			raise ValueError("Invalid Data Type (UnOp).")


class IntVal(Node):

	def Evaluate(self):

		assembler.addOutput("MOV EBX, " + str(self.value))
		return (int(self.value),"i32")

class StrVal(Node):

	def Evaluate(self):

		return (str(self.value),"String")

class VarDec(Node):

	def Evaluate(self):

		var = self.value
		for i in self.children:
			SymbolTable.creator(i.value,var)
			assembler.addOutput("PUSH DWORD 0")




class NoOp(Node):

	def Evaluate(self):

		pass

symbol_table = {}
class SymbolTable():

	stat = 0 

	@staticmethod
	def creator(var,type):

		SymbolTable.stat += 4
		if var in symbol_table:
			raise ValueError("Invalid ST.")
		else:

			symbol_table[var] = [None,type, SymbolTable.stat]

	@staticmethod
	def getter(k):

		return symbol_table[k]

	@staticmethod
	def setter(k,v):

		if k in symbol_table:
			if v[1] == symbol_table[k][1]:
				symbol_table[k][0] = v[0]
			else:

				raise ValueError("Invalid Data Type in ST.")

		else:

			 raise ValueError("Var not in ST.")



class Identifier(Node):

	def Evaluate(self):

		st = SymbolTable.getter(self.value)

		assembler.addOutput("MOV EBX, [EBP-{}]".format(st[2]))

		return (st[0],st[1])


class Printer(Node):

	def Evaluate(self):


		print(self.children[0].Evaluate()[0])
		assembler.addOutput("PUSH  EBX")
		assembler.addOutput("CALL print")
		assembler.addOutput("POP EBX")


class Block(Node):

	def Evaluate(self):

		for child in self.children:

			child.Evaluate()



class Assignment(Node):

	def Evaluate(self):

		SymbolTable.setter(self.children[0], self.children[1].Evaluate())
		var = SymbolTable.getter(self.children[0])[2]
		assembler.addOutput("MOV [EBP-{}], EBX".format(var))

class Reader(Node):

	def __init__(self,value,children=[]):
		super().__init__(value, children)

	def Evaluate(self):
		return (int(input()),"i32")

class If(Node):

	def Evaluate(self):

		self.id = Node.newId()
		assembler.addOutput("if_{}:".format(self.id))
		first_child = self.children[0]
		# second_child = self.children[1]
		# third_child = self.children[2]
		assembler.addOutput("CMP EBX, False")

		if len(self.children) > 2:
			assembler.addOutput("JE ELSE_{}".format(self.id))
			self.children[1].Evaluate()
			assembler.addOutput("JMP EXIT_{}".format(self.id))
			assembler.addOutput("ELSE_{}:".format(self.id))
			self.children[2].Evaluate()
			assembler.addOutput("EXIT_{}:".format(self.id))
		else:
			assembler.addOutput("JE EXIT_{}".format(self.id))
			self.children[1].Evaluate()
			assembler.addOutput("JMP EXIT_{}".format(self.id))
			assembler.addOutput("EXIT_{}:".format(self.id))



class While(Node):

	def Evaluate(self):

		first_child = self.children[0]
		second_child = self.children[1]
		
		self.id  = Node.newId()
		assembler.addOutput("LOOP_{}:".format(self.id))
		first_child.Evaluate()[0]
		assembler.addOutput("CMP EBX, False")
		assembler.addOutput("JE EXIT_{}".format(self.id))
		second_child.Evaluate()
		assembler.addOutput("JMP LOOP_{}".format(self.id))
		assembler.addOutput("EXIT_{}:".format(self.id))

class assembler:
	string_w = ""
	prog = ""

	for i in sys.argv[1]:

		if i != ".":
			prog += i
		else:
			break

	@staticmethod
	def addOutput(content):
		assembler.string_w += content + "\n"

	@staticmethod
	def create():
		start = """; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss ; variaveis
res RESB 1


section .text
global _start

print: ; subrotina print

PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
XOR ESI , ESI

print_dec: ; empilha todos os digitos
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0'
PUSH EDX
INC ESI ; contador de digitos
CMP EAX, 0
JZ print_next ; quando acabar pula
JMP print_dec

print_next:
CMP ESI , 0
JZ print_exit ; quando acabar de imprimir
DEC ESI

MOV EAX, SYS_WRITE
MOV EBX, STDOUT

POP ECX
MOV [res] , ECX
MOV ECX, res

MOV EDX, 1
INT 0x80
JMP print_next

print_exit:
POP EBP
RET

; subrotinas if / while
binop_je:
JE binop_true
JMP binop_false

binop_jg:
JG binop_true
JMP binop_false

binop_jl:
JL binop_true
JMP binop_false

binop_false:
MOV EBX, False
JMP binop_exit

binop_true:
MOV EBX, True

binop_exit:
RET

_start:

PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

; codigo gerado pelo compilador


"""

		end = """;
				
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
"""
		file = assembler.prog
		with open(file+".asm", "w") as f:

			f.write(start + assembler.string_w + end)







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

assembler.create()













