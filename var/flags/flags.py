#!/usr/bin/env python3

o0 = ''
o1 = ''
o2 = ''
o3 = ''
uniq = ''

with open('clang_o0', 'r') as file:
    o0= file.readlines()

with open('clang_o1', 'r') as file:
    o1= file.readlines()

with open('clang_o2', 'r') as file:
    o2= file.readlines()

with open('clang_o3', 'r') as file:
    o3= file.readlines()

with open('uniq', 'r') as file:
    uniq= file.readlines()

res = []

uniq = list(dict.fromkeys(uniq))

for u in uniq:
    row = []
    row.append(u.strip())
    row.append(u in o0)
    row.append(u in o1)
    row.append(u in o2)
    row.append(u in o3)
    res.append(row)


import pandas as pd

df = pd.DataFrame(res)
df.to_csv('flags.csv', index=False, header=['flag', 'o0', 'o1', 'o2', 'o3'])
