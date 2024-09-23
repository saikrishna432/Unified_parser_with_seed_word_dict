import sortedcontainers as sc
from helpers import RemoveUnwanted
from uparser import safe_word_parse
from tqdm import tqdm
from itertools import product
from itertools import chain
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



def load_prefex_words(language,path_prefiex_words):
    # load a separate prefix file... maybe use the set of seed words itself??
    prefix_words = sc.SortedList()
    # path_prefiex_words=os.path.abspath("new_unified_parser/prefixes/prefixes_"+language+".txt")
    # give the path to the hindi prefix files
    # path_prefiex_words="/home/krupa/Documents/Krupavathy/wordfreq/prefix_list_hindi.txt"
    with open(path_prefiex_words, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            wd = ln.strip()
            try:
                wd = RemoveUnwanted(wd)
                spword = split_word(wd)
            except:
                continue
            # if len(spword) >= 2:
            #     prefix_words.add(spword)
            # if len(spword) >= 2:
            prefix_words.add(spword)
    print("prefix words are processed")
    # print("printing prefix words: \n", prefix_words)
    return prefix_words

def load_sufix_words(language,path_sufix_words):
    # load a separate prefix file... maybe use the set of seed words itself??
    sufix_words = sc.SortedList()
    # path_prefiex_words=os.path.abspath("new_unified_parser/prefixes/prefixes_"+language+".txt")
    # give the path to the hindi prefix files
    # path_sufix_words="/home/krupa/Documents/Krupavathy/wordfreq/hindi_suffixes.txt"
    with open(path_sufix_words, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            wd = ln.strip()
            try:
                wd = RemoveUnwanted(wd)
                spword = split_word(wd)
            except:
                continue
            # if len(spword) >= 2:
            #     sufix_words.add(spword)
            # if len(spword) >= 2:
            sufix_words.add(spword)
    print("Suffix words are processed")
    # print("printing prefix words: \n", prefix_words)
    return sufix_words

def load_seed_dict(language,seed_dict_path):
    seed_words = sc.SortedList()    
    with open(seed_dict_path, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            ln = ln.strip()
            wd, parsing = ln.split('\t')
            # print(wd, parsing)
            try:
                wd = RemoveUnwanted(wd)
                spword = split_word(wd)
            except:
                continue
            if len(spword) >= 2:
                seed_words.add(spword)
    return seed_words


def load_words_carpus(path_words_carpus):
    words = []
    with open(path_words_carpus, 'r') as fl:
        cnts = fl.readlines()
        for ln in cnts:
            # print("line: ", ln)
            # _,ln = ln.split("\t") original
            words.append(ln.strip())
    return words



def get_mapping(lang_id ):
    symboltable = [[None for _ in range(2)] for _ in range(128)]
    with open('common.map', 'r') as fl:
        lines = fl.readlines()
        for i in range(len(lines)):
            l = lines[i].strip().split('\t')
            symboltable[i][0] = l[1]
            symboltable[i][1] = l[1 + lang_id]
    return symboltable

def split_word(word): #symbolTable):
    # print("before splitting the word: ", word)
    split_list = []
    count = 0
    for sym in word:
        count += 1
        # print("symbol: ", sym)
        # print("count: ", count)
        idx = ord(sym)%128
        # if idx in range(0,4) or idx in range(58,80) or idx in range(85, 88):
        if idx in range(0,4) or idx in range(58,80) or idx in range(85, 88): #added an and condition
            # print("leng-before", len(split_list))
            if len(split_list) == 0:
            # print("split list", split_list[-1], sym)
                split_list.append(sym)
            split_list[-1] += sym
            # print("leng-after", len(split_list))
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
#             sub.append((sublist, i, i + len(sublist) - 1))
#     return sub

# generate all prefixes of a given list
# first index '0' is fixed in sublists to indicate prefix
def generate_prefixes(lst):
    ln = len(lst)
    sublists = []
    for l in range(2, ln):
        # print("l of prefix: ", l)
        print("prefix range: ", lst[:l])
        sublists.append([lst[:l], 0, l-1])
    # sublists.reverse()
    print("sublists prefixes: \n", sublists)
    return sublists

# generate all prefixes of a given list
# last index '-1' is fixed in sublists to indicate suffix
def generate_sufixes(lst):
    ln = len(lst)
    sublists_suf = []
    for l in range(ln-2, 0, -1):
        # print("l of sufix: ", l)
        print("range: ", lst[l:])
        sublists_suf.append([lst[l:], l, ln-1])
        # sublists_suf.append([lst[l:], l, ln-1]) # original code
    sublists_suf.reverse()
    print("sublists sufixes: \n", sublists_suf)
    return sublists_suf

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



def matching_based_parse(word : str,lsflag : int, wfflag : int, clearflag : int, prefix_encodings, sufix_encodings, seed_word_encodings, language, debug):
    if g.flags.DEBUG:
        print(f'debugging {word}')
    if word == '':
        return []
    
    print("word before splitting: ", word)
    spword = split_word(word)
    print("word after splitting: ", spword)
    prefixes = []
    sufixes = []
    prefixes = generate_prefixes(spword)
    sufixes = generate_sufixes(spword)
    

    match_prefix, pref_ans = [], []
    match_sufix, suf_ans = [], []
    pref_ch_count = 0
    suf_ch_count = 0
    # print("prefixes: ", prefixes)
    for pref in prefixes:
        # print("prefix encodings-pref: ", pref)
        # print("pref[0]: ", pref[0])
        # print("prefix_encodings.count(pref[0]): ", prefix_encodings.count(pref[0]))
        if prefix_encodings.count(pref[0]) != 0:
            match_prefix = pref
            print("match prefix: \n")
            print(match_prefix)
            _, pref_ans = safe_word_parse(''.join(match_prefix[0]), lsflag , wfflag , clearflag,language)
            print("pref_ans: ", pref_ans)
            # for counting the parsed alphabet characters in the tuple 
            pref_ch_count = len(match_prefix[0])
            print("length of pref ans: ", len(pref_ans))
            print("length of pref ans: ", pref_ch_count)
            # pref_ans = [match_prefix]
            pref_ans = [pref_ans]
            break
    for suf in sufixes:
        print("sufix encodings: ", suf)
        print("suf[0]: ", suf[0])
        print("sufix_encodings.count(suf[0]): ", sufix_encodings.count(suf[0]))
        if sufix_encodings.count(suf[0]) != 0:
            match_sufix = suf
            print("match sufix: \n")
            print(match_sufix)
            _, suf_ans = safe_word_parse(''.join(match_sufix[0]), lsflag , wfflag , clearflag,language)
            print("suf_ans: ", suf_ans)
            # for counting the parsed alphabet characters in the tuple 
            suf_ch_count = len(match_sufix[0])
            print("length of suf ans: ", len(suf_ans))
            print("length of suf ans: ", suf_ch_count)
            # suf_ans = [match_sufix]
            suf_ans = [suf_ans]
            break
    print("length of matching prefix: ", len(pref_ans))
    print("length of matching sufix: ", len(suf_ans))
    print("match prefix: ", match_prefix)
    print("match suffix: ", match_sufix)
    # print("pref_ans: ", pref_ans)
    if len(match_prefix) != 0 and len(match_sufix) != 0:
        # m_pref = len(match_prefix[0])
        # m_suf = len(match_sufix[0])
        m_pref = pref_ch_count
        m_suf = suf_ch_count
        print("m_pref: ", m_pref)
        print("m_suf: ", m_suf)
    elif len(match_prefix) == 0 and len(match_sufix) != 0:
        m_pref = 0
        m_suf = len(match_sufix[0])
    elif len(match_sufix) == 0 and len(match_prefix) != 0:
        m_suf = 0
        m_pref = len(match_prefix[0])
    else:
        m_pref = 0
        m_suf = 0
    # if match_prefix and match_sufix and len(match_prefix[0]) is not None and len(match_sufix[0]) is not None:
    #     m_pref = match_prefix[0]
    #     m_suf = match_sufix[0]
    # elif not match_prefix or match_prefix[0] is None:
    #     m_pref = match_prefix[0]
    # elif not match_sufix or match_sufix[0] is None:
    #     m_suf = match_sufix[0]


    # print("m_pref: ", m_pref)
    # print("m_suf: ", m_suf)
    remword = spword[m_pref:len(spword) - m_suf]
    # remword = spword[len(pref_ans):len(spword) - len(suf_ans)] # original code
    # print("word after removing suffix: ", remword)
    # remword = spword[len(match_prefix):]
    print("pref and suf rem word: ", remword)
    if g.flags.DEBUG:
        if len(match_prefix) == 0:
            print(f'prefixes are not found')
        elif len(match_sufix) == 0:
            print(f'sufixes are not found')
        else:
            print(f'found prefix - {"".join(str(match_prefix))}')
            print(f'found sufix - {"".join(str(match_sufix))}')
        print(f'remaining words excluding prefix and suffix - {remword}')
        print(f'spword - {spword}')
    # remword = spword[len(match_prefix):]
    print("2. remword: ", remword)
    matching_sublists = []
    # matching_sublists_pref = []
    # matching_sublists_suf = []

    sublists = generate_sublists(remword)
    # sublists_pref = generate_sublists_pref(match_prefix)
    # print("sublists_pref: \n", sublists_pref)
    # sublists_suf = generate_sublists_suf(match_sufix)
    # print("sublists_suf: \n", sublists_suf)
    # for sublist, begpos, endpos in sublists_pref:
    #     # print("seed words: \n", seed_word_encodings)
    #     if prefix_encodings.count(sublist) != 0:
    #         matching_sublists_pref.append([sublist, begpos, endpos])
    #     if g.flags.DEBUG:
    #         print ("matching sublist pref:",matching_sublists_pref)
    #     if len(matching_sublists_pref) == 0:
    #         matching_sublists_pref = []

    # for sublist, begpos, endpos in sublists_suf:
    #     # print("seed words: \n", seed_word_encodings)
    #     if sufix_encodings.count(sublist) != 0:
    #         matching_sublists_suf.append([sublist, begpos, endpos])
    #     if g.flags.DEBUG:
    #         print ("matching sublist suf:",matching_sublists_suf)
    #     if len(matching_sublists_suf) == 0:
    #         matching_sublists_suf = []

    print("sublists: - ",sublists)

    # print('seed_word_encodings:',seed_word_encodings)


    for sublist, begpos, endpos in sublists:
        # print("seed words: \n", seed_word_encodings)
        if seed_word_encodings.count(sublist) != 0:
            matching_sublists.append([sublist, begpos, endpos])
        # else:
        #     return 0
    if g.flags.DEBUG:
        print ("matching sublist remword:",matching_sublists)
    if len(matching_sublists) == 0:
        matching_sublists = []
        # _, ans = safe_word_parse(''.join(remword), lsflag , wfflag , clearflag,language)
        # ans = [ans]
        # ans=[]
        # return pref_ans + ans
    print("matching sublists: ", matching_sublists)
    # flat_pref_sublists = sum(prefixes, []) # Flatten the list
    # flat_matching_sublists = sum(matching_sublists, []) # Flatten the list
    # flat_sub_sublists = sum(sufixes, []) # Flatten the list

    op_for = prefixes + matching_sublists + sufixes
    # flat_op_for = sum(op_for, [])
    op_format.append(op_for)
    print("output_format: \n", op_for)


    # op_format = matching_sublists_pref + matching_sublists + matching_sublists_suf
    # print("output_format: \n", op_format)

    # DP problem
    # max_matching_sublists = weighted_activity_selection(word,matching_sublists, debug)
    max_matching_sublists = weighted_activity_selection(word, op_for, debug)
    if g.flags.DEBUG:
        print("max_matching_sublists:",max_matching_sublists)
    if g.flags.DEBUG:
        for l, _, _ in max_matching_sublists:
            wd = ''.join(l)
            
            print("max_matching_sublists:",l, wd)
    if len(max_matching_sublists) ==0:
        return 0
    idx = 0
    cur_act = 0
    parsings = pref_ans
    print("suffix answer before rem word parsing: ", suf_ans)
    while idx < len(remword):
        if cur_act == len(max_matching_sublists):
            word = ''
            while (idx < len(remword)):
                word += remword[idx]
                idx += 1
            if word != '':
                _, parsing = safe_word_parse(word,lsflag , wfflag , clearflag, language)
                parsings += [parsing]
                print("ukparse: ", parsings)
            break

        word = ''
        while (idx < max_matching_sublists[cur_act][1]):
            word += remword[idx] # can make idx+1 to start from the 3rd 
            idx += 1
        if word != '':
            _, parsing = safe_word_parse(word, lsflag , wfflag , clearflag, language)
            parsings += [parsing]
            print("eparse: ", parsings)
        
        word = ''
        print("idx: ", idx)
        print("max_matching_sublists[cur_act] max match", max_matching_sublists[cur_act])
        print("max_matching_sublists[cur_act][2]max match sub", max_matching_sublists[cur_act][2])
        # print("idx: ", idx)
        while (idx <= (max_matching_sublists[cur_act][2])):
            print("idx: ", idx)
            # added this if condition here so that we don't go out of rem_word array index
            if idx < len(remword): 
                print("remword: ", remword)
                print("remword[idx]: ", remword[idx])
                word += remword[idx]
                idx +=1
            else:
                break
        if word != '':
            _, parsing = safe_word_parse(word, lsflag , wfflag , clearflag, language)
            parsings += [parsing]
            print("aprase: ", parsings)
        cur_act += 1
    if len(suf_ans) == 0:
        print("no suffixes")
    else:
        parsings += [suf_ans]
    if g.flags.DEBUG:
        print(f'parsings - {parsings}')
    return parsings

op_format = []


# def testing(symttable):
#     # testing some functionality 
#     sp = split_word('तितिम्मा', symbolTable=symttable)
#     print(sp)
#     sp = split_word('तितिलिका', symbolTable=symttable)
#     print(sp)
#     sp = split_word('कहाल', symbolTable=symttable)
#     print(sp)



def generate_item(word : str, lsflag : int, wfflag : int, clearflag : int,language_main : str,seed_words_main,path_prefiex_words:str, path_sufix_words:str, wd_debug=False):
    try:
        print("word in generate_item function: ", word)
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
        prefix_words = load_prefex_words(language,path_prefiex_words)
        sufix_words = load_sufix_words(language,path_sufix_words)
        # prefexes and suffixes are in the form of splitted letters: इउगा -- ['इ', 'उ', 'गा']
        print("number of prefix words: \n", len(prefix_words))
        print("sufix words: \n", len(sufix_words))
        # prefix_words=[]
        lanf_id=set_lang_id(language)
        print("language:", language, "id:", lanf_id)
        symttable = get_mapping(lanf_id)
        parsing = matching_based_parse(wd,lsflag , wfflag, clearflag, prefix_words, sufix_words, seed_words, language, wd_debug)
        if g.flags.DEBUG:
            print("parsed output:",parsing)
        if parsing ==0:
            return 0
        # parsing = ''.join(parsing) # Previously was commented out #original
        print("parsing: ", parsing)
        parsing = ''.join(['(' + ''.join(map(str, item)) + ')' for item in parsing])
        if g.flags.DEBUG:
            print(wd, parsing, sep='\t')
    except KeyError:
        parsing = 'FAILED'
        print(f'ignored {wd}')
    # return [wd, f"(set! wordstruct '( {parsing}))"] #original
    return [wd, f"(set! wordstruct '({parsing}))"]







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
    language='hindi'
    debug=True
    


    seed_dict_path = "/home/speech/Desktop/Unified_Parser_smt_working/seed_word_dict/new_hindi_seed_words.txt"
    path_prefiex_words="/home/speech/Desktop/Unified_Parser_smt_working/hindi_root_words/prefix_list_hindi.txt"
    path_sufix_words="/home/speech/Desktop/Unified_Parser_smt_working/hindi_root_words/hindi_suffixes.txt"
    path_words_carpus="/home/speech/Desktop/Unified_Parser_smt_working/hindi_new_corpus_words/hindi.words.new.txt"




    

    seed_words_main = sc.SortedList()    
    # source_dir = os.path.dirname("seed_word_dict")
    # seed_dict_file_name = os.path.basename("seed_word_dict")
    # temp_path= seed_dict_file_name + "/"+'new_bengali_seed_dict'
    # seed_dict_path=os.path.join(source_dir, temp_path)
    seed_words_main= load_seed_dict(language,seed_dict_path)
    # if debug=="True":
    #     print("seed_words_main \n", seed_words_main)
    print("length of seed_words_main: ", len(seed_words_main))   
    

    words_carpus=[]
    words_carpus=load_words_carpus(path_words_carpus)

    # print("list of all words: \n", words)
    # words_carpus=['सफल','असफल','अस','अकल','कल','अंतरंग']
    # words_carpus=['क']
    # words_carpus=['ताजमहल']#,'पागलपन','देशभक्ति','अतिरिक्त','अत्यंत','अतिक्रमण','अधिकार','लोकसभा','उसका']#,'किंकर्तव्यविमूढ़','अवधिप्रतिबंधकसमिति']'भारत']#,
    # words_carpus=["ਅੰਗੂਰੀ","ਮੇਰੇ","ਗਵਾਂਢੀਆਂ","ਦੇ","ਗਵਾਂਢੀਆਂ", "ਦੇ ਗਵਾਂਢੀਆਂ ਦੇ ਘਰ, ਉਹਨਾਂ ਦੇ ਬੜੇ ਪੁਰਾਣੇ ਨੌਕਰ ਦੀ ਬੜੀ ਨਵੀਂ ਬੀਵੀ ਹੈ।"]
    words_carpus=["अंतरारष्ट्रीय","अवधिप्रतिबंधकसमिति"]
    # words_carpus=['स्वचालित']
    # words_carpus=["समाजवादी","घटिया"]
    # words_carpus=['बन्दर']
    # words_carpus=['एकत्र']
    # words_carpus=["उल्ल"]
    # words_carpus=['स्त्री']

    # print("words_carpus:", words_carpus)
    print("length of words list: ", len(words_carpus))
    items = []
    for wd in tqdm(words_carpus):
        print("word:", wd)
        result=generate_item(wd,0,0,0,"hindi",seed_words_main,path_prefiex_words,path_sufix_words)  # phoneme parsing
        print("1. result: ", result)
        if result ==0:
            pass
        else:
            print(result)
            items.append(result)



    # path_out='/home/krupa/Documents/Unified_Parser_smt_lab_IITM/Pref_Suf/hindi_output_format_new.txt'
    # with open(path_out, 'w') as f:
    #     # flat_op_for = list(chain.from_iterable(op_format))
    #     for item in op_format:
    #         # print("item:", item)
    #         f.write(str(item) + '\n')
    #         # f.write('\n')

    # # print("items: \n", items)
    # path_out='/home/krupa/Documents/Unified_Parser_smt_lab_IITM/seedworddictionaryfiles/Output/hindi_output_new.txt'
    # with open(path_out, 'w') as f:
    #     for wd, parsing in items:
    #         f.write(wd + '\t' + parsing + '\n')
    # print('count=',c_check)


    # # seed_words_main=[]
    # path_cond = "/home/krupa/Documents/Unified_Parser_smt_lab_IITM/seedworddictionaryfiles/seed_condition_passing_for_hindi_new.txt"
    # # seed_words_main=[]
    # with open(path_cond, 'w') as f:
    #     for item in seed_words_main:
    #         # print("word: ", item)
    #         f.write(str(item) + '\n')

    # print("words passing condition is written")



    



















# # checking from here
# # symttable = get_mapping()
# # now, we open the file containing all the hindi words
#     # words = []
#     # with open('/home/speech/Desktop/new_parser_v5_sudhanshu/progress_report_compresion/unique_words.words', 'r') as fl:
#     #     cnts = fl.readlines()
#     #     for ln in cnts:
#     #         ln = ln.strip()
#     #         ln = RemoveUnwanted(ln)
#     #         words.append(ln)

# # words.sort(key=lambda x : (len(encode_split_word(split_word(x,symttable), sym2id)), x))

#     # we fix hindi as of now and may change it later
#     # MAX_LENGTH = 5
#     # MIN_LENGTH = 3
#     # DEBUG = False

# # words = []
# # items = []
# # f = open('diff_syl_dict')
# # lines = f.readlines()
# # for line in lines:
# #     temp_line = line.split()
# #     word = temp_line[0]
# #     # print(word)
# #     words.append(word)
# #     items.append(generate_item(word))

#     # words = ['अवश्यम्भावी','निराशा','सबक़','कुंड']
#     # items = []
#     # for wd in tqdm(words):
#     #     items.append(generate_item(wd,0,0,0,"hindi"))

#     # with open('/home/speech/Desktop/Unified_Parser_smt_lab_IITM/rough_out.txt', 'w') as f:
#     #     for wd, parsing in items:
#     #         f.write(wd + '\t' + parsing + '\n')























































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


# # remove unwanted symbols from word before passing it
# # def matching_based_parse(word, prefix_encodings, seed_word_encodings, symboltable, debug=True):
# #     if g.flags.DEBUG:
# #          print(f'debugging {word}')
#     # if word == '':
#     #     return []
    
#     # spword = split_word(word, symboltable)
#     # prefixes = []
#     # # prefixes = generate_prefixes(spword)
    
#     # # print("list of prefixes")
#     # # print(prefix_encodings)
#     # match_prefix, pref_ans = [], []
#     # for pref in prefixes:
#     #     if prefix_encodings.count(pref) != 0:
#     #         # print(match_prefix)
#     #         match_prefix = pref
#     #         _, pref_ans = safe_word_parse(''.join(match_prefix), 0, 0, 0)
#     #         pref_ans = [pref_ans]
#     #         break
#     # remword = spword[len(match_prefix):]
#     # if debug:
#     #     print(f'found prefix {"".join(match_prefix)}')
#     #     print(f'remaining - {remword}')
#     #     print(f'spword - {spword}')
#     # remword = spword[len(match_prefix):]

#     # sublists = generate_sublists(remword)
#     # print(sublists)
#     # matching_sublists = []
#     # for sublist, begpos, endpos in sublists:
#     #     if seed_word_encodings.count(sublist) != 0:
#     #         matching_sublists.append((sublist, begpos, endpos))
    
#     # if len(matching_sublists) == 0:
#     #     _, ans = safe_word_parse(''.join(remword), 0, 0, 0)
#     #     ans = [ans]
#     #     return pref_ans + ans

#     # max_matching_sublists = weighted_activity_selection(matching_sublists, debug)
#     # if debug:
#     #     for l, _, _ in max_matching_sublists:
#     #         wd = ''.join(l)
#     #         print(l, wd)
    
#     # idx = 0
#     # cur_act = 0
#     # parsings = pref_ans
#     # while idx < len(remword):

#     #     if cur_act == len(max_matching_sublists):
#     #         word = ''
#     #         while (idx < len(remword)):
#     #             word += remword[idx]
#     #             idx += 1
#     #         if word != '':
#     #             _, parsing = safe_word_parse(word, 0, 0, 0)
#     #             parsings += [parsing]
#     #         break

#     #     word = ''
#     #     while (idx < max_matching_sublists[cur_act][1]):
#     #         word += remword[idx]
#     #         idx += 1
#     #     if word != '':
#     #         _, parsing = safe_word_parse(word, 0, 0, 0)
#     #         parsings += [parsing]
        
#     #     word = ''
#     #     while (idx <= max_matching_sublists[cur_act][2]):
#     #         word += remword[idx]
#     #         idx +=1
#     #     if word != '':
#     #         _, parsing = safe_word_parse(word, 0, 0, 0)
#     #         parsings += [parsing]
        
#     #     cur_act += 1
#     # if debug:
#     #     print(f'parsings - {parsings}')
#     # return parsings
    




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
