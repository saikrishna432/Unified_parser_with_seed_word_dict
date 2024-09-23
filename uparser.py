# import sys, os
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(SCRIPT_DIR)

# combined lexical analyzer and parser
from tqdm import tqdm
from ply.lex import Lexer
from ply.yacc import yacc
from globals import *
from helpers import *
import sys
from sys import exit
from joblib import Parallel, delayed
from tqdm import tqdm
from get_phone_mapped_python import *

# tokens used
tokens = ('kaki_c', 'conjsyll2_c', 'fullvowel_b', 'kaki_a', 'kaki_b',  'conjsyll2_b', 'conjsyll2_a',
        'conjsyll1', 'nukchan_b','nukchan_a', 'yarule', 'fullvowel_a', 'vowel')

# parser part

def p_sentence(p):
    '''
    sentence : words
    '''
    if p.parser.g.flags.parseLevel == 0:
        p.parser.g.words.syllabifiedWordOut = p[1]

        if p.parser.g.words.syllabifiedWordOut.find('&&') != -1:
            p.parser.g.words.syllabifiedWordOut = rec_replace(p.parser.g.words.syllabifiedWordOut,'&&','&')
        
        p.parser.g.flags.parseLevel += 1
    else:
        p.parser.g.words.phonifiedWord = p[1]

def p_words_syltoken(p):
    '''
    words : syltoken
    '''
    if(p.parser.g.flags.DEBUG):
        print(f"Syll:\t{p[1]}")
    p[0] = p[1]

def p_words_wordsandsyltoken(p):
    '''
    words : words syltoken
    '''
    if(p.parser.g.flags.DEBUG):
        print(f"Syll:\t{p[2]}")
    p[0] = p[1] + p[2]

def p_syltoken(p):
    '''
    syltoken : fullvowel_b
             | fullvowel_a
             | conjsyll2_c
             | conjsyll2_b
             | conjsyll2_a
             | conjsyll1 
             | nukchan_b
             | nukchan_a
             | yarule
             | vowel
    '''
    p[0] = p[1]

def p_syltoken1(p):
    '''
    syltoken :
             | kaki_c
             | kaki_a
             | kaki_b
    '''
    if (p.parser.g.flags.DEBUG):
        print(f'kaki : {p[1]}')
    p[0] = p[1]

def p_error(p):
    print('parse error')
    exit(1)

# print the help of syntax
def printHelp():

    print("UnifiedParser - Usage Instructions")
    print("Run python3 parser.py wd lsflag wfflag clearflag")
    print("wd - word to parse in unicode.")
    print("lsflag - always 0. we are not using this.")
    print("wfflag - 0 for Monophone parsing, 1 for syllable parsing, 2 for Akshara Parsing")
    print("clearflag - 1 for removing the lisp like format of output and to just produce space separated output. 0. for normal syntx, 2 for cls labled output")
    print("language - name of language in quationes")



