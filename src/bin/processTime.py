#!/usr/bin/env python3

# TODO: Maybe try out a real parser module this time?

if __name__ == '__main__':

  filename='/tmp/time_id_.txt'
  with open(filename) as f:
    for line in f:
      print(line)
