import pandas as pd
import numpy as np
import re
import random

###############################################
# parse_text
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
    return line

def remove_numb_semicol_numb(line):
    line_out = []
    for word in line.split(' '):
        if ':' in word:
            words = word.split(':')
            if len(words) > 1:
                if not (words[0].isnumeric() and words[1].isnumeric()):
                    line_out.append(word)
            else:
                line_out.append(word)
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

def parse_text(fileName, parse=True, min_chars_per_line=5):
    """Parse a book into a list of sentances, separated by a dot
    """
    txt_lines_in = open(fileName).readlines()
    if parse:
        txt_out = []
        for line in txt_lines_in:
            if len(line) >= min_chars_per_line:
                line = line.lower()
                line = remove_brackets(line)
                line = remove_new_line_symbol(line)
                line = parse_sed_words_endings(line)
                line = remove_numb_semicol_numb(line)
                line = separate_punctuation(line)
                txt_out.append(line)
        txt_out = ' '.join(txt_out)
        txt_out = split_by_sentence(txt_out)
    else:
        txt_out = txt_lines_in
    return txt_out
###############################################
# END parse_text
###############################################




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

def get_word_counts_and_freqs_df(parsed_book, words_dict):
    counts = [0]*len(words_dict)
    for line in parsed_book:
        for word in line.split(' '):
            counts[words_dict[word]] += 1
    counts_sum = np.sum(counts)
    count_freqs = []
    for count in counts:
        count_freqs.append(count/counts_sum)
    df = pd.DataFrame({'word': list(words_dict.keys()),
                      'count': counts,
                      'freq': count_freqs} )
    return df
           
    
def get_mean_freq_diff(sample_1, sample_2, words_dict):
    # Sample 1:
    df1 = get_word_counts_and_freqs_df(sample_1, words_dict)
    df1 = df1.rename(columns={'count': 'count1', 'freq': 'freq1'})
    # Sample 2:
    df2 = get_word_counts_and_freqs_df(sample_2, words_dict)
    df2 = df2.rename(columns={'count': 'count2', 'freq': 'freq2'})
    # df:
    df = df1.merge(df2, on='word', how='inner')
    df['freq_diff'] = abs(df['freq1']-df['freq2'])
    # freq_diff_mean:
    freq_diff_mean = df['freq_diff'].mean()
    return freq_diff_mean
    
def freq_perm_test(parsed_book_1, parsed_book_2, n_tests=10, perms_per_test=100, do_perm_testing=True, sample_len=False):
    """
    Uses permutation testing to compare the two texts:
    
    Example usage:
    Apocryphon = 'temp_data/The Apocryphon of John.txt'
    Revelation = 'temp_data/The Revelation of Saint John the Divine.txt'
    freq_perm_test(parse_text(Revelation), parse_text(Apocryphon), n_tests=10, perms_per_test=100)
    
    Output:
    Real freq diff: 0.00039689116497929256
    Mean perm freq diff: 0.00016977974260111298
    Zero hypothesis prob: 0.0 (0 out of 1000 tests had bigger freq diffs)
    """
    words_dict = get_words_dict([parsed_book_1, parsed_book_2])
    least_len = min(len(parsed_book_1), len(parsed_book_2))
    if sample_len:
        if sample_len < least_len:
            least_len = sample_len
        else:
            print(f'WARNING: Input sample_len [{sample_len}] is bigger than least_len [{least_len}]. Using least_len...')
    
    freq_diff_mean_reals_list = []
    freq_diff_mean_perms_list = []
    freq_bigger = 0
    
    for test in range(n_tests):
        # Real freq diff:
        sample_1 = random.sample(parsed_book_1, least_len)
        sample_2 = random.sample(parsed_book_2, least_len)
        freq_diff_mean_real = get_mean_freq_diff(sample_1, sample_2, words_dict)
        freq_diff_mean_reals_list.append(freq_diff_mean_real)
        if do_perm_testing:
            # Permutation test:
            all_samples = sample_1 + sample_2
            for perm in range(perms_per_test):
                psample = all_samples.copy()
                random.shuffle(psample)
                psample_1 = psample[:int(len(psample)/2)]
                psample_2 = psample[int(len(psample)/2):]
                freq_diff_mean_perm = get_mean_freq_diff(psample_1, psample_2, words_dict)
                freq_diff_mean_perms_list.append(freq_diff_mean_perm)
                if freq_diff_mean_perm > freq_diff_mean_real:
                    freq_bigger += 1
                
    if do_perm_testing:
        zero_hypothesis_prob = freq_bigger/(perms_per_test*n_tests)
        print(f'Real freq diff: {np.mean(freq_diff_mean_reals_list)}')
        print(f'Mean perm freq diff: {np.mean(freq_diff_mean_perms_list)}')
        print(f'Zero hypothesis prob: {zero_hypothesis_prob} ({freq_bigger} out of {perms_per_test*n_tests} tests had bigger freq diffs)')
    return np.mean(freq_diff_mean_reals_list)