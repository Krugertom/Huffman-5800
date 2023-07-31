'''
run without argument to print to command line for testing purpose:
python3 test_runner.py 

run in command line for writing to csv:
python3 test_runner.py > compression_runtime.csv
'''

import time
import os
import subprocess

# List of input and output file names
INFILES = ["test_data/infile1.txt", "test_data/infile2.txt"]
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
def runCommand(algo, action, sourceFileName, outFileName, data, originalSizeInBytes=0):
    cmd = COMMON_ARGS.format(algo = algo, action = action, infile = sourceFileName, outfile = outFileName)
    runTime = timeCommand(cmd)     # encoded/decode called and output file generated here
    data.append(runTime)     # record time 

    # space data for encode
    if action == "encode":
        encodedSize = count_bytes(outFileName)      
        data.append(encodedSize)    # record size after encoding 
        reduced_by = round((originalSizeInBytes - encodedSize) / originalSizeInBytes, 2)
        data.append(reduced_by)     # record compression effect on size


def main():
    print(table_header())   # column titles in csv format for our run data 

    # run encode/decode on each encoding algo, write result to an output file
    for i, originalFile in enumerate(INFILES):
        infileSizeInBytes = count_bytes(originalFile)
        result = ""
        
        for algorithm in ALGOS:
            result += originalFile      # append file name for each algo
            data = [infileSizeInBytes]      # append file size for each algo

            encodedFileName = f"{originalFile[:-4]}_{algorithm[:-3]}_encoded.txt"
            runCommand(algorithm, "encode", originalFile, encodedFileName, data, infileSizeInBytes)

            decodedFileName = f"{originalFile[:-4]}_{algorithm[:-3]}_decoded.txt"   # generate the filename for decoded txt
            runCommand(algorithm, "decode", encodedFileName, decodedFileName, data)

        result += ", " + ", ".join(str(t) for t in data)    
        print(result)

if __name__ == "__main__":
    main()