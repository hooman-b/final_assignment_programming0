"""
Author: Hooman Bahrdo
date of final revision: 5 Jan. 2023
explanation: this module contains a child class (FeatureString) that is
             used in the main class (GenbankParser).
"""

import re
from features import Features

class FeatureString(Features):

    """
    type: child class
    explanation: this class contains one independant attribute, one static method,
                 and four instance method. The methods are used to set values for
                 attributes.
    output: FeaturesString objects
    """

    def __init__(self,feature_name, feature_description, feature_location, feature_string):
        super().__init__(feature_name, feature_description, feature_location)
        self.string = feature_string

    def __str__(self):
        return f"name= {self.name} location= {self.location}\n string={self.string}"

    def set_feature_string_seperated(self, origin):

        """
        type: instance method
        input: 1- a primitive instance of Feature object
               2- origin string
        explanation: this function produces feature string for seperated mode for
                     all the possible location types, and set it as feature_string
                     attribute.
        output: FeatureString.feature_string
        """

        feature_string = " "

        #extract the feature string when the feature is NOT COMPLEMENT
        if self.location[0] != "complement":

            # find the start point of the location range
            for counter in range(0, len(self.location), 2):
                counter_start_piont = int(self.location[counter]) - 1

                # if there is a range add all bases to feature string
                try:
                    while counter_start_piont <= (int(self.location[counter + 1]) - 1):
                        feature_string += origin[counter_start_piont]
                        counter_start_piont += 1

                #if there is no end point take the start point as the end point
                except IndexError:
                    feature_string += origin[counter_start_piont]

                #if the range value is not integer
                except ValueError as err:
                    print(f'{err}: feature does not have the regular range structure')

        #extract the feature string when the feature is COMPLEMENT
        elif self.location[0] == "complement":

            # suppose the end point as  the start point and move reverse
            for counter in range(len(self.location)-1, 0, -2):
                counter_start_piont = int(self.location[counter]) - 1

                # if there is a range add all bases to feature string
                try:

                    while counter_start_piont >= (int(self.location[counter-1]) - 1):
                        base_pair_complement = " "
                        base_pair_complement = FeatureString.base_pair_complement_maker(
                            origin[counter_start_piont])
                        feature_string += base_pair_complement
                        counter_start_piont -= 1

                #if there is no end point take the start point as the end point
                except IndexError:
                    feature_string += FeatureString.base_pair_complement_maker(
                        origin[counter_start_piont])

                #if the range value is not integer
                except ValueError as err:
                    print(f'{err}: feature does not have the regular range structure')

        self.string = feature_string

    def set_feature_string_uppercase(self, origin):

        """
        type: instance method
        input: 1- a primitive instance of Feature object
               2- origin string
        explanation: this function produces feature string for uppercase mode for
                     all the possible location types, and set it as feature_string
                     attribute.
        output: FeatureString.feature_string
        """

        feature_string = " "

        #set the start point based on complement or not
        if self.location[0] != "complement":
            counter = 0

        else:
            counter = 1

        #set the start point
        assistant_counter = 0
        while counter <= len(self.location)-1:
            upper_maker_assistant = " "
            counter_start_piont = int(self.location[counter]) - 1

            # if there is a range add all bases to feature string
            try:
                counter_end_point = int(self.location[counter + 1])
                lower_keeper_assistant = origin[assistant_counter: counter_start_piont]
                upper_maker_assistant = origin[counter_start_piont: counter_end_point].upper()
                assistant_counter = counter_end_point

            #if there is no end point take the start point as the end point
            except IndexError:
                counter_end_point = int(self.location[counter])
                lower_keeper_assistant = origin[assistant_counter: counter_start_piont]
                upper_maker_assistant = origin[counter_end_point-1].upper()
                origin = re.sub(upper_maker_assistant, origin[counter_end_point-1], origin)

            #if the range value is not integer
            except ValueError as err:
                print(f'{err}: feature does not have the regular range structure')

            feature_string += lower_keeper_assistant + upper_maker_assistant
            counter += 2

        # if is not complement, set the string as the attribute of the class
        if self.location[0] != "complement":
            self.string = feature_string

        # if is complement, reverse the string, set the string as the attribute
        else:
            feature_string_complement = " "

            for counter in range(len(feature_string), 1, -1):
                feature_string_complement += FeatureString.base_pair_complement_maker(
                    feature_string[counter - 1])

            self.string = feature_string_complement

    @staticmethod
    def base_pair_complement_maker(base_pair):

        """
        type: static method
        input: a single base pair in the feature string.
        explanation: this function convert each base pair to its complement counterpart.
        output: complemented base pair.
        """

        base_pair_complement_dictionary = {
            "a": "t", "c": "g", "A": "T", "C": "G", "t": "a", "g": "c", "T": "A", "G": "C"}

        return base_pair_complement_dictionary[base_pair]
