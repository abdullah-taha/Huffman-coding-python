
class Huffman_Node:
	def __init__(self,data,freq):
		self.char = data
		self.freq = freq
		self.right = None
		self.left = None

	def __lt__(self,other):
		return self.freq < other.freq	

class Huffman_tree:
	def __init__(self,freq):
		self.tree = self.__build_huffman(freq)
		self.root = None
		self.encoded = {}

	def __build_huffman(self,freq):
		tree = [ Huffman_Node(i,freq[i]) for i in freq.keys() ]
		
		while(len(tree) > 1):
			m1, m2 = Huffman_tree.minimum_tow(tree)
			print(m1.char, m2.char)
			m3 = Huffman_tree.merge(m1,m2)
			m3.right = m1
			m3.left = m2
			tree.remove(m1)
			tree.remove(m2)
			tree.append(m3)
			self.root = m3
		return tree

	def print_tree(self):
		self.__print_tree(self.tree[0],"")

	def __print_tree(self,root,result):
		 if(root.right == None and root.left == None):
		 	self.encoded[root.char] = result
		 	result = result + " " + root.char 
		 	print(result)
		 	return result 

		 self.__print_tree(root.left, result + "1")
		 self.__print_tree(root.right, result + "0" )	

	@staticmethod
	def merge(m1,m2):
		return Huffman_Node('Node',m1.freq+m2.freq)
	

	@staticmethod
	def minimum_tow(liste):
		minimum2 = Huffman_Node(None,1000)
		minimum1 = Huffman_Node(None,1000)
		for i in range(len(liste)):
				if(liste[i].freq < minimum1.freq ):
					minimum2 = minimum1
					minimum1 = liste[i]
				elif(minimum2.char == None or minimum2 > liste[i]):
					minimum2 = liste[i]

		return minimum1,minimum2
		
	
	def compress(self,text):
		result = ""
		for i in text:
			encoded = self.encode(i)
			result += encoded
		print(result)
		return result

	def encode(self,x):
		#print(self.encoded[x])
		return self.encoded[x]

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




def convert2freq(text):
	freq = {}
	for i in text:
		if i not in freq.keys():
			freq[i] = 1
		else:
			freq[i] += 1
	return freq


f = open("text.txt", 'r')
text = f.read().rstrip()
#text = "hellooo"
f.close()
result = convert2freq(text)
print(result)

huffman = Huffman_tree(result)
print(huffman.tree[0].freq)
huffman.print_tree()
#huffman.encoded)
compressed_text = huffman.compress(text)
print(f"encoded = {huffman.encoded}")
print(compressed_text)
buffer = 0
count = 0
compressed_file = open("compressed_text","wb")
for i in compressed_text:
	#print(i)
	 count += 1

	 if(int(i) == 1):
	 	buffer = (buffer << 1) + 1
	 	print(f"bit is one {buffer}")
	 else:
	 	buffer = buffer << 1
	 	print(f"bit is zero {buffer}")

	 if(count == 8):
	 	compressed_file.write(bytes([buffer]))
	 	#pickle.dump(buffer, compressed_file)
	 	print(f"buffer dumped to file {buffer}")
	 	print(bytes([buffer]))
	 	#print(f"buffer dumped to file {bytes(buffer)}")
	 	buffer = 0
	 	count = 0

if(buffer != 0 ):
	#pickle.dump(buffer, compressed_file)
	compressed_file.write(bytes([buffer]))
	print(f"buffer dumped to file {buffer}")
compressed_file.close()


read_file = open("compressed_text","rb")
data_coded = ""
data = read_file.read(1)
while(data != b""):
	data_int = int.from_bytes(data,"big") 
	print(f"data int : {data_int}")
	mask = 128
	for i in range(8):
		if((data_int & mask) == 0):
			data_coded += '0'
			print(f"{i}th bit is zero")
		else:
			data_coded += '1'
			print(f"{i}th bit is one")
		mask = mask >> 1
	print(data_coded)
	data = read_file.read(1)

decoded_text = huffman.decode(data_coded)
print(decoded_text)








	 	