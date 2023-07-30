'''
run without argument to print to command line for testing purpose:
python3 test_runner.py 

run in command line for writing to csv:
python3 test_runner.py > compression_runtime.csv

note: my code doesn't handle existing output files yet, not sure if they will be overwritten or cause error, will test tmr;
if you run into issue with that, delete the encoded and decoded .txt, or make changes to my code if you feel like to! 
'''

import sys
import time
import csv
import os
import subprocess

# List of input and output file names
INFILES = ["infile1.txt", "infile2.txt"]
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
        for each in ALGOS:
            algoName = each[:-3]
            header.append(col_titles.format(algo=algoName))
        return ", ".join(header)
     
'''
return the runtime of the command in second
'''
def timeCommand(cmd) -> float:
    start_time = time.time()
    subprocess.run(cmd.split())
    elapsed_time = time.time() - start_time

    # return round(elapsed_time, 5)
    return elapsed_time


def main():
    print(table_header())

    for i, originalFile in enumerate(INFILES):
        infileSizeInBytes = count_bytes(originalFile)
        result = ""
        
        for algorithm in ALGOS:
            result += originalFile      # append file name for each algo
            data = [infileSizeInBytes]      # append file size for each algo

            # run encode on each encoding algo, write result to an output file
            encodedFile = f"{originalFile[:-4]}_{algorithm[:-3]}_encoded.txt"
            encodeCmd = COMMON_ARGS.format(algo = algorithm, action = "encode", infile = originalFile, outfile = encodedFile)
            encodeTime = timeCommand(encodeCmd)     # encoded file generated here
            data.append(encodeTime)     # record time 
            encodedSize = count_bytes(encodedFile)      
            data.append(encodedSize)    # record size after encoding 
            reduced_by = round((infileSizeInBytes - encodedSize) / infileSizeInBytes, 2)
            data.append(reduced_by)     # record compression effect on size

            # run decode on each encoding algo, write result to an output file
            decodedFile = f"{originalFile[:-4]}_{algorithm[:-3]}_decoded.txt"
            decodeCmd = COMMON_ARGS.format(algo = algorithm, action = "decode", infile = originalFile, outfile = encodedFile)
            decodeTime = timeCommand(decodeCmd)
            data.append(decodeTime)     # record time 

        result += ", " + ", ".join(str(t) for t in data)    
        print(result)


if __name__ == "__main__":
    main()