
from seed_word_parser import *
import tqdm


# now, we open the file containing all the hindi words
words = []
with open('/home/speech/Desktop/hema_mam_work/words_maam_check.txt', 'r') as fl:
    cnts = fl.readlines()
    for ln in cnts:
        ln = ln.strip()
        words.append(ln)


items = []
for wd in words:#tqdm(words):
    items.append(generate_item(wd,0,0,0,"hindi"))

with open('/home/speech/Desktop/hema_mam_work/words_maam_check_ans_compare.txt', 'w') as f:
    for wd, parsing in items:
        f.write(wd + '\t' + parsing + '\n')
