#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class mainclass(object):
  def __init__(self):
    print('=== mainclass __init__ ===')
    self.common = 123
    
  def write(self):
    print('=== mainclass write ===')
    self.subwrite()

  def subwrite(self):
    print('=== mainclass subwrite ===')
    print(self.common)

class subclass(mainclass):
  #def aha(self):
    #return
  def __init__(self):
    print('=== subclass __init__ ===')
    mainclass.__init__(self)
    self.sub = 10
    
  def subwrite(self):
    print('=== subclass subwrite ===')
    print(self.common)
    print(self.sub)

if __name__ == '__main__':
  print('================================')
  a=subclass()
  a.write()

  print('================================')
  b=mainclass()
  b.write()
