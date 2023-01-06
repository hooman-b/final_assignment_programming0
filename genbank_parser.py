r"""
Author: Hooman Bahrdo
date of final revision: 5 Jan. 2023
explanation: this main program contains a class (GenbankParser), and one main
             function. this program gets a genbank file, highlights the relavant
             parts, and make a multi Fasta text file.
inpute lines base on sys are:
1- python3 .\genbank_parser.py .\CFTR_DNA.gb seperated
2- python3 .\genbank_parser.py .\CFTR_DNA.gb uppercased
3- python3 .\genbank_parser.py .\CFTR_mRNA.gb seperated
4- python3 .\genbank_parser.py .\CFTR_mRNA.gb uppercased
5- python3 .\genbank_parser.py .\CFTR_protein.gp seperated
6- python3 .\genbank_parser.py .\CFTR_protein.gp uppercased
"""

import re
import textwrap
import sys
from features import Features
from feature_string import FeatureString
from exceptions import InvalidOriginArgument

class GenbankParser():

    """
    type: class
    explanation: this class is the main class of the program that contains
    three attributes of genbank file, two static methods and six instance
    methods. the methods are contributing in building a GenbankParser object
    as well as an output multi Fasta text file.
    output: genbank objects
    """

    def __init__(self, definition, origin, feature_objects):
        self.definition = definition
        self.origin = origin
        self.feature_objects = feature_objects



    def __str__(self):
        return f"{self.definition} and {self.origin} and {self.feature_objects}"

    @staticmethod
    def store_genbank_file_in_list(input_file_name):

        """
        type: static method
        input: a genbank file
        explanation: this function store genbank file in a list.
        output: a list of genbank file sentences.
        """

        try:
            with open(input_file_name, encoding="utf-8") as genbank:
                genbank_list = []

                for line in genbank:
                    genbank_list.append(line)

        except OSError:
            print(f'file {genbank} cannot open')

        #find any unexpected error and re-raise it.
        except Exception as err:
            print(f'unexpected error: {type(err)}')
            raise

        return genbank_list

    @staticmethod
    def store_features_in_list(genbank_file):

        """
        type: static method
        input: genbank file list from "store_genbank_file_in_list" method.
        explanation: this function extract the raw feature part from the
                     genbank file.
        output: 1- a list of feature sentences
                2- the number of feature sentences
        """

        feature_list = []

        for counter, line in enumerate(genbank_file):

            feature_finder = re.search("^FEATURES", line)
            origin_finder = re.search("^ORIGIN", line)

            if feature_finder:
                start_point = counter

            elif origin_finder:
                end_point = counter

        file_size = end_point - start_point
        feature_list = genbank_file[start_point + 1: end_point]
        return feature_list, file_size

    def set_definition(self, genbank_file):

        """
        type: instance method
        input: 1- a list of genbank file sentences.
               2- a primitive instance of GenbankParser object
        explanation: this function finds the definition of each genbank file in
                     the form of a string and set it as the defintion attribute
                     of the class.
        output: GenbankParser.definition
        """

        final_definition = " "
        definition = []

        #slice the definition section
        for counter, line in enumerate(genbank_file):
            definition_finder = re.search("^DEFINITION", line)
            accession_finder = re.search("^ACCESSION", line)

            if definition_finder:
                start_point = counter

            elif accession_finder:
                end_point = counter

        definition_list = genbank_file[start_point: end_point]

        #make definition string and set it as object attribute
        for line in definition_list:
            definition = re.split(r"\s", line, 1)
            line = definition[1].lstrip().strip("\n")

            final_definition += line

        self.definition = final_definition


    def set_origin(self, genbank_file, input_file_name):

        """
        type: instance method
        input: 1- a list of genbank file sentences
               2- a primitive instance of GenbankParser object
        explanation: this funtion is used to extract origin as a string and set
                     it as the origin attribute of the class.
        output: GenbankParser.origin
        """

        origin = []
        final_origin = ""

        #slice the origin section
        for counter, line in enumerate(genbank_file):
            origin_finder = re.search("^ORIGIN", line)

            if origin_finder:
                origin = genbank_file[counter + 1:]

        #make origin string and set it as the attribute of the class
        for line in origin:
            line = line.lstrip().strip("\n")
            elements_of_each_line = line.split(" ")

            for element in elements_of_each_line:
                base_finder = re.search(r"\D", element)
                end_correction = re.search("[^//]", element)

                if base_finder and end_correction:
                    final_origin += element

        #check the origin string to check  all elements are bases
        for counter, element in enumerate(final_origin):

            if re.search(r"[^atcg]",element) and re.search(".gb$", input_file_name):
                raise InvalidOriginArgument(counter, element)

        self.origin = final_origin

    def set_feature_list(self, genbank_file):

        """
        type: instance method
        input: 1- a list of genbank file sentences
               2- a primitive instance of GenbankParser object
        explanation: this method uses 'store_features_in_list' method to cut the
                     feature part, then by using 'set_feature_attributes' method
                     from Feature class, it makes Feature objects. Finally, it
                     accumulates feature objects in a list and set it as feature
                     _objects attribute of the class.
        output: GenbankParser.feature_objects
        """

        #make a feature list
        feature_file = GenbankParser.store_features_in_list(genbank_file)
        file_size = feature_file[1]
        feature_list = feature_file[0]
        feature_object_list = []

        #make feature objects
        for counter in range(0, file_size - 1):
            feature_object = Features(None, None, None)
            feature_object.set_feature_attributes(counter, feature_list)

            #make sure all the feature attributes get correct values and add them to a list
            if feature_object.name is not None and feature_object.location is not None \
                    and feature_object.description is not None:

                feature_object_list.append(feature_object)

        # set the list as the class attribute
        self.feature_objects = feature_object_list


    def output_writer(self, out_put_name, program_mode):

        """
        type: instance method
        input: 1- GenbankParser object
               2- output name
               3- program mod (seperated or uppercased)
        explanation: this method organize all the attributes of a genbank object
                     into multi FASTA format and store them in a text file. this
                     function use two methods of Feature's child class (FeatureString)
                     to extraxt the uppercased or seperated string of a feature string.
        output: a multi_FASTA text file for a genbank file.
        """

        feature_object_list = self.feature_objects
        uppercase_name_finder = re.search("^up.*", program_mode)
        out_put_name.write(self.definition)
        out_put_name.write("\n"*2)

        #write the feature object attributes in the output file
        for feature_object in feature_object_list:
            out_put_name.write(
                f">{feature_object.name}{feature_object.description}\n")

            #make FeatureString object and set the correct amount for its attribute
            feature = FeatureString(feature_object.name, feature_object.description,
                                        feature_object.location, None)
            if uppercase_name_finder:
                feature.set_feature_string_uppercase(self.origin)

            else:
                feature.set_feature_string_seperated(self.origin)

            #wrap feature string into 60 digit pieces and write it in output file
            feature.string = feature.string.lstrip()
            feature_string = textwrap.wrap(feature.string, 60)

            for element in feature_string:
                out_put_name.write(f"{element}\n")
            out_put_name.write("\n")

def main():

    """
    type: function
    input: 1- name of the genbank file
           2- mode of the program
    explanation: the main function uses GenbankParser methods to build a
                 GenbankParser object, also it makes an output text file.
    output: an output file
    """

    #make the output name from input file's name
    input_file_name = sys.argv[1]
    program_mode = sys.argv[2]
    name = re.sub(".gb|.gp", "_result", input_file_name)

    #create a GenbankParser object
    genbank_object = GenbankParser(None, None, None)
    genbank_file = GenbankParser.store_genbank_file_in_list(input_file_name)
    genbank_object.set_definition(genbank_file)
    genbank_object.set_origin(genbank_file, input_file_name)
    genbank_object.set_feature_list(genbank_file)

    #make an output text file
    with open(f"{name}.txt", "w", encoding="utf-8") as output_name:
        genbank_object.output_writer(output_name, program_mode)

if __name__ == "__main__":
    main()
