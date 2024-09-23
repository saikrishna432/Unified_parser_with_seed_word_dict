from uparser import *
from joblib import Parallel, delayed
from tqdm import tqdm

# path_hindi_input="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/hindi_new_corpus_words/hindi.words.new.txt"
# with open(path_hindi_input, 'r') as f:
#     words = f.readlines()
word=[]
path4="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/new_parser_big_dict.txt"
with open(path4, 'r') as fl:
    cnts = fl.readlines()
    for ln in cnts:
        ln,_ = ln.split("\t")
        word.append(ln)
words = word
words = [wd.strip() for wd in words]
anslist = Parallel(n_jobs=25)(delayed(safe_word_parse)(wd, 0, 0, 0, "hindi") for wd in tqdm(words))

# path_odiya_oputput='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/seed_word_dict/new_hindi_seed_words.txt'
# with open(path_odiya_oputput, 'w') as f:
#     for i in range(len(words)):
#         if len(anslist[i].split(") ("))<=2:
#             f.write(f'{words[i]}    {anslist[i]}\n')
#             print(f'{words[i]}    {anslist[i]}\n')

print(anslist)
path_out_4="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/old_parser_big_dict.txt"

with open(path_out_4, 'w') as f:
    # for wd, parsing in items:
    #     f.write(wd + '\t' + parsing + '\n')
    for item in anslist:
        if len(item) == 2:
            wd, parsing = item
            parsing= f"(set! wordstruct '( {parsing}))"
            f.write(wd + '\t' + parsing + '\n')
        else:
            print(f"Skipping item: {item}")

