/***********************************************************************
* FILENAME :  deepsix.c     
*
* DESCRIPTION :
*       deepsix is a random string generator useful for creating strings for Volumne IDs and passwords 
*
*
* AUTHOR 	:  Eric Andresen        START DATE :    16 Mar 2020
* EMAIL 	: andresen.eric@gmail.com please add deepsix to the subject for all inqueries
* WEBSITE	: http://ericandresen.me/technology/deepsix/
*
* CHANGES :
*           1.0		  Initial Release 21 Mar 2020
*           1.0a	  Updated header comments
*           1.0b    Modified help text to add examples and clarification
*           1.0c    Modified to add runtime flag and display options
*           1.0d    Modified to correct a randomization effecting uppercase values
*			2.0     Complete re-write some functions 100% new and optimized codebase
*										
*
*License
*  MIT License
*
*  Copyright (c) 2020 Eric Andresen
*
*  Permission is hereby granted, free of charge, to any person obtaining a copy
*  of this software and associated documentation files (the "Software"), to deal
*  in the Software without restriction, including without limitation the rights
*  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
*  copies of the Software, and to permit persons to whom the Software is
*  furnished to do so, subject to the following conditions:
*  
*  The above copyright notice and this permission notice shall be included in all
*  copies or substantial portions of the Software.
*
*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
*  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
*  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
*  SOFTWARE.
*
***********************************************************************/

