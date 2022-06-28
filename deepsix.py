#!/opt/homebrew/bin/python3

"""
###############################################################################
# FILENAME :  deepsix.py
# LANGUAGE: Python3
# Purpose: A swiss army knife for generating random strings.
# DESCRIPTION :
#       deepsix is a random string generator useful for creating Strings for
#       a variety of purposes including passwords, hex Strings or media IDs.
#
#
# AUTHOR 	:  Eric Andresen        START DATE :    01 May 2022
# EMAIL 	: andresen.eric@gmail.com please add deepsix to the subject for
#             all inqueries
#
# WEBSITE	: http://ericandresen.me/technology/deepsix/
#
# CHANGES :
# all below in C
#           1.0	     Initial Release 21 Mar 2020
#           1.0a	 Updated header comments
#           1.0b     Modified help text to add examples and clarification
#           1.0c     Modified to add runtime FLAG and display options
#           1.0d     Modified to correct a randomization effecting uppercase
#                    values
#			2.0      Complete re-write some functions 100% new and optimized
#                    codebase
#			2.1p     A Python port of DeepSix 01 May 2022 (Python)
#           2.2p     Added in UUID Support
#
# License
#   MIT License
#
#  Copyright (c) 2022 Eric Andresen
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without reSTRiction, including without limitation the rights
#to use, copy, modify, merge, publish, diSTRibute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
"""	
#Import external modules
#import argparse
import sys 
import time #Time modiule is used for both the Runtime data and to seed the Random Module
import random
import uuid

#Configure Charachter Set possibilities
#based on program arguments various symbol sets are selected
STR_SYMBOL_SET = ""                       #zero out the selecxted Symbol set
STR_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # if -u is used this is added to STR_SYMBOL_SET
STR_HEX   = "ABCDEF"                      # if -H is used this and STR_NUMERIC is added to STR_SYMBOL_SET
STR_LOWER = "abcdefghijklmnopqustuvwxyz"  # if -l is used this is added to STR_SYMBOL_SET
STR_NUMERIC = "0123456789"                # if -n is user this is added to STR_SYMBOL_SET
STR_SPACE = " "                           # if -S is used this is added to STR_SYMBOL_SET
STR_TO_DISPLAY = ""                           # Zero out the final string that is displayed 
STR_DELIMITER = ""

#Include Symbols in the Charachter set, use only password safe symbols recommended by OWASP and IBM.
#https://www.ibm.com/support/knowledgecenter/SSV2LR/com.ibm.wbpm.imuc.doc/topics/..
#..rsec_characters.html
#https://owasp.org/www-community/password-special-characters

STR_SYMBOLS = "!$%&()*+-./=?@[]^{}_"     #if -s is used this is added to STR_SYMBOL_SET

#Instantiate and clear symbol set options FLAGs
FLAG_HFLAG = False
FLAG_UPPER = False
FLAG_LOWER = False
FLAG_NUMERIC = False
FLAG_SYMBOL = False
FLAG_SPACE = False
FLAG_HEX = False
FLAG_VFLAG = False
FLAG_TFLAG = False
FLAG_HASP = False
FLAG_PRETTY = False 
FLAG_UUID = False

#Instantiate and clear variables for arguments that pass values.
INT_C = 0  #Default to 5 unless explicitly changed - number of chars to ourput
INT_C_KEEP = 0 # This is used to reset the chars between iterations since iterations are decremented
INT_I = 0 #Number of iterations to run - default to 1 if not explicitly changed 
INT_P = 0 #Use P to format output by adding a dash every x chars where x is defined by INT_P
INT_P_KEEP = 0 # this is useds to reset P by transfering K to P after every n-th char.

#-------------------------------------------------------+
# Evaluate the command line arguments	        	    |
# This section evaluates all of the startup switches    |
# by evaluating the arguments in sys.argv               |
#                                                       |
# Some of the options flip FLAGs evaluted later and     |
# others take direct action. Those that take action     |
# are often using some state to ensure that the option  |
# is only acted on once.                                |
#-------------------------------------------------------+

# Evaluate each of the Flag oriented arguments and set any required flags from False to True.

# Was help requested?
if '-h' in sys.argv: 
	FLAG_HFLAG = True

# Case -u push upper case characters into the Symbol Set
if '-u' in sys.argv: 
	FLAG_UPPER = True 
	STR_SYMBOL_SET += STR_UPPER

if '-l' in sys.argv:# Case -l push lower case characters into the Symbol Set
	FLAG_LOWER = True 
	STR_SYMBOL_SET += STR_LOWER

if '-n' in sys.argv: # Case -n push numeric characters into the Symbol Set
	FLAG_NUMERIC = True
	STR_SYMBOL_SET += STR_NUMERIC

if '-s' in sys.argv: # Case -s push symbols into the Symbol Set
	FLAG_SYMBOLS = True
	STR_SYMBOL_SET += STR_SYMBOLS	

if '-S' in sys.argv: # Case -S pushes a space into the Symbol Set
	FLAG_SPACE = True
	STR_SYMBOL_SET += STR_SPACE

