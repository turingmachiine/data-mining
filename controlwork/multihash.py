import csv
from itertools import *
import zlib

baskets = {}
with open('transactions.csv') as f:
    reader = csv.reader(f, delimiter=';')
    i = 0
    for row in reader:
        if i == 0:
            i += 1
            continue
        if baskets.keys().__contains__(row[1]):
            baskets[row[1]].append(row[0])
        else:
            baskets[row[1]] = list()
            baskets[row[1]].append(row[0])
frequents = {}

for key in baskets.keys():
    for item in baskets[key]:
        if frequents.keys().__contains__(item):
            frequents[item] += 1
        else:
            frequents[item] = 1

pair_frequents = {}
for key in baskets.keys():
    for i in combinations(baskets[key], 2):
        if pair_frequents.keys().__contains__(i) :
            pair_frequents[i] += 1
        elif pair_frequents.__contains__((i[1], i[0])):
            pair_frequents[(i[1], i[0])] += 1
        else:
            pair_frequents[i] = 1

good_pairs = set()
first_buckets = {}
second_buckets = {}
for key in pair_frequents.keys():
    if frequents[key[0]] >= 3 and frequents[key[1]] >= 3:
        hash1 = (zlib.crc32(bytes(key[0].encode())) + zlib.crc32(bytes(key[1].encode()))) % 100
        if first_buckets.keys().__contains__(hash1):
            first_buckets[hash1] += pair_frequents[key]
        else:
            first_buckets[hash1] = pair_frequents[key]
        hash2 = (zlib.adler32(bytes(key[0].encode())) + zlib.adler32(bytes(key[1].encode()))) % 100
        if second_buckets.keys().__contains__(hash2):
            second_buckets[hash2] += pair_frequents[key]
        else:
            second_buckets[hash2] = pair_frequents[key]

for key in pair_frequents.keys():
    if frequents[key[0]] >= 3 and frequents[key[1]] >= 3:
        hash1 = (zlib.crc32(bytes(key[0].encode())) + zlib.crc32(bytes(key[1].encode()))) % 100
        hash2 = (zlib.adler32(bytes(key[0].encode())) + zlib.adler32(bytes(key[1].encode()))) % 100
        if first_buckets[hash1] >= 3 and second_buckets[hash2] >= 3:
            good_pairs.add(key)

print(len(good_pairs))
print(good_pairs)

