"""
Author: Hooman Bahrdo
date of final revision: 5 Jan. 2023
explanation: this module contains a parent class (Feature) that is
             used in the main class (GenbankParser).
"""

import re
from exceptions import UnexpectedFeatureType

class Features():

    """
    type: class
    explanation: this class contains three attributes, and six instance
                 method. The methods are used to set values for attributes.
    output: Features objects
    """

    feature_number = 0

    def __init__(self, feature_name, feature_description, feature_location):
        self.name = feature_name
        self.description = feature_description
        self.location = feature_location
        Features.feature_number += 1

    def __str__(self):
        return f"name= {self.name} description= {self.description}  location= {self.location}"

    def normal(self, location, counter, feature_list):

        """
        type: instance method
        input: 1- a primitive instance of Feature object
               2- location: location of the feature string in the origin
               3- counter: the line number in the feature list
               4- feature list
        explanation: this function extracts the location and description of the
                     normal features and set them as description and location
                     attributes of the class.
        output: 1- Features.description   (normal)
                2- Features.location      (normal)
        """

        #set description and location as the attributes of the class
        feature_description = feature_list[counter+1].lstrip().strip("\n")
        feature_location_list = re.split(r"\..", location)
        self.description, self.location = feature_description, feature_location_list

    def join_order(self, location, counter, feature_list):

        """
        type: instance method
        input: 1- a primitive instance of Feature object
               2- location: location of the feature string in the origin
               3- counter: the line number in the feature list
               4- feature list
        explanation: this function extracts the location and description of the join
                     and order features and set them as description and location
                     attributes of the class.
        output: 1- Features.description  (join|order)
                2- Features.location     (join|order)
        """

        assistant_counter = 1

        #extract the location of the feature in a list
        while re.search(r"^\s*\d", feature_list[counter + assistant_counter]):
            location += feature_list[counter + assistant_counter].lstrip().strip("\n")
            assistant_counter += 1

        feature_location_list = re.split("[()]", location)

        # make the location list for ORDER
        if feature_location_list[0] == "order":
            order_location_list = []
            location = feature_location_list[1]
            feature_location_list = re.split(",", location)

            for element in feature_location_list:

                #add a range for individual locations, add locations to list
                if re.search(r"\..", element):
                    order_location_list.extend(re.split(r"\..", element))

                else:
                    order_location_list.extend([element]*2)

            #set description and location as the attributes of the class
            feature_description = feature_list[counter + assistant_counter].lstrip().strip("\n")
            self.description, self.location = feature_description, order_location_list
            return

        # make the location list for JOIN
        location = feature_location_list[1]
        feature_location_list = re.split(r",|\..", location)

        #set description and location as the attributes of the class
        feature_description = feature_list[counter + assistant_counter].lstrip().strip("\n")
        self.description, self.location = feature_description, feature_location_list

    def complement_join(self, location, counter, feature_list):

        """
        type: instance method
        input: 1- a primitive instance of Feature object
               2- location: location of the feature string in the origin
               3- counter: the line number in the feature list
               4- feature list
        explanation: this function extracts the location and description of the
                     complement and join/complement features and set them as
                     description and location attributes of the class.
        output: 1- Features.description   (join/complement)
                2- Features.location      (join/complement)
        """

        feature_location_list = re.split("[()]", location)

        # the combination of JOIN and COMPLEMENT
        if re.search("^join", feature_location_list[1]):
            assistant_counter = 1
            location = feature_location_list[2]

            #extract the location of the feature in a list
            while re.search(r"^\s*\d", feature_list[counter+assistant_counter]):
                location += feature_list[counter + assistant_counter].lstrip().strip("\n")
                assistant_counter += 1

            feature_location_list = re.split("[()]", location)
            location = feature_location_list[0]
            feature_location_list = re.split(r",|\..", location)
            feature_location_list.insert(0, "complement")

            #set description and location as the attributes of the class
            feature_description = feature_list[counter + assistant_counter].lstrip().strip("\n")
            self.description, self.location = feature_description, feature_location_list

        # this part is COMPLEMENT only
        else:
            location = feature_location_list[1]
            feature_location_list = re.split(r",|\..", location)

            #extract the location of the feature in a list
            if re.search("^>|$<", feature_location_list[1]):
                feature_location_list[1] = feature_location_list[1].strip(">")

            feature_location_list.insert(0, "complement")
            #set description and location as the attributes of the class
            feature_description = feature_list[counter+1].lstrip().strip("\n")
            self.description, self.location = feature_description, feature_location_list

    def set_feature_attributes(self, counter, feature_list):
        """
        inpute: 1- number of the line from "feature_object_building" function.
                2- list of feature from "store_features_in_list" function.
        explanation: this funtion finds all the feature attributes of each feature.
                     this function is using different functions for normal, join, complement,
                     and join complement locations.
        output: 1- feature name
                2- feature description
                3- feature location
        """

        location = " "
        line = feature_list[counter]

        #extract the feature name and location
        if re.search(r"^\s{5}[a-zA-Z]", line):
            line = line.lstrip().strip("\n")
            line = re.split(r"\s", line, 1)
            feature_name = line[0]
            location = line[1].lstrip()

            # set all the attributes of a NORMAL feature
            if re.search(r"^\d", location):
                self.name = feature_name
                self.normal(location, counter, feature_list)

            # set all the attributes of a JOIN or an ORDER feature
            elif re.search("^join|^order", location):
                self.join_order(location, counter, feature_list)
                self.name = feature_name

            # set all the attributes the COMPLEMENT/JOIN and COMPLEMENT part
            elif re.search("^complement", location):
                self.complement_join(location, counter, feature_list)
                self.name = feature_name

            else:
                UnexpectedFeatureType(location)
