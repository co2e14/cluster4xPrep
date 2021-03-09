#!/usr/bin/env python3 
import os
from pathlib import Path

directory = os.getcwd()

l = [x[0] for x in os.walk(directory)]

m = []
for x in l:
    if 'dimple' in x:
        m += [x]

print(m)