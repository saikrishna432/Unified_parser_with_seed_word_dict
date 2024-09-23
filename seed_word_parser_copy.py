import sortedcontainers as sc
from helpers import RemoveUnwanted
from uparser import safe_word_parse
from tqdm import tqdm
from itertools import product
import sys
import os
from globals import *

c_check=0
def findLang(word : str):
    id = ord(word[0])
    language="hindi"
    if(id>=3328 and id<=3455):
        language = "malayalam" #malayalam
    elif(id>=2944 and id<=3055):
        language = "tamil" #tamil
    elif(id>=3202 and id<=3311):
        language = "kannada" #KANNADA
    elif(id>=3072 and id<=3198):
        language = "telugu" #telugu
    elif(id>=2304 and id<=2431):
        language = "hindi" #hindi
    elif(id>=2432 and id<=2559):
        language = "bengali" #BENGALI
    elif(id>=2688 and id<=2815):
        language = "gujarathi"#gujarathi
    elif(id>=2816 and id<=2943):
        language = "odiya" #odiya
    elif(id>=2560 and id <= 2687): 
        language = "punjabi" # punjabi
    elif(id>=64 and id<=123):
        language = "english" #english
    elif(id>=1536  and id<=1791):
        language = "urdu" #urdu
    # if(g.langId < 5):
    #     g.isSouth = 1
    # if(g.langId == 0):
    #     print(f"UNKNOWN LANGUAGE - id = {fl}")
    #     exit(0)
    return language


def set_lang_id(language):
    if language == "malayalam":
        lang_id=1
    elif language == "tamil":
        lang_id=2
    elif language == "telugu":
        lang_id=3
    elif language == "kannada":
        lang_id=4
    elif language == "hindi":
        lang_id=5
    elif language == "bengali":
        lang_id=6
    elif language == "gujrathi":
        lang_id=7
    elif language == "odiya":
        lang_id=8
    elif language == "punjabi":
        lang_id=9
    return lang_id



