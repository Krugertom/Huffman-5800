import heapq
import os
import sys
import json

class HuffmanCoding:
    """Class for handling Huffman coding algorithm, compression, and decompression."""

    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class Node:
        """Node class to represent characters and their frequencies in the Huffman tree."""

        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def make_frequency_dict(self, text):
        """Creates a frequency dictionary from the input text.

        :param text: The input string.
        :return: A dictionary containing character frequencies.
        """
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        """Creates a min heap from the frequency dictionary.

        :param frequency: The frequency dictionary.
        """
        for key in frequency:
            node = self.Node(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """Merges nodes in the heap until only one node remains."""
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        """Recursive helper function to create the Huffman codes.

        :param root: Current node.
        :param current_code: Current Huffman code string.
        """
        if root == None:
            return

        if root.char != None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """Creates the Huffman codes from the heap."""
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        """Generates the encoded text using the Huffman codes.

        :param text: The input text.
        :return: Encoded text.
        """
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        """Pads the encoded text to make its length a multiple of 8.

        :param encoded_text: The input encoded text.
        :return: Padded encoded text.
        """
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        """Converts the padded encoded text to a byte array.

        :param padded_encoded_text: Padded encoded text.
        :return: Byte array of the encoded text.
        """
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, text):
        
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        # Serialize the frequency dictionary using JSON
        frequency_str = json.dumps(frequency)
        frequency_bytes = frequency_str.encode()
        frequency_size = len(frequency_bytes)
        frequency_size_bytes = frequency_size.to_bytes(4, 'big')

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        # Convert the padded encoded text to bytes
        padded_encoded_bytes = int(padded_encoded_text, 2).to_bytes((len(padded_encoded_text) + 7) // 8, byteorder='big')

        return frequency_size_bytes + frequency_bytes + padded_encoded_bytes


    def remove_padding(self, padded_encoded_text):
        """Removes padding from the encoded text.

        :param padded_encoded_text: Padded encoded text.
        :return: Encoded text without padding.
        """
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        encoded_text = padded_encoded_text[8: -extra_padding if extra_padding != 0 else len(padded_encoded_text)]
        return encoded_text

    def decode_text(self, encoded_text):
        """Decodes the encoded text using reverse mapping.

        :param encoded_text: Encoded text.
        :return: Decoded text.
        """
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, bit_string):
        # Extract the frequency size and frequency information
        frequency_size = int.from_bytes(bit_string[:4], 'big')
        frequency_bytes = bit_string[4:4 + frequency_size]
        frequency_str = frequency_bytes.decode()

        # Deserialize the frequency dictionary using JSON
        frequency = json.loads(frequency_str)

        # Rebuild the Huffman tree
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        # Convert the remaining bit string to binary
        encoded_text = ''.join(f'{byte:08b}' for byte in bit_string[4 + frequency_size:])

        encoded_text = self.remove_padding(encoded_text)
        decompressed_text = self.decode_text(encoded_text)
        return decompressed_text



def encode(infile, outfile):
    """Encodes a file using Huffman coding.

    :param infile: Path to the input file.
    :param outfile: Path to the output file.
    """
    with open(infile, 'r') as input:
        text = input.read().rstrip()

    huffman = HuffmanCoding()
    compressed_data = huffman.compress(text)
    
    # FOR TESTING PURPOSES -- REMOVE BEFORE SUBMISSION


    with open(outfile, 'wb') as output:
        output.write(compressed_data)
        

def decode(infile, outfile):
    """Decodes a file using Huffman coding.

    :param infile: Path to the input file.
    :param outfile: Path to the output file.
    """
    with open(infile, 'rb') as input_file:
        bit_string = input_file.read()

    huffman = HuffmanCoding()
    decompressed_text = huffman.decompress(bit_string)

    with open(outfile, 'w') as output:
        output.write(decompressed_text)




def main():
    """Main function that takes command line arguments for encoding or decoding."""
    if len(sys.argv) != 5:
        print("Run with: pypy3 f1.py [encode/decode] infile outfile")
        sys.exit(1)

    action, infile, outfile, original_file = sys.argv[1:]
    if action == "encode":
        encode(infile, outfile)
    elif action == "decode":
        decode(infile, outfile)
    else:
        print("Invalid action. Use 'encode' or 'decode'.")


if __name__ == "__main__":
    main()
