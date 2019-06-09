#!/usr/bin/env python
# enlil - v0.2
#
# 26.05.2019 @ 00:28
# full tutorial: https://www.youtube.com/watch?v=cQWu4B6mV2Q
# have fun ;]
# 

# --- imports ---
import sys

# --- defines ---
from pymongo import MongoClient

sys.path.append('./files')
import core


## --- functions ---
def main():
  core.banner() 
  core.menu()

  print '\nThanks, bye! o/\n'


## --- main ---
if __name__ == '__main__':
  main()

