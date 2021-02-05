import zipfile
from tqdm import tqdm
from time import sleep
import multiprocessing as mp
import sys
import re


info = '''
## General Usage Info ##

Program: DICTIONARY ATTACK

dict_attack.py [ZIP FILE] [PASSWORD LIST1] [PASSWORD LIST2] [PASSWORD LIST3]...

Example:

>>> dict_attack.py test.zip, list1.txt, list2.txt, list3.txt

'''



def multi_password_crack(filename, wordlist, i):
    '''
    Attempts to crack the password of a zip file using the passwords available in the wordlist

    filename -> (str) Name of the secured zip file to be cracked
    wordlist -> Python list-type object containing passwords
    '''
    print(f"Starting Process {i}")

    try:
        zip_file = zipfile.ZipFile(filename)
    except BadZipFile:
        print("File is not a valid zip file")
        sys.exit()

    counter = 0
    found = False
    for j in tqdm(wordlist, desc="Comparing passwords in dictionary..."):
        try:
            password = j.encode() # convert regular string to UTF-8 format
            zip_file.extractall(pwd=password)
            found = True
            print(f"\nProcess {i} found password: {password}")
            return password
        except:
            counter += 1
            continue
    
    if not found:
        print(f"Process {i} password not found")
        return

def quit(arg): # Signal the system to end all processes if 1 worker finds value
    print(f"quitting with {arg}")
    # note: p is visible because it's global in __main__
    p.terminate()  # kill all pool workers

def driver(arguments):
    '''
    This function uses multi-processing to check for the correct password in multiple dictionaries concurrently

    arguments (lst) --> main program arguments

    returns -> the password if found and outputs the contents of the secured zipfile in the current working directory

    Example:
    driver(sys.argv)
    '''
    filename = arguments.pop(0)

    # Check if given file is a valid zip file
    result = re.search('.zip$', filename)
    if not result:
        print("Input file is not a valid zip file")
        sys.exit()

    print(f"target file: {filename}")
    word_dicts = []
    for arg in arguments:

        # Try to open and read file if it exists
        try:
            file = open(arg, "r", encoding="latin1")
            words = []
            data = file.readlines()

            for word in data:
                words.append(word.rstrip())

            word_dicts.append(words)
            file.close()
            print(f"list: {arg}, length: {len(words)}")
        
        except FileNotFoundError:
            print(f"{arg} not found in directory. Exiting...")
            sleep(1)
            sys.exit()


    return filename, word_dicts



### Main functionality ###


if __name__ == "__main__":

    if len(sys.argv) <= 2:
        print(info)
        sleep(1)
        sys.exit()
    else:
        filename, word_dicts = driver(sys.argv[1:])

    ncpu = mp.cpu_count()

    if ncpu < len(word_dicts):
        print(f"CPU limit reached: only first {ncpu} lists will be searched concurrently")
        word_dicts = word_dicts[:ncpu]
    
    p = mp.Pool(ncpu)
    for i in range(len(word_dicts)):
          p.apply_async(multi_password_crack, args=(filename, word_dicts[i], i), callback=quit)
    p.close()
    p.join()
    