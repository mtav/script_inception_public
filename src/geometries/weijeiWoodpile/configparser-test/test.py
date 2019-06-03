#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utilities.common import str2list, int_array

def main():
  from configparser import ConfigParser, ExtendedInterpolation, BasicInterpolation
  
  parser = ConfigParser(interpolation=ExtendedInterpolation())
  # the default BasicInterpolation could be used as well
  #parser.read('test.ini') # this ignores missing files!
  parser.read_file(open('test-extended.ini'))
  
  print(parser['hashes']['shebang'])
  print(parser['hashes']['extensions'])
  print(parser['hashes']['interpolation not necessary'])
  print(parser['hashes']['even in multiline values'])
  print(parser['foo']['goo'])
  print(parser['foo'].get('goo'))
  print(parser.get('foo','goo'))

  parser = ConfigParser()
  # the default BasicInterpolation could be used as well
  #parser.read('test.ini')
  parser.read_file(open('test-extended.ini'))
   
  print(parser['hashes']['shebang'])
  print(parser['hashes']['extensions'])
  print(parser['hashes']['interpolation not necessary'])
  print(parser['hashes']['even in multiline values'])
  print(parser['foo']['goo'])
  print(parser['foo'].get('goo'))
  print(parser.get('foo','goo'))

  parser = ConfigParser(interpolation=BasicInterpolation())
  # the default BasicInterpolation could be used as well
  parser.read('test-basic.ini')
  print(parser['Paths']['my_pictures'])
  print(parser['Paths']['goo'])
  
  print(parser['foo']['goo'])
  print(parser['foo'].get('goo'))
  print(parser.get('foo','goo'))

  parser = ConfigParser()
  # the default BasicInterpolation could be used as well
  parser.read('test-basic.ini')
  print(parser['Paths']['my_pictures'])
  print(parser['Paths']['goo'])
  
  print(parser['foo']['goo'])
  print(parser['foo'].get('goo'))
  print(parser.get('foo','goo'))
    
  print_type_and_value(parser.getfloat('foo','midgap'))

  print_type_and_value(parser.get('foo','vec3_float'))
  print_type_and_value(str2list(parser.get('foo','vec3_float')))
  
  print_type_and_value(parser.get('foo','vec3_int'))
  print_type_and_value(parser.get('foo','vec3_int_v2'))
  print_type_and_value(str2list(parser.get('foo','vec3_int_v2')))

  return 0

def print_type_and_value(x):
  print(type(x), x)

if __name__ == '__main__':
  main()
