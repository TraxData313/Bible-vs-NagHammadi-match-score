import pandas as pd
import numpy as np
import re
import os




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
    line = line.replace("_", "")
    line = line.replace("â", "a")
    line = line.replace("ã", "a")
    line = line.replace("ž", "z")
    line = line.replace("ª", "a")
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
###############################################
# END SUB FUNCTIONS
###############################################







###############################################
# MAIN FUNCTONS
###############################################
def print_dataset_stats(df, who='LIBRARY', what='char_count'):
    """Prints WHAT stats by WHO, for example word_cout stats per AUTHOR
    df: df as returned from return_dataset()
    who: LIBRARY, AUTHOR, TEXT_NAME, TRANSLATION
    what: char_count, words_count
    
    Example output:
    - LIBRARY [OT] has [19792] sentences with mean char_count: [161], and std of [118.58]
    - LIBRARY [NT] has [6412] sentences with mean char_count: [148], and std of [106.58]
    - LIBRARY [NH] has [9374] sentences with mean char_count: [106], and std of [88.75]
    - LIBRARY [Control] has [741] sentences with mean char_count: [108], and std of [131.65]
    """

    for a in df[who].unique():
        adf = df.loc[df[who]==a]
        print(f'- {who} [{a}] has [{len(adf)}] sentences with mean {what}: [{int(adf[what].mean())}], and std of [{round(adf[what].std(),2)}]')

def return_dataset():
    """Parses all the texts in the folders:
    - data/Bible - King James
    - data/Nag Hammadi
    - data/Control texts

    Returns df with columns:
    'sentence' - every sentences text
    'NUM' - id in the folder (ex book: 011)
    'LIBRARY' - libraty in the folder (ex book: OT for Old Testament)
    'AUTHOR' - the author of the book (ex book: Unknown)
    'TEXT_NAME' - the book name (ex book: The Third Book of the Kings)
    'TRANSLATION' - the name of the translation person or standard (ex book: King James)
    'char_count' - how many characters in the sentence
    'words_count' - how many words in the sentence (symbols like ? or ; count as a word here)
    # ex book used: 011,OT,Unknown,The Third Book of the Kings,King James.txt
    """
    # - Get the df:
    lines = []
    numbers = []
    libraryes = []
    authors = []
    text_names = []
    translations = []
    folders = ['data/Bible - King James', 'data/Nag Hammadi', 'data/Control texts']
    for folder in folders:
        for file in os.listdir(folder):
            try:
                # - Extract the text in lines:
                folder_file = f"{folder}/{file}"
                new_lines = parse_text(folder_file)
                lines += new_lines
                # - Make the LABELS for each line:
                txt_labels = file.split(',')
                txt_labels[-1] = txt_labels[-1].split('.')[0] #remove the .txt at the end of the file
                for i in range(len(new_lines)):
                    numbers.append(txt_labels[0])
                    libraryes.append(txt_labels[1])
                    authors.append(txt_labels[2])
                    text_names.append(txt_labels[3])
                    translations.append(txt_labels[4])
            except Exception as e:
                print(f'WARNING: Coudnlt parse {file} due to {e}')
    df_dict = {
        'sentence': lines,
        'NUM': numbers,
        'LIBRARY': libraryes,
        'AUTHOR': authors,
        'TEXT_NAME': text_names,
        'TRANSLATION': translations
    }
    df = pd.DataFrame(df_dict)
    df['char_count'] = df['sentence'].str.len()
    df['words_count'] = df['sentence'].str.split().apply(len)
    return df
###############################################
# END MAIN FUNCTONS
###############################################



if __name__ == '__main__':
    print('Doing "df = return_dataset()" to get the df...')
    df = return_dataset()
    print('Done! df returned!')
    print(df.sample(5))