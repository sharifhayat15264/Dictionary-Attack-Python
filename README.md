# Dictionary-Attack-Python
This is a **purely educational project** which demonstrates the implementation of a Dictionary Attack using Python.


# Info

'Dictionary Attack' is a popular strategy for cracking the passwords of secured files. In this project, I have implemented the algorithm using Python for cracking secured zip files. In order to speed up the performance of the program, I chose to incorporate multi-processing capabilities in the program, thereby reducing execution time as the program can 
access multiple dictionaries concurrently. This was achieved with the help of the multi-processing library in Python.


## Libraries

* zipfile
* tqdm
* time
* multiprocessing
* sys
* re


## General Usage

Program: Dictionary Attack

dictionary_attack.py [ZIP FILE] [PASSWORD LIST1] [PASSWORD LIST2] [PASSWORD LIST3]...

Example:
```
>>> dictionary_attack.py test.zip list1.txt list2.txt list3.txt
```
