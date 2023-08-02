import sys
from collections import Counter


class ShannonFanoNode:
    def __init__(self, symbol, probability, code=''):
        self.symbol = symbol
        self.probability = probability
        self.code = code
        self.left = None
        self.right = None


def calculate_symbol_probabilities(text):
    # Calculate the occurrence frequency of each character in the text
    total_characters = len(text)
    symbol_counts = Counter(text)

    symbol_probabilities = {symbol: count / total_characters for symbol, count in symbol_counts.items()}

    return symbol_probabilities


def shannon_fano_coding(symbol_probabilities, text):
    # Sort symbols based on probabilities in descending order
    code_table = [[symbol, ''] for symbol in list(set(text))]

    symbols = sorted(symbol_probabilities.items(), key=lambda x: x[1], reverse=True)


    # Create the Shannon-Fano tree
    root = build_shannon_fano_tree(symbols)

    # Assign binary codes to symbols
    assign_codes(root, "", code_table)

    return code_table


def build_shannon_fano_tree(symbols):
    if len(symbols) == 1:
        return ShannonFanoNode(symbols[0][0], symbols[0][1])

    total_probability = sum(prob for _, prob in symbols)
    half_probability = 0
    split_index = 0

    # Find the split index that minimizes the difference in probabilities
    for i, (_, prob) in enumerate(symbols):
        half_probability += prob
        if half_probability >= total_probability / 2:
            split_index = i
            break

    node = ShannonFanoNode(None, None)
    node.left = build_shannon_fano_tree(symbols[:split_index + 1])
    node.right = build_shannon_fano_tree(symbols[split_index + 1:])
    return node


def assign_codes(node, code, code_table):
    if node.symbol is not None:
        node.code = code
        for i in range(len(code_table)):
            if node.symbol in code_table[i]:
                code_table[i][1] = node.code
        return

    assign_codes(node.left, code + '0', code_table)
    assign_codes(node.right, code + '1', code_table)


def encode(infile, outfile):
    with open(infile, 'r') as input:
        text = input.read()

    symbols = list(set(text))
    symbol_probabilities = calculate_symbol_probabilities(text)
    code_table = shannon_fano_coding(symbol_probabilities, text)

    encoded = ''.join([code_table[symbols.index(s)][1] for s in text])

    with open(outfile, 'w') as output:
         output.write(encoded)

    return code_table


def decode(infile, outfile, originalFile):
    with open(originalFile, 'r') as input:
        text = input.read()

    symbols = list(set(text))
    symbol_probabilities = calculate_symbol_probabilities(text)
    code_table = shannon_fano_coding(symbol_probabilities, text)

    with open(infile, 'r') as input:
        encode_text = input.read()

    decoded = ''
    code = ''
    for b in encode_text:
        code += b
        i = -1
        for j, c in enumerate(code_table):
            if c[1] == code:
                i = j
                break

        if i >= 0:
            decoded += code_table[i][0]
            code = ''

    with open(outfile, 'w') as output:
         output.write(decoded)


if __name__ == "__main__":
    # Example usage

    action, infile, outfile, originalFile = sys.argv[1:]

    if action == "encode":
        encode(infile, outfile)

    elif action == "decode":
        decode(infile, outfile, originalFile)

    else:
        print("Invalid action. Use 'encode' or 'decode'.")