#include <stdio.h>   // A basic I/O Library - Required to print to the screen 
#include <stdlib.h>  //Required to support randomization 
#include <string.h>  // 
#include <time.h>    //Required for anything using the time function which is used in the randomization functions 

	// Setup Symbol Sets
	char str_SPOOL[100];
	char str_UPPER[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	char str_HEX[]   = "ABCDEF";
	char str_LOWER[] = "abcdefghijklmnopqustuvwxyz";
	char str_NUMER[] = "1234567890";
	
	//Considered password safe symbols recommended by OWASP and IBM. 
	// https://www.ibm.com/support/knowledgecenter/SSV2LR/com.ibm.wbpm.imuc.doc/topics/rsec_characters.html
	// https://owasp.org/www-community/password-special-characters
	
	char str_SYMBO[] = "!$%&()*+-./=?@[]^{}_"; 
	char str_SPACE[] = " ";
	char str_SUBBU[1];

	//Setup and clear symbol set flags
	int int_UPPER = 0;
	int int_LOWER = 0;
	int int_NUMER = 0;
	int int_SYMBO = 0;
	int int_SPACE = 0;
	int int_HEX = 0;
	int int_vFLAG = 0;	

	//Setup other Global Variables
	int int_HFLAG = 0;
	int int_SENDHELP = 0;
	int TFLAG = 0;  /* value from -t option printing the runtime info */
	int	C_VAL = 0;	/* value from -c option  varies the character output*/
	int I_VAL = 0;  /* value from -i option  varies the iterations run */
	int P_VAL = 0;  /* value from -p option  makes the output pretty*/


int main(int argc, char *argv[]){


/*+------------------------------------------------------+
 |        Evaluate the command line arguments	  	     |
 | This section evaluates all of the startup switches    |
 | some of the options flip flags evaluted later and     |
 | others take direct action. Those that take action     |
 | are often using some state to ensure that the option  |
 | is only acted on once.                                |
 +-----------------------------------------------------+*/
	  int	i; //Local Variable in main only
	  for(i=1;i<argc;i++)
	  {
		if(argv[i][0] == '-' || argv[i][0] == '/' )
		    {//Open the Switch option processing section
			    switch(argv[i][1])
			{//Open Switch processing options
			
			//Case h displays help information
			case 'h' :
				if (int_HFLAG == 0) 
				{
				int_SENDHELP = 1;
				int_HFLAG = 1;
				}
				break;

			case '?' :
				if (int_HFLAG == 0) 
				{
				int_SENDHELP = 1;
				int_HFLAG = 1;
				}
				break;

			
			//Case u pushes upper case characters into the SPOOL array
			case 'u' :
				if (int_UPPER == 0) 
				{
					strcat (str_SPOOL, str_UPPER);
					int_UPPER = 1;
				}
				break;
				
			//Case l pushes lowercase characters into the SPOOL array
			case 'l' :
				if (int_LOWER == 0 ) 
				{
					strcat(str_SPOOL, str_LOWER);
					int_LOWER = 1;
				}
				break;
			
			//Case n pushes numeric values into the SPOOL array
			case 'n' :
				if (int_NUMER == 0) 
				{
					strcat(str_SPOOL, str_NUMER);
					int_NUMER = 1;
				}
				break;
			
			//Case s pushes symbols into the SPOOL array
			case 's' :
				if (int_SYMBO == 0) 
				{
					strcat(str_SPOOL, str_SYMBO);
					int_SYMBO = 1;
				}
				break;

			//Case t displays runtime timestamp 			
			case 't' :
				TFLAG = 1;
				break;


			//Case v displays the applicaiton version
			case 'v' :
				if (int_vFLAG == 0) {printf("deepsix 2.1 (C)Eric Andresen 2020\n");}
				int_vFLAG =1;
				int_HFLAG = 1;
				break;


			//Case H pushes HEX Symbols into the SPOOL array
			case 'H' :
				if (int_HEX == 0) 
				{
					strcat(str_SPOOL, str_HEX);
					strcat(str_SPOOL, str_NUMER);
					int_HEX = 1;
				}
				break;

			//Case S pushes a Space into the SPOOL array
			case 'S' :
				if (int_SPACE == 0) 
				{
					strcat(str_SPOOL, str_SPACE);
					int_SPACE =1;
				}	
				break;
			
			//Case c set the character length
			case 'c' :
				//atoi converts strings to integers - it requires
				// the library stdlib.h
				C_VAL = atoi(argv[i]+2);
				break;

				case 'i' :
				I_VAL = atoi(argv[i]+2);
				break;

				case 'p' :
				P_VAL = atoi(argv[i]+2);
				break;

			default :
				printf("\nUnknown option %s Try -h to display help\n",argv[i]);
				printf(" \n");
				int_HFLAG = 1;
				break;


			}//Close the switch option processing
		}//Close the section that looks for arguments 
	}
	//End of the Switch Evaluations
	//Start of string generation section
	//Evaluate the switches provided and set some default values 
	if (C_VAL == 0) {C_VAL = 6;} 
	if (I_VAL == 0) {I_VAL = 1;} 
	if (strlen(str_SPOOL) == 0 ) {
		//Populate the SPOOL with Uppercase characters
		strcat (str_SPOOL, str_UPPER);
		//Populare the SPOOL with numeric values
		strcat(str_SPOOL, str_NUMER);
	}

	if (int_HFLAG == 0 )
	{


		//Seed & prepare the Random Function 
		time_t rawtime;
  		struct tm * timeinfo;
  		time ( &rawtime );
  		timeinfo = localtime ( &rawtime );
  		srand(time(NULL));

  		// A loop is needed to create the random strings that are needed. 
	  	int j; //Local Variable in main only 
	  		 // outer wrapper for Interations
	  	for (j=0;j < I_VAL ;j++)
	  		{
	  			int k; //Local variable in main only 
	  		   //Inner wrapper for characters
	  				for (k=0;k < C_VAL ;k++)
	  				{
	  					if (P_VAL > 0 ){
	  					if ((k != 0) && k % P_VAL == 0){
	  					printf("-");
	  				}
	  		}
	  			 int int_RAND = rand() % strlen(str_SPOOL);
	  			memcpy( str_SUBBU, &str_SPOOL[int_RAND], 1 );
	  			//printf("%i--",int_RAND);
	  			printf("%s",str_SUBBU);
	  			//printf("%d", str_SPOOL[int_RAND]);
	  	} 
	  		printf("\n");	  		
	
	  }


	  if (TFLAG == 1 ) printf("Runtime is: %s",asctime(timeinfo)); 



	}

	if ( int_SENDHELP == 1 ){
					printf("\ndeepsix [-u -l -n -s -v -H -S] [-cCharacters][-iIterations][-pCount]\n");
					printf("\nIf no swtiches are included defaults to Uppercase and numbers\n");
					printf(" \n");
					printf("-u Include Uppercase characters\n");
					printf("-l Include lowercase characters\n");
					printf("-n Include numbers\n");
					printf("-s Include password safe symbols\n");
					printf("-t Display runtime timestamp\n");
					printf("-H Include HEX symbols\n");
					printf("-S Include a SPACE\n");
					printf("-v Display Version\n");
					printf("-cCharacters number of Random characters to print\n");
					printf("-iIterations number of iteration to run\n");
					printf(" \n");
					printf("If no -c or -i are provided they default to 6 characters and 1 Interations\n");
					printf(" \n");
					printf("Example: deepsix -u -l -n -s -c12 -i10 -p6  ** output complex  passwords\n");
					printf("Example: deepsix -H -t -c12 -i10 -p2        ** output random hex strings\n");
					printf("Example: deepsix                            ** output a random ID\n");
					printf("Author : Eric Andresen\n");
					printf("Email  : andresen.eric@gmail.com please add deepsix to the subject for all inqueries\n");
					printf("License: MIT Open Source\n");
					printf(" \n");
	}

	return 0;
}

