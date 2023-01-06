Title: GENBANK PARSER PROJECT

1- Program application:
This program recieves a genbank or protein file (.gb or .gp) as an input, then 
extracts the relavant parts of the file and write them in a multi Fasta text 
file an the output. It offers two modes for the sequences (uppercase, seperated).
 
2- Program parts:
this program contains FOUR modules:
   A- genbank_parser: contains GenbankParser class. it is the main class of the program,
      it contains three attributes (definition, origin, feature_objects). Moreover, it consists
      of two static methods and six instance methods that contribute in assigning the object
      attributes and aslo in writing the output text file.
   B- features: contains Features class. it is a parent class that is used in GenbankParser 
      class to assign attributes to Feaure objects. it has Three attributes (name, description,
      location). Furthermore, it contains six instance methods. All of them are used to 
      set values to the Feature object attributes.
   C- feature_string: contains FeatureString class. it is a child class of Features class that 
      contains one independant attribute (feature_string), one static method, and four instance
      methods. the methods contribute in setting value to the feature string in two different mode
      (uppercase, seperated).
   D- exceptions: contains two error classes:
		1- InvalidOriginArgument: this error arises when the origin string contains 
		elements apart from a, t, c, g.
		2- UnexpectedFeatureType: this error arises when a feature has a type apart from
		NORMAL, JOIN, COMPLEMENT, ORDER.
Moreover, the main module (genbank_parser), contains a main function that calls most of the 
methods to make a GenbankParser object, and write the output file.

3- Challenges:
During writting this program I have faced some challenges:
   A- Genbank and Protein files have different characteristics, especially when it comes to
      the feature part. Indeed, features can have different types i.e. normal, join, complement,
      order, or a combination of them. Consequently, I tried to include all of them in the
      program, but also I used try except command to tackle some of these errors.
   B- Also, there are some differences in their ranges. For example, some of the files have > 
      or < signs between their ranges (A..>B). So, I tried to cover these differences in the code.
   C- Another challenge was the manner to check the output of the file when the program was not 
      ready yet. some of the files such as DNA file has a large group of features, so the output
      of the program is so large. Consequently checking the correctness of the output was really
      time-consuming.
   D- the last challenge was to determine costume errors (exceptions), in this program I determined
      two costume errors. But, one can find even more than these two.
 
4- future developements:
I think the most important development in the future will be when the gen bank file has some 
unexpected errors, the program will be able to detect those errors and solve them.

5- Run and use the program:
This program is using sys library, so one can use the terminal to run this program. to run it,
one can use one of the below commands:
   A- python3 .\genbank_parser.py .\CFTR_DNA.gb seperated
   B- python3 .\genbank_parser.py .\CFTR_DNA.gb uppercased
   C- python3 .\genbank_parser.py .\CFTR_mRNA.gb seperated
   D- python3 .\genbank_parser.py .\CFTR_mRNA.gb uppercased
   E- python3 .\genbank_parser.py .\CFTR_protein.gp seperated
   F- python3 .\genbank_parser.py .\CFTR_protein.gp uppercased
one just need to copy a line and paste it in the terminal, and press the Enter so the program
starts to run. This program will give a text file, that can be used based on the needs.

6- Credits:
I learnt many useful tips from below links:
   A - https://www.w3schools.com/python/default.asp
   B- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
   C- https://github.com/rwedema/DSLS_PrepProgramming/tree/main/presentations
and many other links that I learn minor points.
you can check my github link to get access to the program. link:
https://github.com/hooman-b?tab=repositories

7- License:
This is an open source code, so I become really appreciated, if somebody improve the code.

  