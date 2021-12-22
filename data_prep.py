import pandas as pd
import numpy as np
import re




###############################################
# SUB FUNCTIONS
###############################################
def remove_new_line_symbol(line):
    if line[-1:] == '\n':
        line = line[:-1]
    return line

def parse_sed_words_endings(line):
    line = line.replace("â€™s", "s")
    line = line.replace("'", "s")
    return line

def remove_brackets(line):
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.replace("<", "")
    line = line.replace(">", "")
    line = line.replace("{", "")
    line = line.replace("}", "")
    line = line.replace("...", "")
    line = line.replace("'", "")
    line = line.replace('"', "")
    line = line.replace("-", "")
    line = line.replace("line unrecoverable", "")
    line = line.replace("lines unrecoverable", "")
    return line

def remove_line_markers(line):
    line_out = []
    for word in line.split(' '):
        if (':' in word) and (len(word) > 1):
            words = word.split(':')
            if (words[0].isnumeric()) and (words[1].isnumeric()):
                pass #word is a line marker like (23) - skip it
            else:
                line_out.append(word)
        elif (len(word) > 1) and (word[0]=='(') and (word[-1]==')') and ((word[1:-1].isnumeric()) or (word[1:-2].isnumeric())):
            pass #word is a line marker like (23) or (252a) - skip it
        elif word.isnumeric():
            pass #remove numbers
        else:
            line_out.append(word)
    return ' '.join(line_out)

def separate_punctuation(line):
    line = re.findall(r"[\w']+|[.,!?;]", line)
    return ' '.join(line)

def split_by_sentence(text):
    lines = text.split('.')
    lines_new = []
    for line in lines:
        if len(line)>1:
            while line[0] == ' ':
                line = line[1:]
            while line[-1] == ' ':
                line = line[:-1]
            lines_new.append(line)
    return lines_new

def remove_numbers(text):
    new_line = []
    for word in text.split(' '):
        if not word.isnumeric():
           new_line.append(word)
    return ' '.join(new_line)
###############################################
# END SUB FUNCTIONS
###############################################







###############################################
# MAIN FUNCTONS
###############################################
def parse_text(fileName, parse=True, min_chars_per_line=3):
    """Parse a book into a list of sentances, separated by a dot
    """
    txt_lines_in = open(fileName).readlines()
    if parse:
        txt_out = []
        for line in txt_lines_in:
            if len(line) >= min_chars_per_line:
                line = line.lower()
                line = remove_line_markers(line)
                line = remove_brackets(line)
                line = remove_new_line_symbol(line)
                line = parse_sed_words_endings(line)
                line = separate_punctuation(line)
                line = remove_numbers(line)
                if len(line) >= min_chars_per_line:
                    txt_out.append(line)
        txt_out = ' '.join(txt_out)
        txt_out = split_by_sentence(txt_out)
    else:
        txt_out = txt_lines_in
    return txt_out

def get_words_dict(list_of_lines):
    word_dict = {}
    index = 0
    for _list in list_of_lines:
        for line in _list:
            for word in line.split(' '):
                if word not in list(word_dict.keys()):
                    word_dict[word] = index
                    index += 1
    return word_dict
###############################################
# END MAIN FUNCTONS
###############################################



if __name__ == '__main__':
    pass