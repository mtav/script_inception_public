#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from utilities.createGUI import createGUI

class ExampleClass():
  '''Example class to implement the createGUI system.'''
  def __init__(self):
    '''The constructor.'''
    
    # call any parent's class constructor.
    super().__init__()
    
    # attributes
    self.example_float = 1.23
    self.example_int = 123
    self.example_boolean = False
    
    return

  def get_argument_parser(self):
    '''Returns an argparse.ArgumentParser designed for the class.'''

    # create the parser and add any additional custom arguments which should appear first and/or only when the parser is for this object and not a child object.
    parser = argparse.ArgumentParser(description = self.__doc__.split('\n')[0], fromfile_prefix_chars='@')
    parser.add_argument('-b','--basename', action="store", dest="basename", default='SpiralPhasePlate', help='output basename')

    # Add arguments for the parent objects.
    #BFDTDobject.add_arguments(self, parser)

    # Add arguments for this object.
    self.add_arguments(parser)
    
    return parser

  def add_arguments(self, parser):
    '''Adds arguments to the given parser.'''

    parser.add_argument("-r","--restricted-number", help="one of a few possible numbers", type=int, choices=[1,2,3],  default=2)
    
    parser.add_argument("--example_int", help="some int", type=int, default=self.example_int)
    parser.add_argument("--example_float", help="some float", type=float, default=self.example_float)
    parser.add_argument("--example_boolean", help="some boolean", action="store_true", default=False)
    
    return

  def writeFromParsedOptions(self, options):
    '''Called by createGUI when OK is clicked.'''
    
    print ("Options: ", options)
    self.setAttributesFromParsedOptions(options)

    # add the functions to actually write out or do whatever you want to do here.
    
    return

  def setAttributesFromParsedOptions(self, options):
    '''Copy the options passed via the GUI into the object's attribute.'''

    # Don't forget to also call this function for any parent objects.
    #BFDTDobject.setAttributesFromParsedOptions(self, options)

    # this can help you fill in this section
    # NOTE: eval or exec could probably be used to automate this, but their use seems to be discouraged.
    # Also, you might want to handle some options manually.
    for key, val in options.__dict__.items():
      #print((key, val))
      print('self.{0} = options.{0}'.format(key))

    self.example_float = options.example_float
    self.example_int = options.example_int
    self.example_boolean = options.example_boolean
    
    return

if __name__ == '__main__':
	createGUI(ExampleClass())
