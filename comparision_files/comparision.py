# path_corrected="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/correct_13k_from_sudhanshu.words"
path_old_parser_output="/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/old_parser_big_dict.txt"
path_seed_2_letters='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/new_parser_big_dict.txt'
# path_seed_3_letters='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/comparision_files/seed_words_out3.txt'

corrected=[]
old_parser_output=[]
seed_2_letters=[]
seed_3_letters=[]

# with open(path_corrected,'r') as opf_corrected:
#     corrected= opf_corrected.readlines()
with open(path_old_parser_output,'r') as opf_old_parser_output:
    old_parser_output= opf_old_parser_output.readlines()
with open(path_seed_2_letters,'r') as opf_seed_2_letters:
    seed_2_letters= opf_seed_2_letters.readlines()
# with open(path_seed_3_letters,'r') as opf_seed_3_letters:
#     seed_3_letters= opf_seed_3_letters.readlines()

n=len(old_parser_output) 
m=len(seed_2_letters)
print('old_parser_output:',len(old_parser_output))
print("seed_2_letters:",len(seed_2_letters))
common=[]
not_common=[]

for i in range(n):
    # found=False
    # print(corrected[i])
    # print(old_parser_output[i])
    # print(seed_2_letters[i])
    # print(seed_3_letters[i])
    # if (corrected[i]== old_parser_output[i]):# and (corrected[i]==seed_2_letters[i]) and (corrected[i] == seed_3_letters[i]):
    #     common.append(i)
        # print(i)
    # if (corrected[i]==seed_3_letters[i]):# and (corrected[i] == seed_3_letters[i]):
    #     common.append(i)
    # for j in range(m):
        # print(i,j)
    # print(old_parser_output[i], seed_2_letters[i])
    if (old_parser_output[i] == seed_2_letters[i]):         
        # found=True
    # if found==False:
    #     print(found)
        common.append(i)
        # print(i)
    # if (seed_2_letters[i]== seed_3_letters[i]):
    #     common.append(i)
l=(n-len(common))
print("Number of lines which are not common:",(n-len(common)) )
k=len(common)
path_comparision='/home/speech/Desktop/Unified_Parser_smt_lab_IITM/big_dict_hindi/comparasion_big_dict.txt'

with open(path_comparision,'w') as opf:
    for i in range(k):
        if i in common:
            continue
        # opf.write(f"{i}:1 {corrected[i]}\n")
        opf.write(f"{i}:2 {old_parser_output[i]}\n")
        opf.write(f"{i}:3 {seed_2_letters[i]}\n")
        # opf.write(f"{i}:4 {seed_3_letters[i]}\n")
        # opf.write(f"{old_parser_output[i]}")

    