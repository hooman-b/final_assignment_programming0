"""
Author: Hooman Bahrdo
date of final revision: 5 Jan. 2023
explanation: this module contains two error classes.
"""

class InvalidOriginArgument(Exception):

    """
    type: exception class
    explanation: this error raises when there is a letter apart from
                 a, t, c, g
    output: an error raises InvalidOriginArgument
    """
    def __init__(self,element_number,element):
        self.element_number = element_number
        self.element = element

    def __str__(self) -> str:
        print(f'for element number {self.element_number} has an unexpected {self.element}')
        return super().__str__()

class UnexpectedFeatureType(Exception):

    """
    type: exception class
    explanation: this error raises when there is a new type of Feature apart from
                 NORMAL, JOIN, ORDER, COMPLEMENT
    output: an error raises UnexpectedFeatureType
    """

    def __init__(self, location):
        self.location = location

    def __str__(self) -> str:
        print(f'this feature has a new type{self.location}')
        return super().__str__()
    