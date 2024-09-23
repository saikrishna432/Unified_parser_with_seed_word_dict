path="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/correct_13000_from_sudhanshu.words"

with open(path, 'r') as ipf:
    lines= ipf.readlines()
# print(lines)
path_out='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/13000_words.txt'
with open(path_out,'w') as opf:
    for line in lines:
        print(line)
        txt1, txt2= line.split("\t")
        opf.write(txt1)
        opf.write("\n")