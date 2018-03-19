import pyshark
import sys
import os,errno
import numpy as np
import extractor
import re
ll = extractor.ladder_logic
p_first = ll.find("23")
n_first = ll.find("22")

print p_first

#first =  (p_first if n_first == -1 else p_first if p_first < n_first else n_first if p_first == -1 else p_first)
#if p_first != -1 ? (if n_first != -1 ? if p_first > n_first ? n_first : p_first) : p_first) : n_first

