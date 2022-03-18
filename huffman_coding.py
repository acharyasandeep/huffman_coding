import math
import random

def get_key(my_dict, val):
    #utility function to find the key in dictionary using value 
    #if found, returns key otherwise returns false
    for key, value in my_dict.items():
        if val==value:
            return key
    return False


def claculate_freq_table(data):
    #calculate the frequency of every character in the data string and sort in decreasing order
    char_freq = {}
    for char in data:
        if char in char_freq:
            char_freq[char]+=1
        else:
            char_freq[char]=1

    #sort the character frequency in descending order
    sorted_char_freq = sorted(char_freq.items(), key=lambda x:x[1], reverse=True)
    #returns the array of tuples (key, value)
    return sorted_char_freq

class Node():
    #Node of a huffman tree, it has left and right child only
    def __init__(self, left = None, right = None):
        self.left=left
        self.right=right
    def children(self):
        return (self.left, self.right)

def gen_huffman_code(node, huffcode=''):
    #generate huffman code
    if type(node) is str:
        return {node: huffcode}
    d = dict()
    (l,r)=node.children()
    d.update(gen_huffman_code(l, huffcode+'0'))
    d.update(gen_huffman_code(r,huffcode+'1'))
    return d

def get_huffman_code(nodes):
    #return huffman code
    while len(nodes) > 1:
        (key1, val1) = nodes[-1]
        (key2, val2) = nodes[-2]
        nodes = nodes[:-2]
        node = Node(key1, key2)
        nodes.append((node, val1+val2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    # Here after the completion of above loop, nodes becomes the huffman tree
    # generate huffman code from the huffman tree just generated.
    huffcode = gen_huffman_code(nodes[0][0])
    return huffcode

def encode_data(data):
    #encode the data by calculating huffman code and frequency table
    nodes=claculate_freq_table(data)
    freq_table=dict(nodes)
    huffcode=get_huffman_code(nodes)
    encoded_data=''
    for char in data:
        encoded_data+=huffcode[char]
    return (encoded_data, huffcode , freq_table)


def decode_data(encoded_data,huffcode):
    #decodes the encoded data using huffcode generated 
    count=0
    encoded_data_length=len(encoded_data)
    decoded_data=''
    #this loop basically works like this:
    #create a bit pattern by adding first bit of encoded data
    #check bit pattern in huffcode, is there a key having that bit pattern?
    #if there is a key then strip that bit pattern from encoded data and reset the bit pattern and repeat from step 1
    #if there's not a key then add next bit to the bit pattern and repeat from step 2
    #stop if the length of encoded data is less than or equal to 0.
    while(len(encoded_data)>0):
        key=get_key(huffcode, encoded_data[:count])
        if(key):
            decoded_data+=key
            encoded_data=encoded_data[count:]
            count=0
        else:
            if(count > encoded_data_length):
                raise Exception("Error in data received")
            count += 1
    return decoded_data

def calculate_parameters(data_length, freq_table, huffcode):
    #calculates average code length, entropy and efficiency
    average_code_length = 0
    entropy = 0
    efficiency = 0
    probabilities = {}
    for key,value in freq_table.items():
        probabilities[key]=value/data_length

    for key, value in huffcode.items():
        average_code_length+=probabilities[key]*len(value)
        entropy+=probabilities[key]*math.log2(1/probabilities[key])
    
    efficiency = entropy/average_code_length
    return (average_code_length, entropy, efficiency)

def artificial_noise(encoded_data, no_of_noise):
    new_data=''
    change_pos=random.randint(0, len(encoded_data)-1) #generate a random position to place random bits
    i=0
    while i < len(encoded_data):
        if no_of_noise and i==change_pos:
            for j in range(no_of_noise): #add random bits according to no of noise sepcified
                random_bit=str(random.randint(0, 1))
                new_data+=random_bit
            i+=no_of_noise
        else:
            new_data+=encoded_data[i]
            i+=1

    print(len(new_data))
    
    return new_data

#Take data from user or hard code it
data = input("Enter the string: ")
print("Original String: ", data)
(encoded_data, huffcode, freq_table)=encode_data(data)
print("\nFrequency Table: \n", freq_table)
print("\nHuffman Encoding: \n", huffcode)
print("\nEncoded Data: \n", encoded_data)

#You can add any no of artificial noise

# encoded_data=artificial_noise(encoded_data,5)

decoded_data=decode_data(encoded_data, huffcode)
print("\nDecoded Data: \n", decoded_data)

#calculates average code length, entropy and efficiency
data_length = len(data)
(average_code_length, entropy, efficiency)=calculate_parameters(data_length,freq_table, huffcode)
print("\nAverage Code Length: ", average_code_length)
print("Entropy: ", entropy)
print("Efficiency: ", efficiency*100)