# deepsix
deepsix is an awesome tool to use when you need any random string such as a media ID to apply to a disk volume, a randomized password, or any other random string.

deepsix 2.1ap (C) 2022 Eric Andresen  -- A Python Port

deepsix [-u -l -n -s -v -H -S] [-c Characters][-i Iterations][-p Count]
If no arguments are included deepSix will default to Uppercase and Numeric output
Python versions of deepsix require a space between arguments and their values
-u Include Uppercase characters
-l Include lowercase characters
-n Include numbers
-s Include password safe symbols
-t Display runtime timestamp
-v Display Version - Also included in Help info - using -v and -h will suppress the -v
-H Include HEX symbols - Overides all other char types
-P Includes a dash every x chars where x is defined by -P to prettify the output
-S Include a SPACE
-c Characters number of Random characters to print
-i Iterations number of iteration to run

If no -c or -i are provided they default to 6 characters and 1 Interations

Example:     deepsix -u -l -n -s -c 12 -i 10 -p 6  ** output complex  passwords
Example:     deepsix -H -t -c 12 -i 10 -p 2        ** output random hex strings
Example:     deepsix                            ** output a random ID
Author :     Eric Andresen
Email  :     andresen.eric@gmail.com please add deepsix to the subject for all inqueries
License:     MIT Open Source
