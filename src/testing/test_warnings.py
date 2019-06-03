#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import tempfile
import subprocess
import warnings

class MyError(Exception):
    """Base class for exceptions in this module."""
    pass

def main():
  warnings.warn('CACAC', MyError)
  return 0

if __name__ == '__main__':
  main()
