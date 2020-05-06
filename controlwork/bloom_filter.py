import spacy
import math
import zlib
import hashlib

file = open('controlwork/text.txt', 'r')


def parse_file(file):
    sentence = ''
    for line in file:
        sentence += line
    return sentence


sentence = parse_file(file)
word_set = set()
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
doc = nlp(sentence)
stop_list = ['.', ',', '\n']
for word in doc:
    if stop_list.__contains__(str(word)) is not True:
        word_set.add(str(word))
m = len(word_set)
n = math.ceil(7 * m / math.log(2))
k = math.floor(n/m * math.log(2))
bloom_filter = [0] * n
for doc_w in doc:
    word = str(doc_w)
    crc = zlib.crc32(bytes(word.encode())) % n
    adl = zlib.adler32(bytes(word.encode())) % n
    md5 = int(hashlib.md5(bytes(word.encode())).hexdigest(), 16) % (10 ** 8) % n
    sha = int(hashlib.sha1(bytes(word.encode())).hexdigest(), 16) % (10 ** 8) % n
    sha2 = int(hashlib.sha224(bytes(word.encode())).hexdigest(), 16) % (10 ** 8) % n
    sha3 = int(hashlib.sha384(bytes(word.encode())).hexdigest(), 16) % (10 ** 8) % n
    sha4 = int(hashlib.sha512(bytes(word.encode())).hexdigest(), 16) % (10 ** 8) % n
    bloom_filter[crc] = 1
    bloom_filter[adl] = 1
    bloom_filter[md5] = 1
    bloom_filter[sha] = 1
    bloom_filter[sha2] = 1
    bloom_filter[sha3] = 1
    bloom_filter[sha4] = 1


print(bloom_filter)