def load_prefex_words(language):
    # load a separate prefix file... maybe use the set of seed words itself??
    prefix_words = sc.SortedList()
    path_prefiex_words=os.path.abspath("new_unified_parser/prefixes/prefixes_"+language+".txt")
    with open(path_prefiex_words, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            wd = ln.strip()
            try:
                wd = RemoveUnwanted(wd)
                spword = split_word(wd)
            except:
                continue
            if len(spword) >= 2:
                prefix_words.add(spword)
    return prefix_words


def load_seed_dict(language):
    seed_words = sc.SortedList()    
    source_dir = os.path.dirname("seed_word_dict")
    seed_dict_file_name = os.path.basename("seed_word_dict")
    temp_path= seed_dict_file_name + "/"+language
    seed_dict_path=os.path.join(source_dir, temp_path)
    with open(seed_dict_path, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            ln = ln.strip()
            wd, parsing = ln.split('\t')
            try:
                wd = RemoveUnwanted(wd)
                spword = split_word(wd)
            except:
                continue
            if len(spword) >= 2:
                seed_words.add(spword)
    return seed_words



def get_mapping(lang_id ):
    symboltable = [[None for _ in range(2)] for _ in range(128)]
    with open('/home/krupa/Documents/Unified_Parser_smt_lab_IITM/common.map', 'r') as fl:
        lines = fl.readlines()
        for i in range(len(lines)):
            l = lines[i].strip().split('\t')
            symboltable[i][0] = l[1]
            symboltable[i][1] = l[1 + lang_id]
    return symboltable

def split_word(word): #symbolTable):
    print("before splitting the word: ", word)
    split_list = []
    count = 0
    for sym in word:
        count += 1
        # print("symbol: ", sym)
        # print("count: ", count)
        idx = ord(sym)%128
        # if idx in range(0,4) or idx in range(58,80) or idx in range(85, 88):
        if (idx in range(0,4) or idx in range(58,80) or idx in range(85, 88)): #added an and condition
            print("leng-before", len(split_list))
            if len(split_list) == 0:
                # print("split list", split_list[-1], sym)
                split_list.append(sym)
            split_list[-1] += sym
            print("leng-after", len(split_list))
            # print("after index")
        else:
            # print("inside else")
            split_list.append(sym)
    return split_list


# function to generate all sublists of a given list
def generate_sublists(lst):
    ln = len(lst)
    sublists = []
    for i in range(ln):
        for j in range(i+2, ln+1):
            sublist = lst[i:j]
            sublists.append((sublist, i, i + len(sublist) - 1))
    return sublists




# def generate_sublists_pref(lst):
#     ln = len(lst)
#     sub = []
#     for i in range(ln):
#         print("i \n", i)
#         for j in range(i, ln):
#             print("lst: ", lst)
#             print("j \n", j)
#             sublist = lst[i]
#             print("sublist for prefix or suffix: ", sublist)
#             sub.append((sublist, i, i + len(sublist) - 1))
#     return sub

# def generate_sublists_suf(lst):
#     ln = len(lst)
#     sub = []
#     for i in range(ln):
#         print("i \n", i)
#         for j in range(i, ln):
#             print("lst: ", lst)
#             print("j \n", j)
#             sublist = lst[i]
#             print("sublist for prefix or suffix: ", sublist)
#             sub.append((sublist, i,- 1) i + len(sublist) )
#     return sub




# generate all prefixes of a given list
def generate_prefixes(lst):
    ln = len(lst)
    sublist = []
    for l in range(1, ln):
        sublist.append((lst[:l], 0, l - 1))   
    sublist.reverse()
    print("Generated prefixes:,",sublist)
    return sublist

# generate all suffixes of a given list
def generate_suffixes(lst):
    ln = len(lst)
    sublist = []
    for l in range(ln-1,0,-1):
        sublist.append((lst[l:], l, ln - 1))   
    sublist.reverse()
    print("Generated suffixes:,",sublist)
    return sublist


# we do weighted activity selection with weight = length of match in order to maximize
# the total portion of the word that is covered.
# reference - https://www.cs.princeton.edu/~wayne/cs423/lectures/dynamic-programming-4up.pdf
def weighted_activity_selection(word,activities, debug):
    print("word: ", word)
    global c_check
    if g.flags.DEBUG:
        print("activities:",activities)
    N = len(activities)
    activities.sort(key = lambda x : (x[2], -x[1]))

    # finding the maximum indexed preceding activity that is compatible with the current activity
    preceding_compatible_activity = [None for i in range(N+1)]

    for i in range(1, N+1):
        comp_act = 0
        cur_act = activities[i-1]
        for j in range(1, i):
            cand = activities[j-1]
            if cand[2] < cur_act[1]:
                comp_act = j
        preceding_compatible_activity[i] = comp_act
        # print('preceding_compatible_activity:',preceding_compatible_activity)

    weights = [0 for i in range(N+1)]
    for i in range(1, N+1):
        cur_act = activities[i-1]
        weights[i] = cur_act[2] - cur_act[1] + 1
        # print('weights:', weights)
    opt = [0 for i in range(N+1)]
    ans = [[] for i in range(N+1)]

    for idx in range(1, N+1):
        opt[idx] = opt[idx-1]
        ans[idx] = ans[idx-1].copy()
        # print("opt",opt[idx])
        # print("ans",ans[idx])
        if weights[idx] + opt[preceding_compatible_activity[idx]] >= opt[idx]:
            opt[idx] = weights[idx] + opt[preceding_compatible_activity[idx]]
            # print("1:optimal",opt[idx])
            ans[idx] = ans[preceding_compatible_activity[idx]] + [activities[idx-1]]
            # print("2:ans",ans[idx])
    if g.flags.DEBUG:
        print("length--->:", len(ans[N]))
        print("length of split word:",len(split_word(word)))
        print("ans:",ans[N])
        print("len of ans[N]", len(ans[N]))
    if len(ans[N]) > 1:
        print("passing condition: ", ans[N])
        for i in range(len(ans[N])-1):
            print("i:",i)
            if ans[N][i][2]+1==ans[N][i+1][1]:
                pass
            else:
                return []
        if g.flags.DEBUG:
            print("value:",ans[N][0][1])
        if ans[N][len(ans[N])-1][2]== len(split_word(word))-1 and ans[N][0][1]==0:
            c_check+=1
            # if g.flags.DEBUG:
            print('chosen words :', ans[N])
            return ans[N]
        else:
            return []
    else:
        if g.flags.DEBUG:
            print('chosen words :', ans[N])
        return []

    # if (debug):
    #     print('chosen words :', ans[N])
    # return ans[N]


# # remove unwanted symbols from word before passing it
# def matching_based_parse2(word : str,lsflag : int, wfflag : int, clearflag : int, prefix_encodings, seed_word_encodings, language, debug=True):
#     if g.flags.DEBUG:
#         print(f'debugging {word}')
#     if word == '':
#         return []
    
#     spword = split_word(word)
#     prefixes = []
#     # prefixes = generate_prefixes(spword)
    
#     # print("list of prefixes")
#     # print(prefix_encodings)
#     match_prefix, pref_ans = [], []
#     for pref in prefixes:
#         if prefix_encodings.count(pref) != 0:
#             # print(match_prefix)
#             match_prefix = pref
#             _, pref_ans = safe_word_parse(''.join(match_prefix), lsflag , wfflag , clearflag,language)
#             pref_ans = [pref_ans]
#             break
#     remword = spword[len(match_prefix):]
#     if g.flags.DEBUG:
#         if len(match_prefix)==0:
#             print(f'prefixes are not found')
#         else:
#             print(f'found prefix - {"".join(match_prefix)}')
#         print(f'remaining words excluding prefix - {remword}')
#         print(f'spword - {spword}')
#     remword = spword[len(match_prefix):]  #if prepfix are 0 then remaining word is full word

#     sublists = generate_sublists(remword)
#     if g.flags.DEBUG:
#         print("sublists: - ",sublists)
#     matching_sublists = []
#     # print('seed_word_encodings:',seed_word_encodings)
#     for sublist, begpos, endpos in sublists:
#         if seed_word_encodings.count(sublist) != 0:
#             matching_sublists.append([sublist, begpos, endpos])
#     if g.flags.DEBUG:
#         print ("matching sublist:",matching_sublists)
#     if len(matching_sublists) == 0:
#         _, ans = safe_word_parse(''.join(remword), lsflag , wfflag , clearflag,language)
#         ans = [ans]
#         return pref_ans + ans

#     max_matching_sublists = weighted_activity_selection(word, matching_sublists, debug)
#     print("max_matching_sublists:",max_matching_sublists)
#     if g.flags.DEBUG:
#         for l, _, _ in max_matching_sublists:
#             wd = ''.join(l)
#             print("max_matching_sublists:",l, wd)
    
#     idx = 0
#     cur_act = 0
#     parsings = pref_ans
#     while idx < len(remword):

#         if cur_act == len(max_matching_sublists):
#             word = ''
#             while (idx < len(remword)):
#                 word += remword[idx]
#                 idx += 1
#             if word != '':
#                 _, parsing = safe_word_parse(word,lsflag , wfflag , clearflag, language)
#                 parsings += [parsing]
#             break

#         word = ''
#         while (idx < max_matching_sublists[cur_act][1]):
#             word += remword[idx]
#             idx += 1
#         if word != '':
#             _, parsing = safe_word_parse(word, lsflag , wfflag , clearflag, language)
#             parsings += [parsing]
        
#         word = ''
#         while (idx <= max_matching_sublists[cur_act][2]):
#             word += remword[idx]
#             idx +=1
#         if word != '':
#             _, parsing = safe_word_parse(word, lsflag , wfflag , clearflag, language)
#             parsings += [parsing]
        
#         cur_act += 1
#     if g.flags.DEBUG:
#         print(f'parsings - {parsings}')
#     return parsings


def matching_based_parse(word : str,lsflag : int, wfflag : int, clearflag : int, prefix_encodings, seed_word_encodings, language, debug):
    if g.flags.DEBUG:
        print(f'debugging {word}')
    if word == '':
        return []
    
    spword = split_word(word)
    prefixes = []
    suffixes = []
    prefixes = generate_prefixes(spword)
    suffixes = generate_suffixes(spword)
    
    # print("list of prefixes")
    # print(prefix_encodings)
    match_prefix, pref_ans = [], []
    match_sufix, suf_ans = [], []
    for pref in prefixes:
        if prefix_encodings.count(pref[0]) != 0:
            # print(match_prefix)
            match_prefix.append(pref)
            # _, pref_ans = safe_word_parse(''.join(match_prefix), lsflag , wfflag , clearflag,language)
            # pref_ans = [pref_ans]
            break
    remword = spword[len(match_prefix):]
    if g.flags.DEBUG:
        if len(match_prefix)==0:
            print(f'prefixes are not found')
        else:
            print(f'found prefix - {"".join(match_prefix)}')
        print(f'remaining words excluding prefix - {remword}')
        print(f'spword - {spword}')
    remword = spword[len(match_prefix):]
    print("2. remword: ", remword)

    sublists = generate_sublists(remword)
    print("sublists: - ",sublists)
    matching_sublists = []
    # print('seed_word_encodings:',seed_word_encodings)
    for sublist, begpos, endpos in sublists:
        if seed_word_encodings.count(sublist) != 0:
            matching_sublists.append([sublist, begpos, endpos])
    if g.flags.DEBUG:
        print ("matching sublist:",matching_sublists)
    if len(matching_sublists) == 0:
        return 0, 0
        # _, ans = safe_word_parse(''.join(remword), lsflag , wfflag , clearflag,language)
        # ans = [ans]
        # ans=[]
        # return pref_ans + ans

    max_matching_sublists = weighted_activity_selection(word,matching_sublists, debug)
    if g.flags.DEBUG:
        print("max_matching_sublists:",max_matching_sublists)
    if g.flags.DEBUG:
        for l, _, _ in max_matching_sublists:
            wd = ''.join(l)
            
            print("max_matching_sublists:",l, wd)
    if len(max_matching_sublists) ==0:
        return 0, 0
    idx = 0
    cur_act = 0
    parsings = pref_ans
    lst = []
    while idx < len(remword):
        if cur_act == len(max_matching_sublists):
            word = ''
            while (idx < len(remword)):
                word += remword[idx]
                idx += 1
            if word != '':
                ch, parsing = safe_word_parse(word,lsflag , wfflag , clearflag, language)
                lst += [ch]
                print("lst: ", lst)
                parsings += [parsing]
                print("parsings: ", parsings)
            break

        word = ''
        while (idx < max_matching_sublists[cur_act][1]):
            word += remword[idx]
            idx += 1
        if word != '':
            ch, parsing = safe_word_parse(word,lsflag , wfflag , clearflag, language)
            lst += [ch]
            print("lst: ", lst)
            parsings += [parsing]
            print("parsings: ", parsings)
        word = ''
        while (idx <= max_matching_sublists[cur_act][2]):
            word += remword[idx]
            idx +=1
        if word != '':
            ch, parsing = safe_word_parse(word,lsflag , wfflag , clearflag, language)
            lst += [ch]
            print("lst: ", lst)
            parsings += [parsing]
            print("parsings: ", parsings)
        
        cur_act += 1
    if g.flags.DEBUG:
        print(f'parsings - {parsings}')
    print("lst type", type(lst))
    print("parsings type", type(parsings))
    return lst, parsings





# def testing(symttable):
#     # testing some functionality 
#     sp = split_word('तितिम्मा', symbolTable=symttable)
#     print(sp)
#     sp = split_word('तितिलिका', symbolTable=symttable)
#     print(sp)
#     sp = split_word('कहाल', symbolTable=symttable)
#     print(sp)



def generate_item(word : str, lsflag : int, wfflag : int, clearflag : int,language_main : str,seed_words_main):
    try:
        print("word inside generate item: ", word)
        #wd = word.strip()
        wd = word
        wd = RemoveUnwanted(wd)
        u_languages=["telugu","tamil","kannada","malayalam"]
        wd_debug = False
        # language_main=language
        temp_lang=findLang(word)
        if temp_lang in u_languages:
            language= temp_lang   
        else:
            language=language_main

        seed_languages=["hindi","marathi","gujrathi","bengali","assamese",'Rajasthani',"panjabi"]
        if language in seed_languages:
            #seed_words=load_seed_dict(language)
            seed_words = seed_words_main  

        else:
            seed_words=[]
        # prefix_words=load_prefex_words(language)
        prefix_words=[]
        lanf_id=set_lang_id(language)
        symttable = get_mapping(lanf_id)
        wd_debug=False
        print("before matching based parse")
        ch, parsing = matching_based_parse(wd,lsflag , wfflag, clearflag, prefix_words, seed_words, language, wd_debug)
        print("after matching based parse")
        # print("after matching parse: ", ch)
        if g.flags.DEBUG:
            print("parsed output:",parsing)
        if parsing ==0:
            return 0
        parsing = ''.join(parsing)
        # ch = ''.join(ch)
        if g.flags.DEBUG:
            print(wd, ch, parsing, sep='\t')
    except KeyError:
        parsing = 'FAILED'
        print(f'ignored {wd}')
    # return [wd, f"(set! wordstruct '( {parsing}))"] #original
    return [wd, f"{ch}\t(set! wordstruct '({parsing}))"]



# def generate_item(word):
#     try:
#         wd = RemoveUnwanted(word)
#         wd_debug = True
#         parsing = matching_based_parse(wd, prefix_words, seed_words, symttable, wd_debug)
#         parsing = ''.join(parsing)
#         if wd_debug:
#             print(wd, parsing, sep='\t')
#     except KeyError:
#         parsing = 'FAILED'
#         print(f'ignored {wd}')
#     return [wd, f"(set! wordstruct '( {parsing}))"]



# print the help of syntax
def printHelp():
    print("UnifiedParser - Usage Instructions")
    print("Run python3 seed_word_parser.py wd lsflag wfflag clearflag language")
    print("wd - word to parse in unicode.")
    print("lsflag - always 0. we are not using this.")
    print("wfflag - 0 for Monophone parsing, 1 for syllable parsing, 2 for Akshara Parsing")
    print("clearflag - 1 for removing the lisp like format of output and to just produce space separated output. Otherwise, 0.")
    print("language - name of the language")



if __name__ == '__main__':

    # if (len(sys.argv) != 6):
    #     printHelp()
    #     exit(-1)
    
    # ans=generate_item(sys.argv[1], int(sys.argv[2]),int(sys.argv[3]), int(sys.argv[4]),str(sys.argv[5]))
    # print(ans)
    g = GLOBALS()
    seed_words_main = sc.SortedList()    
    # source_dir = os.path.dirname("seed_word_dict")
    # seed_dict_file_name = os.path.basename("seed_word_dict")
    # temp_path= seed_dict_file_name + "/"+'new_bengali_seed_dict'
    #seed_dict_path=os.path.join(source_dir, temp_path)
    seed_dict_path = "/home/krupa/Documents/CorpusCleaning/Full_Dataset_Preprocessing/seedwords/bengali_seed_new_corpus.txt"
    with open(seed_dict_path, 'r') as fl:
        cnts = fl.readlines()
    cnts = [cnt.strip() for cnt in cnts if cnt.strip()]
    for ln in cnts:
        ln = ln.strip()
        print(ln)
        wd, parsing = ln.split('\t')
        try:
            wd = RemoveUnwanted(wd)
            spword = split_word(wd)
        except:
            continue
        if len(spword) >= 2:
            seed_words_main.add(spword)
    print("seed_words_main \n", seed_words_main)
    print("seed_words_main \n", len(seed_words_main))
    # print(seed_words_main)
    # seed_words_main=[]




# now, we open the file containing all the hindi words
    words = []
    # path_old='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/13000_words_s.txt'
    # path_new="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/hindi_new_corpus_words/hindi.words.new.txt"
    # # path_big_dict="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/phone_dict_big/hindi"
    # path='/home/krupa/Documents/CorpusCleaning/Full_Dataset_Preprocessing/bengali_words_new_corpus_wo_hyphens_all_rem.txt'
    # with open(path, 'r') as fl:
    # # with open('/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/test_words.txt', 'r') as fl:
    #     cnts = fl.readlines()
    #     # print(cnts)
    #     for ln in cnts:
    #         # print("line: ", ln)
    #         # _,ln = ln.split("\t") original
    #         print("line inside loop: ", ln)
    #         words.append(ln)
    #appended words has trailing \n, removing that in below line
    # words = [wd.strip() for wd in words]
    # words=['सफल','असफल','अस','अकल','कल','अंतरंग']
    # words=['क']
    # words=['ताजमहल']#,'पागलपन','देशभक्ति','अतिरिक्त','अत्यंत','अतिक्रमण','अधिकार','लोकसभा','उसका']#,'किंकर्तव्यविमूढ़','अवधिप्रतिबंधकसमिति']'भारत']#,
    # words=["ਅੰਗੂਰੀ","ਮੇਰੇ","ਗਵਾਂਢੀਆਂ","ਦੇ","ਗਵਾਂਢੀਆਂ", "ਦੇ ਗਵਾਂਢੀਆਂ ਦੇ ਘਰ, ਉਹਨਾਂ ਦੇ ਬੜੇ ਪੁਰਾਣੇ ਨੌਕਰ ਦੀ ਬੜੀ ਨਵੀਂ ਬੀਵੀ ਹੈ।"]
    words=["अंतरारष्ट्रीय"]
    # words=['स्वचालित']
    # words=["समाजवादी"]
    # words=['बन्दर']
    # words=['एकत्र']
    # words=["उल्ल"]
    #words=['स्त्री']
    print("words:\n", words)
    print("length of words list: ", len(words))
    items = []
    for wd in tqdm(words):
        print("word before strip", wd)
        #wd = wd.split commented out from org
        print("word after removing whitespaces", wd)
        print("before generate item")
        result=generate_item(wd,0,0,0,"bengali",seed_words_main)
        print("1. result: ", result)
        if result ==0:
            pass
        else:
            print(result)
            items.append(result)
            
    print("items: \n", items)
    # path_old_out="'/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/seed_words_out_1k_2.txt'"
    # path_new2="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/new_comp/new_seed_res_prefex_suffex.txt"
    # path_out_big_dict="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/new_parser_big_dict.txt"
    path_out='/home/krupa/Documents/Unified_Parser_smt_lab_IITM/seedworddictionaryfiles/new_bengali_seed_format_reference.txt'
    with open(path_out, 'w') as f:
        for wd, parsing in items:
            f.write(wd + '\t' + parsing + '\n')
    print('count=',c_check)





# checking from here
# symttable = get_mapping()
# now, we open the file containing all the hindi words
    # words = []
    # with open('/home/speech/Desktop/new_parser_v5_sudhanshu/progress_report_compresion/unique_words.words', 'r') as fl:
    #     cnts = fl.readlines()
    #     for ln in cnts:
    #         ln = ln.strip()
    #         ln = RemoveUnwanted(ln)
    #         words.append(ln)

# words.sort(key=lambda x : (len(encode_split_word(split_word(x,symttable), sym2id)), x))

    # we fix hindi as of now and may change it later
    # MAX_LENGTH = 5
    # MIN_LENGTH = 3
    # DEBUG = False

# words = []
# items = []
# f = open('diff_syl_dict')
# lines = f.readlines()
# for line in lines:
#     temp_line = line.split()
#     word = temp_line[0]
#     # print(word)
#     words.append(word)
#     items.append(generate_item(word))

    # words = ['अवश्यम्भावी','निराशा','सबक़','कुंड']
    # items = []
    # for wd in tqdm(words):
    #     items.append(generate_item(wd,0,0,0,"hindi"))

    # with open('/home/speech/Desktop/Unified_Parser_smt_lab_IITM/rough_out.txt', 'w') as f:
    #     for wd, parsing in items:
    #         f.write(wd + '\t' + parsing + '\n')





