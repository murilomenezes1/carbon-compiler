import sys
import re


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
		EON = False

		if self.position < len(self.source):



			if "+" not in self.source and "-" not in self.source and "*" not in self.source and "/" not in self.source:

				print(self.source)

				self.next = Token("INVALID", "INVALID")

				return self.next

			if self.source[self.position] != '+' and self.source[self.position] != '-' and self.source[self.position] != " " and self.source[self.position] != "*" and self.source[self.position] != "/":
				if isinstance(int(self.source[self.position]), int):
					num += self.source[self.position]

				if self.position != (len(self.source)-1):
					for i in range(self.position, len(self.source)):
						if not EON:
							if i != (len(self.source) - 1):
								if self.source[i+1] != '+' and self.source[i+1] != '-' and self.source[i+1] != "*" and self.source[i+1] != "/":
									
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

			if num != "" and EON == True:

				self.next = Token("INT", num)
				self.position += len(num)
				num = ""
				EON = False
				return self.next

		else:

			self.next = Token("EOF", None)
			return self.next

class Parser():

	@staticmethod
	def parseTerm(token):

		output = 0
		data = token.selectNext()

		if token.next.data_type == "INVALID":

			raise ValueError("No Operand")

		while token.next.data_type == "BLANK":

			token.selectNext()

		if token.next.data_type == "INT":

			output = int(token.next.value)
			token.selectNext()

			while token.next.data_type == "MULT" or token.next.data_type == "DIV":

				if token.next.data_type == "MULT":

					token.selectNext()

					if token.next.data_type == "INT":

						output *= int(token.next.value)

					elif token.next.data_type == "BLANK":

						output += 0 

					else:
						raise Exception("Not a number (sum).")

				if token.next.data_type == "DIV":

					token.selectNext()

					if token.next.data_type == "INT":

						output //= int(token.next.value)

					elif token.next.data_type == "BLANK":

						output -= 0 
 
					else:

						sys.stderr.write("Not a number (sub).")

				token.selectNext()

			return output

		
		else:

			sys.stderr.write("invalid expression starter.")

	@staticmethod
	def parseExpression(token):

		output = Parser.parseTerm(token)

		while token.next.data_type == "PLUS" or token.next.data_type == "MINUS":

			if token.next.data_type == "PLUS":

				# token.selectNext()
				output += Parser.parseTerm(token)

			if token.next.data_type == "MINUS":

				# token.selectNext()
				output -= Parser.parseTerm(token)


		return output



	@staticmethod
	def run(code):
		token = Tokenizer(code)
		print(Parser.parseExpression(token))





class PrePro():

	@staticmethod
	def filter(code):
		return re.sub(r"//[^\r\n]*$","",code)


Parser.run(PrePro.filter(sys.argv[1]))









