import sys, os, glob, fitz
from pathlib import Path
from string import punctuation
from nltk.tokenize import word_tokenize

PROJ_DIR = os.path.dirname(os.path.realpath('__file__'))
DATA_DIR = os.path.join(PROJ_DIR, 'DATA')
KEYWORDS_DIR = os.path.join(PROJ_DIR, 'KEYWORDS')

# For ref: https://usefulshortcuts.com/alt-codes/bullet-alt-codes.php
def tokenize(pdfs_dict):
    pdfs_dict_tokens = {}
    remove_list = list(set(punctuation)) + ["♦", "•", "◘", "○", "◙", "--", "``", "–", "//", "’" , "●",]
    for key, value in pdfs_dict.items():
        list_tokens = word_tokenize(value)
        list_tokens = list(filter(lambda i: i not in remove_list, list_tokens))
        pdfs_dict_tokens[key] = list_tokens
    return pdfs_dict_tokens

# For ref: https://pymupdf.readthedocs.io/en/latest/document.html#document
def readfiles():
    pdf_text, pdfs_dict, keyword_list =  "", {}, []
    for pdf_file in glob.glob(os.path.join(DATA_DIR, '*.pdf')):
        with fitz.open(pdf_file) as doc:
            # read each page
            for page in doc: 
                pdf_text += page.getText("text")
        # get pdf file name
        pdf_filename = os.path.basename(pdf_file)
        # save the read pdf in dict
        pdfs_dict[pdf_filename] = pdf_text
    
    for keyword_file in glob.glob(os.path.join(KEYWORDS_DIR, '*.txt')):
        with open(keyword_file , 'r') as file:
            keyword_list = file.read().split("\n")

    return(pdfs_dict,keyword_list)

def main():
    pdfs_dict,keyword_list = readfiles()
    pdfs_dict_tokens = tokenize(pdfs_dict)
    print(pdfs_dict_tokens)
    print("\n Keyword list")
    print(keyword_list)

if __name__ == "__main__":
    main()