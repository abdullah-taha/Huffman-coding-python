import sys

class Huffman_Node:
	def __init__(self,data,freq):
		self.char = data
		self.freq = freq
		self.right = None
		self.left = None

	def __lt__(self,other):
		return self.freq < other.freq	

class Huffman_tree:

	### Huffman tree constructor: 
	# 	takes a text string as input, invoke the convert2freq function
	# 	to convert the text into a {character:number_of_occurances} dictionary
	#	uses the dictionary to build the huffman tree by invoking build_huffman method
	# inputs: 
	# 	text : a string to encode it's characters and build a huffman encoding tree  
	def __init__(self,text):
		freq = Huffman_tree.__convert2freq(text)
		self.tree = self.__build_huffman(freq)
		self.root = None
		self.encoded = {}
		self.extra_bits = 0

	### build_huffman function:
	# 	takes a frequancy dictionary as input and construct a list of huffman nodes to represent the tree. Then builds the tree by taking the tow
	# 	minimum nodes in the list, merging them into one node and append it back to the list. the result node's frequancy is the sum of the tow nodes.
	#  	at the end, the "tree" list will only contain the root of the tree, with it's frequancy as the sum of all characters frequancies.
	# inputs:
	# 	freq: a {character : number_of_frequancy} dictionary 
	def __build_huffman(self,freq):
		tree = [ Huffman_Node(i,freq[i]) for i in freq.keys() ]
		
		while(len(tree) > 1):
			m1, m2 = Huffman_tree.__minimum_tow(tree)
			#print(m1.char, m2.char)
			m3 = Huffman_tree.__merge(m1,m2)
			m3.right = m1
			m3.left = m2
			tree.remove(m1)
			tree.remove(m2)
			tree.append(m3)
			self.root = m3
		return tree

	### print_tree function :
	# 	a method to print the huffman tree, invokes the private recursive print_tree function by passing the root of the tree
	#  	to traverse the tree from root to leafs
	def print_tree(self):
		self.__print_tree(self.tree[0],"")

	### __print_tree function:
	# 	a recursive function printing the character and its encoding by traversing the tree in an in-order matter, putting '1' each time we go left
	# 	and '0' each time we go right
	def __print_tree(self,root,result):
		 if(root.right == None and root.left == None):
		 	self.encoded[root.char] = result
		 	result = result + " " + root.char 
		 	print(result)
		 	return result 

		 self.__print_tree(root.left, result + "1")
		 self.__print_tree(root.right, result + "0" )	

	### merge functioj :
	#	a private function to merge tow huffman nodes into one node holding the sum of their frequancy
	# inputs:
	# 	m1, m2 : a huffman node
	@staticmethod
	def __merge(m1,m2):
		return Huffman_Node('Node',m1.freq+m2.freq)
	
	### mimimum_tow function:
	#	a private function to find and return the tow mimimum objects out of a huffman_node object list by comparing nodes frequancies
	# inputs: 
	# 	liste : a Huffman_node object list
	@staticmethod
	def __minimum_tow(liste):
		minimum2 = Huffman_Node(None,sys.maxsize)
		minimum1 = Huffman_Node(None,sys.maxsize)
		for i in range(len(liste)):
				if(liste[i].freq < minimum1.freq ):
					minimum2 = minimum1
					minimum1 = liste[i]
				elif(minimum2.char == None or minimum2 > liste[i]):
					minimum2 = liste[i]

		return minimum1,minimum2
	
	### convert2freq function:
	# 	a private function to turn a string of characters into a {character : number of frequancy} dictionary
	# 	for example : convert2freq("hellooo") ---> {'h': 1, 'e': 1, 'l': 2, 'o': 3}
	@staticmethod	
	def __convert2freq(text):
		freq = {}
		for i in text:
			if i not in freq.keys():
				freq[i] = 1
			else:
				freq[i] += 1
		return freq

	### compress function:
	# 	takes a string as input, encode it by invoking the encode function, and return the encoded string   
	def compress(self,text):
		result = ""
		for i in text:
			encoded = self.encode(i)
			result += encoded
		#print(f"compress result :{result}")
		return result

	### encode function :
	# 	takes a character and return the corresponding encoding 
	def encode(self,x):
		#print(self.encoded[x])
		return self.encoded[x]

	### decode function :
	# 	takes a string of encoded string, decodes it, and return the decoded string
	def decode(self, encoded_data):
		temp = ""
		decoded_text = ""
		for i in encoded_data:
			temp += i
			if(temp in self.encoded.values()):
				for char, code in self.encoded.items():
					if(code == temp):
						decoded_text += char
						temp = ""
		return decoded_text

	### save_to_file function:
	# 	takes the huffman-compressed string and save it into a binary file with the file name provided as a parameter 
	def save_to_file(self,text,filename):
		compressed_file = open(f"{filename}","wb")
		buffer = 0
		count = 0
		for i in compressed_text:
			#print(i)
			 count += 1

			 if(int(i) == 1):
			 	buffer = (buffer << 1) + 1
			 	#print(f"bit is one {buffer}")
			 else:
			 	buffer = buffer << 1
			 	#print(f"bit is zero {buffer}")

			 if(count == 8):
			 	compressed_file.write(bytes([buffer]))
			 	#pickle.dump(buffer, compressed_file)
			 	#print(f"buffer dumped to file {buffer}")
			 	#print(bytes([buffer]))
			 	#print(f"buffer dumped to file {bytes(buffer)}")
			 	buffer = 0
			 	count = 0

		if(buffer != 0 ):
			buffer = buffer << (8-count)
			#pickle.dump(buffer, compressed_file)
			compressed_file.write(bytes([buffer]))
			print(f"buffer dumped to file {buffer}")
			self.extra_bits = 8 - count
		compressed_file.close()

	###	read_from_file function:
	# 	read the encoded stored string from a binary file
	#   NOTE: the file must be created using this class
	def read_from_file(self,filename):
		read_file = open(f"{filename}","rb")
		data_coded = ""
		data = read_file.read(1)
		while(data != b""):
			data_int = int.from_bytes(data,"big") 
			#print(f"data int : {data_int}")
			mask = 128
			for i in range(8):
				if((data_int & mask) == 0):
					data_coded += '0'
					#print(f"{i}th bit is zero")
				else:
					data_coded += '1'
					#print(f"{i}th bit is one")
				mask = mask >> 1
			#print(data_coded)
			data = read_file.read(1)
		return data_coded

	### decode_from_file function:
	# 	the function reads the encoded compressed string from the binary file, decode it and return the decoded original string
	def decode_from_file(self,filename):
		data_coded = self.read_from_file(filename)
		return self.decode(data_coded[:-huffman.extra_bits])


f = open("text.txt", 'r')
text = f.read().rstrip()
#text = "hellooo"
f.close()
#result = Huffman_tree.convert2freq(text)
#print(f"convert2freq result :{result}")
	
huffman = Huffman_tree(text)
#print(f"huffman tree root : {huffman.tree[0].freq}")
print("huffman tree :")
huffman.print_tree()
print()

compressed_text = huffman.compress(text)
print(f"encoded = {huffman.encoded}")
print(f"compress result : {compressed_text}")

############################################################################################################	


huffman.save_to_file(compressed_text, "compressed_text")

decoded_text = huffman.decode_from_file("compressed_text")

print(decoded_text)









	 	