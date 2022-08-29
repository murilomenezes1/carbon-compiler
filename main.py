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



			if "+" not in self.source and "-" not in self.source:

				self.next = Token("INVALID", "INVALID")

				return self.next

			if self.source[self.position] != '+' and self.source[self.position] != '-' and self.source[self.position] != " ":
				if isinstance(int(self.source[self.position]), int):
					num += self.source[self.position]

				if self.position != (len(self.source)-1):
					for i in range(self.position, len(self.source)):
						if not EON:
							if i != (len(self.source) - 1):
								if self.source[i+1] != '+' and self.source[i+1] != '-':
									
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
				self.position += 1

				while self.source[self.position + 1] == " ":
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

class Parser():

	@staticmethod
	def parseExpression(token):

		output = 0
		data = token.selectNext()

		if token.next.data_type == "INVALID":

			raise ValueError("No Operand")

		while token.next.data_type == "BLANK":

			token.selectNext()

		if token.next.data_type == "INT":

			output = int(token.next.value)
			token.selectNext()

			if token.next.data_type == "PLUS" or token.next.data_type == "MINUS" or token.next.data_type == "BLANK":

				while token.next.data_type == "PLUS" or token.next.data_type == "MINUS":

					if token.next.data_type == "PLUS":

						token.selectNext()

						if token.next.data_type == "INT":

							output += int(token.next.value)

						elif token.next.data_type == "BLANK":

							output += 0 

						else:
							raise Exception("Not a number (sum).")

					if token.next.data_type == "MINUS":

						token.selectNext()

						if token.next.data_type == "INT":

							output -= int(token.next.value)

						elif token.next.data_type == "BLANK":

							output -= 0 
	 
						else:

							sys.stderr.write("Not a number (sub).")

					token.selectNext()

				return output

			else:

				raise ValueError("No operand")
		
		else:

			sys.stderr.write("invalid expression starter.")

	@staticmethod
	def run(code):
		token = Tokenizer(code)
		print(Parser.parseExpression(token))

Parser.run(sys.argv[1])