if '-H' in sys.argv: # Case -H push Hex symbols into the Symbol Set
	FLAG_HEX = True
	STR_SYMBOL_SET = "" # Once HEX is selected this will override other symbols selected
	STR_SYMBOL_SET += STR_NUMERIC # HEX includes numeric chars
	STR_SYMBOL_SET += STR_HEX # HEX includes alpha A-F

if '-t' in sys.argv: # Check and see if runtime timestamp was requested
	FLAG_TFLAG = True

if  '-v' in sys.argv: # Check to see if version information was requested
	if FLAG_HFLAG:
		FLAG_VFLAG = False
	else:
		FLAG_VFLAG = True

#Some special handling is needed here in case both version and help is requested to filter out some duplicate information
if FLAG_VFLAG and FLAG_HFLAG:
	FLAG_VFLAG = 0 # This will suppress duplicate version informaition
	
#Now Check all values that include arguments so that we know how to manage the arguments with values
if '-c' in sys.argv:
	C_INDEX = sys.argv.index('-c')
	INT_C = sys.argv[C_INDEX + 1]
	INT_C = int(INT_C)
	INT_C_KEEP = int(INT_C)

if '-i' in sys.argv:
	I_INDEX = sys.argv.index('-i')
	INT_I = sys.argv[I_INDEX + 1]
	INT_I = int(INT_I)

if '-p' in sys.argv:
	P_INDEX = sys.argv.index('-p')
	INT_P = sys.argv[P_INDEX + 1]
	INT_P = int(INT_P)
	INT_P_KEEP = int(INT_P)
	FLAG_PRETTY = True 

if '-uuid' in sys.argv: # Case -S pushes a space into the Symbol Set
	FLAG_UUID = True


#Set the defaults for a few values in the event none are provided
if INT_C == 0: 
	INT_C = 6
	INT_C_KEEP = INT_C 

if INT_I == 0:
	INT_I = 1

if len(str(STR_SYMBOL_SET)) == 0:
	STR_SYMBOL_SET += STR_UPPER
	STR_SYMBOL_SET += STR_NUMERIC

#Now act on all of the FLAGS 
if FLAG_VFLAG:
   	print ("deepsix 2.2p (C) 2022 Eric Andresen  -- A Python Port")

if FLAG_HFLAG:
	print("deepsix [-u -l -n -s -v -H -S] [-c Characters][-i Iterations][-p Count]")
	print("If no arguments are included deepSix will default to Uppercase and Numeric output")
	print("Python versions of deepsix require a space between arguments and their values")
	print("-uuid Output a UUID - Combine with -i for multiples")
	print("-u Include Uppercase characters")
	print("-l Include lowercase characters")
	print("-n Include numbers")
	print("-s Include password safe symbols")
	print("-t Display runtime timestamp")
	print("-v Display Version - Also included in Help info - using -v and -h will suppress the -v")
	print("-H Include HEX symbols - Overides all other char types")
	print("-P Includes a dash every x chars where x is defined by -P to prettify the output")
	print("-S Include a SPACE")
	print("-c Characters number of Random characters to print")
	print("-i Iterations number of iteration to run")
	print(" ")
	print("If no -c or -i are provided they default to 6 characters and 1 Interations")
	print(" ")
	print("Example:     deepsix -u -l -n -s -c 12 -i 10 -p 6  ** output complex  passwords")
	print("Example:     deepsix -H -t -c 12 -i 10 -p 2        ** output random hex strings")
	print("Example:     deepsix                            ** output a random ID")
	print("Author :     Eric Andresen")
	print("Email  :     andresen.eric@gmail.com please add deepsix to the subject for all inqueries")
	print("License:     MIT Open Source")
	print(" ")

#This section is where the random seed is selected. This is done by looking at the data
#print ("INT_I is " + str(INT_I))	
INT_SECONDS_EPOCH = ((time.time()% 1))
random.seed(INT_SECONDS_EPOCH)

# A loop is needed to create the random strings that are needed. 
# Everything before this point is basically managing options and selecting flags
# this is where the real work is done. 	
if FLAG_VFLAG != True and FLAG_HFLAG != True and FLAG_UUID != True:
	while INT_I > 0:

# start a loop from 0 to INT_C and increment - this ensures excess chars are at the end of the string
# The if (INT_P > 0) below ensures that a - will never be before the first char of the output
# Modulo is used to determine when INT_C and INT_P are equally divisible - that is when a 
# delimeter needs to be added 

		for INT_C in range (0,INT_C): 
			if (INT_P > 0) and (INT_C > 0) and ((INT_C % INT_P ) == 0) and (INT_C_KEEP != INT_C):
				STR_TO_DISPLAY = STR_TO_DISPLAY + "-"
			STR_TO_DISPLAY = STR_TO_DISPLAY + STR_SYMBOL_SET[random.randrange(0,(len(STR_SYMBOL_SET)),1)]
			INT_C = INT_C + 1	

		INT_C = INT_C - 1		
		print (STR_TO_DISPLAY)
		INT_C = INT_C_KEEP
		STR_TO_DISPLAY = ""
		INT_I = INT_I -1

if FLAG_UUID == True:
	while INT_I > 0:
		print (uuid.uuid4())
		INT_I = INT_I -1


# If you have selected the option to print a runtime at the end of the run
# then print the runtime		
if FLAG_TFLAG:
	print ("Runtime is:" + time.asctime())
