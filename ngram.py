# coding: UTF-8

import re
import time

intre = re.compile(r"^[0-9]+$")

readamount = 0
totalcount = 0
words_lower = dict()
words = dict()

time_start = time.time()

for x in [chr(i) for i in range(ord('a'), ord('z') + 1)]:
    with open("googlebooks-eng-all-1gram-20120701-" + x, "r", encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line is None: break

            data = line.strip().split()
            if len(data) == 0: break

            readamount += len(line)
            if readamount // 1000000 != (readamount - len(line)) // 1000000:
                print(x + ", total amount = " + str((readamount // 1000000) * 1000000), end = "\r")

            word = data[0].split("_")

            if len(word) != 2: continue

            try:
                assert len(data) == 4
                assert re.fullmatch(intre,data[1]) is not None
                assert re.fullmatch(intre,data[2]) is not None
                assert re.fullmatch(intre,data[3]) is not None
            except:
                print(line)
                sys.exit(1)

            if int(data[1]) <= 2000: continue

            c = int(data[2])

            w = word[0]
            if w in words:
                words[w] += c
            else:
                words[w] = c

            w_lower = w.lower()
            if w_lower in words_lower:
                words_lower[w_lower] += c
            else:
                words_lower[w_lower] = c

            totalcount += c

with open("ngram-wordlist-lower.csv", "w", encoding='utf-8') as f:
    words_lower_freq = sorted([(y,x) for (x,y) in words_lower.items()], reverse=True)
    f.write("word,freq"+"\n")
    for x in words_lower_freq:
        f.write(x[1] + "," + str(x[0]) + "\n")

with open("ngram-wordlist.csv", "w", encoding='utf-8') as f:
    words_freq = sorted([(y,x) for (x,y) in words.items()], reverse=True)
    f.write("word,freq"+"\n")
    for x in words_freq:
        f.write(x[1] + "," + str(x[0]) + "\n")

time_end = time.time()
print("")
print("")
print("finish! elapsed time = " + str(int(time_end-time_start)) + " sec")
print("readamount = " + str(readamount))
print("words = " + str(len(words)))
print("words(lower) = " + str(len(words_lower)))
print("total count = " + str(totalcount))



