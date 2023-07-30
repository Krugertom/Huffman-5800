import sys

'''
infile: file name of the original text 
outfile: file name to output the encoded text to
'''
def encode(infile, outfile):
    with open(infile, 'r') as input:
        data = input.read()
    
    # with open(outfile, 'w') as output:
    #     output.write("--- encode: ---")
    #     output.write(data)

'''
infile: file name of a piece of encoded text 
outfile: file name to output the decoded text to
'''
def decode(infile, outfile):
    with open(infile, 'r') as input:
        data = input.read()
    
    # with open(outfile, 'w') as output:
    #     output.write("--- decode: ---")
    #     output.write(data)


def main():
    if len(sys.argv) != 4:
        print("Run with: pypy3 f1.py [encode/decode] infile outfile")
        sys.exit(1)

    action, infile, outfile = sys.argv[1:]
    if action == "encode":
        encode(infile, outfile)
        # print("huffman encoding " + infile)
    elif action == "decode":
        decode(infile, outfile)
        # print("huffman decoding " + infile)
    else:
        print("Invalid action. Use 'encode' or 'decode'.")

if __name__ == "__main__":
    main()