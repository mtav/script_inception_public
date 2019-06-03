#!/usr/bin/env python

import schemepy as scheme

if __name__ == '__main__':
  vm = scheme.VM()
  vm.load('values.ctl')
  print vm.get('foo')
  print vm.get('bar')
  print vm.get('foobar')
