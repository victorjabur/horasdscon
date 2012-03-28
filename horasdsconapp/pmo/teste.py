#! /usr/bin/python
# coding: utf-8

import sys, re
from unicodedata import normalize

def retirar_acento(str):
    return normalize('NFKD', str.decode('utf-8')).encode('ASCII','ignore')

print retirar_acento('fá')