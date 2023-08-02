'''
This script reads from path "test_files", generate compression results to path "encoded" and "decoded";
before run, make sure all three path exists.

Run without argument to print to command line for testing purpose:
python3 test_runner.py 

Run in command line for writing to csv:
python3 test_runner.py > compression_runtime.csv
'''

import glob
import os
import subprocess
import time


# List of input and output file names
INFILE_PATH = "test_files"
ENCODED_PATH = "encoded"
DECODED_PATH = "decoded"
ALGOS = ["huffman.py"]
COMMON_ARGS = "python3 {algo} {action} {infile} {outfile}"

# the size of a character is typically considered to be one byte
def count_bytes(filename):
    if not os.path.exists(filename):
        return None

    # Get the size of the file in bytes
    file_size_bytes = os.path.getsize(filename)

    return file_size_bytes

# file name, file size, algo1 encode time, algo1 encoded size, size reduced by, algo1 decode time
def table_header(format="csv") -> str:
    if format == "csv":
        header = []
        col_titles = "file name, file size, {algo} encode time, {algo} encoded size, size reduced by, {algo} decode time"
        for algo_filename in ALGOS:
            algo = algo_filename[:-3]
            header.append(col_titles.format(algo=algo))
        return ", ".join(header)
     
'''
subprocess runs encode and decode on an algo, with result written to corresponding outout files;
return the runtime of the command in second
'''
def timeCommand(cmd) -> float:
    start_time = time.time()
    subprocess.run(cmd.split())
    elapsed_time = time.time() - start_time

    # return round(elapsed_time, 5)
    return elapsed_time

'''
generates command to run an algorithm file, and record the runtime and space data 
'''
def runCommand(algo, action, source_filename, out_filename, data, original_size_bytes=0):
    cmd = COMMON_ARGS.format(algo = algo, action = action, infile = source_filename, outfile = out_filename)
    runTime = timeCommand(cmd)     # encoded/decode called and output file generated here
    data.append(runTime)     # record time 

    # space data for encode
    if action == "encode":
        encoded_size_bytes = count_bytes(out_filename)      
        data.append(encoded_size_bytes)    # record size after encoding 
        reduced_by = round((original_size_bytes - encoded_size_bytes) / original_size_bytes, 2)
        data.append(reduced_by)     # record compression effect on size

'''
generate the output file name for encode/decode for each algorithm
'''
def generate_outfile_name(original_file, algo_file, action):
    file, ext = os.path.splitext(os.path.basename(original_file))
    algo, ext = os.path.splitext(os.path.basename(algo_file))
    if (action == "encode"):
        return os.path.join(ENCODED_PATH, f"{file}_{algo}_{action}d.txt")
    elif (action == "decode"):
        return os.path.join(DECODED_PATH, f"{file}_{algo}_{action}d.txt")
    else:
        exit(1)

def main():
    print(table_header())   # column titles in csv format for our run data 

    test_files = glob.glob(os.path.join(INFILE_PATH, "*.txt"))  # a list of txt file names in INFILE_PATH

    # run encode/decode on each encoding algo, write result to an output file
    for i, original_file in enumerate(test_files):
        original_size_bytes = count_bytes(original_file)
        result = ""
        
        for algorithm in ALGOS:
            result += os.path.basename(original_file)      # append file name for each algo
            data = [original_size_bytes]      # append file size for each algo

            encoded_file = generate_outfile_name(original_file, algorithm, "encode")
            runCommand(algorithm, "encode", original_file, encoded_file, data, original_size_bytes)

            decoded_file = generate_outfile_name(original_file, algorithm, "decode")   # generate the filename for decoded txt
            runCommand(algorithm, "decode", encoded_file, decoded_file, data)

        result += ", " + ", ".join(str(t) for t in data)    
        print(result)

if __name__ == "__main__":
    main()