def wordparse(wd : str, lsflag : int, wfflag : int, clearflag : int, language_main :str):
    # print("language:",language)
    g = GLOBALS()
    lexer = Lexer()
    parser = yacc()
    parser.g = g
    g.flags.DEBUG = False
    wd = wd.strip('  ') # hidden characters

    if lsflag not in [0,1] or wfflag not in [0,1,2]:
        print("Invalid input")
        exit(1)
    
    g.flags.LangSpecificCorrectionFlag = lsflag
    
    g.flags.writeFormat = wfflag
    if wfflag == 4:
        g.flags.writeFormat = 1
        g.flags.syllTagFlag = 1
    
    word = wd
    if g.flags.DEBUG:
        print(f'Word : {word}')

    word = RemoveUnwanted(word)
    if g.flags.DEBUG:
        print(f'Cleared Word : {word}')
    print(word)
    if SetlanguageFeat(g, word) == 0:
        return 0
    
    if CheckDictionary(g, word) != 0:
        return 0

    if g.flags.DEBUG:
        print(f'langId : {g.langId}')
    
    word = ConvertToSymbols(g, word)

    if g.flags.DEBUG:
        print(f"Symbols code : {g.words.unicodeWord}")
        print(f"Symbols syllables : {g.words.syllabifiedWord}")

    if language_main == "sanskrit":
        g.currLang = g.TELUGU
        g.langId = g.TELUGU
        # g.currLang = g.SANSKRIT
        # g.langId = g.SANSKRIT
        if(g.langId < 5 or g.langId ==10 ):
            g.isSouth = 1
        g.flags.LangSpecificCorrectionFlag=1
        print("language:",language_main)
        print("one one:",g.langId, g.currLang, g.isSouth )
    print("Word before lex and Yacc parser:",g.words.syllabifiedWord)
    parser.parse(g.words.syllabifiedWord, lexer=lexer)
    print("Word before lex and Yacc parser:",g.words.syllabifiedWordOut)
    if(g.flags.DEBUG):
        print(f"Syllabified Word : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = rec_replace(g.words.syllabifiedWordOut, '&#&','&') + '&'
    if(g.flags.DEBUG):
        print(f"Syllabified Word out : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = LangSpecificCorrection(g, g.words.syllabifiedWordOut, g.flags.LangSpecificCorrectionFlag)
    if(g.flags.DEBUG):
        print(f"Syllabified Word langCorr : {g.words.syllabifiedWordOut}")
    # if(g.flags.DEBUG):
    #     print(f"Syllabified Word gemCorr : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)
    if(g.flags.DEBUG):
        print(f"Syllabified Word memCorr : {g.words.syllabifiedWordOut}")

    if not g.isSouth:
        if g.flags.DEBUG:
            print('NOT SOUTH')
        count = 0
        for i in range(len(g.words.syllabifiedWordOut)):
            if g.words.syllabifiedWordOut[i] == '&':
                count += 1
        splitPosition = 2
        if GetPhoneType(g, g.words.syllabifiedWordOut, 1) == 1:
            if count > 2:
                tpe = GetPhoneType(g, g.words.syllabifiedWordOut, 2)
                if tpe == 2:
                    splitPosition = 1
                elif tpe == 3:
                    splitPosition = 3
            else:
                splitPosition = 1
        count = 0
        for i in range(len(g.words.syllabifiedWordOut)):
            if g.words.syllabifiedWordOut[i] == '&':
                count += 1
            if count > splitPosition:
                count = i
                break
        start, end = g.words.syllabifiedWordOut, g.words.syllabifiedWordOut
        end = end[count:]
        start = start[:count]
        if(g.flags.DEBUG):
            print(f"posi {count} {start} {end}")
        end = SchwaSpecificCorrection(g, end)
        if(g.flags.DEBUG):
            print(f"prefinal : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = start + end
        if(g.flags.DEBUG):
            print(f"prefinal1 : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)
        if(g.flags.DEBUG):
            print(f"final : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = SchwaDoubleConsonent(g.words.syllabifiedWordOut)
        if(g.flags.DEBUG):
            print(f"final0 : {g.words.syllabifiedWordOut}")
    
    g.words.syllabifiedWordOut = GeminateCorrection(g.words.syllabifiedWordOut, 0)
    g.words.syllabifiedWordOut = MiddleVowel(g, g.words.syllabifiedWordOut)
    g.words.syllabifiedWordOut = Syllabilfy(g,g.words.syllabifiedWordOut)
    
    SplitSyllables(g,g.words.syllabifiedWordOut)
    if g.flags.DEBUG:
        print("control_1")
        print(g.words.syllabifiedWordOut)
    
    # if language_main == g.currLang
    # g.words.syllabifiedWordOut=convert_to_main_lang (g,g.words.syllabifiedWordOut, language_main)
        print("control_2",g.words.syllabifiedWordOut)
    temp_list=g.syllableList

    if g.flags.DEBUG:
        print("temp_list_1",temp_list)

    # for i in range(len(temp_list)):
    #     print("temp_word_a",temp_list[i])
    #     temp_list[i]=convert_to_main_lang (g,temp_list[i], language_main)
    #     print("temp_word_b",temp_list[i])

    WritetoFiles(g)
    if clearflag == 0:
        return g.words.outputText
    if clearflag == 1:
        t = g.words.outputText
        t = t.split('"')
        ln = len(t)
        i = 1
        g.answer = ''
        while i < ln:
            g.answer += t[i] + ' '
            i += 2
        g.answer.strip()
        return g.answer
    print("output text:",g.words.outputText)
    if clearflag == 2:
        t = g.words.outputText
        t = t.split('"')
        print(t)
        ln = len(t)
        i = 1
        g.answer = ''
        text_replacer=TextReplacer()
        while i < ln:
            if len(t[i])>1 and ord(t[i][0])<128 and ord(t[i][0])>=65:
                temp = text_replacer.apply_replacements_by_phonems(t[i])
                g.answer += temp
            elif len(t[i])==1 and ord(t[i][0])<128 and ord(t[i][0])>=65:
                g.answer += t[i]
            i += 1
        g.answer.strip()
        return g.answer


def safe_word_parse(wd : str, lsflag : int, wfflag : int, clearflag : int,language : str):
    try:
        ans = wordparse(wd, lsflag, wfflag, clearflag,language)
        print(ans) 
    except:
        print(f'failed on {wd}')
        ans = 'FAILED', 'FAILED'
    return wd, ans,

if __name__ == '__main__':

    if (len(sys.argv) != 6):
        printHelp()
        exit(-1)
    
    ans = wordparse(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),str(sys.argv[5]))
    print(ans)

    # words = []
    # # path='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/13000_words_s.txt'
    # path="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/seed_words_out_1k_2.txt"
    # path2="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/new_comp/new_seed_res_prefex_suffex.txt"
    # path3="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/new_comp/not_common_suffix.txt"
    # path4="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/new_parser_big_dict.txt"
    # with open(path4, 'r') as fl:
    #     cnts = fl.readlines()
    #     for ln in cnts:
    #         ln,_ = ln.split("\t")
    #         words.append(ln)
    # # print(words)
    # # words=["स्त्री","ज़िलाअध्यक्ष"]
    # words=['हौंसला','किंकर्तव्यविमूढ़','अवधिप्रतिबंधकसमिति']
    # words=["ਅੰਗੂਰੀ","ਮੇਰੇ","ਗਵਾਂਢੀਆਂ","ਦੇ","ਗਵਾਂਢੀਆਂ"]#, "ਦੇ ਗਵਾਂਢੀਆਂ ਦੇ ਘਰ, ਉਹਨਾਂ ਦੇ ਬੜੇ ਪੁਰਾਣੇ ਨੌਕਰ ਦੀ ਬੜੀ ਨਵੀਂ ਬੀਵੀ ਹੈ।"]
    # words=words[:50]
    words=["केशव","वामसी"]
    words=["शृगालः","रघुवंशः","दुःखेन","राष्ट्रपतिः"]
    # words=["सः"]
    # words=['ఎవరైనా']#,"స్పృహ","ప్రత్యేక","ఉన్నారు","చెబుతునే"]
    # words=['वामसी','केन्द्रीयान्वेषणविभागेन','कतिचिदर्बुदराशि','बैंक','ऋणस्य', 'प्रत्यावर्तनप्रकरणस्यान्वीक्षणम्','अद्य', 'द्वितीये','नेऽपि','क्रियते']
    # words=['అనిర్వచనీయము']
    items = []
    # # anslist = Parallel(n_jobs=10)(delayed(wordparse)(wd, 0, 0, 0, "hindi") for wd in tqdm(words))

    # for wd in tqdm(words):
    #     items.append(safe_word_parse(wd,0,0,1,"sanskrit"))
    #     #items.append(wordparse(wd,0,0,0,"sanskrit"))
    #     print(items)

    # path_out="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/old_parser_out_1k_2.txt"
    # # path_out='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/old_parser_oput.txt'
    # path_out_2="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/new_comp/new_old_parcer_res_suffex.txt"
    # path_out_4="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/old_parser_big_dict.txt"
    
    # with open(path_out_4, 'w') as f:
    #     # for wd, parsing in items:
    #     #     f.write(wd + '\t' + parsing + '\n')
    #     for item in items:
    #         if len(item) == 2:
    #             wd, parsing = item
    #             parsing= f"(set! wordstruct '( {parsing}))"
    #             f.write(wd + '\t' + parsing + '\n')
    #         else:
    #             print(f"Skipping item: {item}")


