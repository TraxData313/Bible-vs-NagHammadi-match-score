import pandas as pd
import numpy as np
import random
import data_prep as dp
import matplotlib.pyplot as plt


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

def get_words_dict(list_of_lines):
    word_dict = {}
    index = 0
    for line in list_of_lines:
        for word in line.split(' '):
            if word not in list(word_dict.keys()):
                word_dict[word] = index
                index += 1
    return word_dict


def freq_compare_with_Bible(df, who='TEXT_NAME', name='The Apocryphon of John', words_dict=None, count_words=False):
    """Gets word frequency for the Bible (without the text, if the text is in the Bible),
    Gets word freq for the text,
    Returns log of the mean absolute word freq difference of the two texts
    
    if the word_dict is not passed it will be created (takes a few minutes, so better create it and pass it)
    """
    # - Word dict on all possible words:
    if words_dict is None:
        print('- Getting word dict...')
        words_dict = get_words_dict(list(df['sentence']))
    # - Bible df:
    bdf_cond = (df['LIBRARY'].isin(['OT', 'NT']))&(df[who]!=name)
    bdf = df.loc[bdf_cond]
    # - Text df:
    tdf = df.loc[df[who]==name]
    # - Freq comparison:
    #print(f'- Calculating log mean abs freq diff for [{name}]...')
    freq_diff = get_mean_freq_diff(list(bdf['sentence']), list(tdf['sentence']), words_dict)
    freq_diff = np.log(freq_diff)
    if count_words:
        word_count_diff = tdf.words_count.mean() - bdf.words_count.mean()
        return freq_diff, word_count_diff
    else:
        return freq_diff
    
def freq_compare_with_Bible_loop(df, words_dict, texts='all'):
    #texts: all, Bible/Control
    if texts == 'all':
        # - All texts:
        print('Comparing all texts...')
        texts = list(df.loc[df['LIBRARY'].isin(['OT','NT','NH','Control'])]['TEXT_NAME'].unique())
    else:
        # - Bible vs control:
        print('Comparing Bible (OT,NT) with Control texts only (no NH)...')
        texts = list(df.loc[df['LIBRARY'].isin(['OT','NT','Control'])]['TEXT_NAME'].unique())
    results = {}
    LIBRARYs = []
    AUTHORs = []
    TRANSLATIONs = []
    AUTHOR_LIBRARYs = []
    word_count_diffs = []
    for text in texts:
        LIBRARYs.append(df.loc[df['TEXT_NAME']==text]['LIBRARY'].unique()[0])
        AUTHORs.append(df.loc[df['TEXT_NAME']==text]['AUTHOR'].unique()[0])
        TRANSLATIONs.append(df.loc[df['TEXT_NAME']==text]['TRANSLATION'].unique()[0])
        AUTHOR_LIBRARYs.append(df.loc[df['TEXT_NAME']==text]['AUTHOR_LIBRARY'].unique()[0])
        freq_diff, word_count_diff = freq_compare_with_Bible(df, who='TEXT_NAME', name=text, words_dict=words_dict, count_words=True)
        results[text] = freq_diff
        word_count_diffs.append(word_count_diff)
    results = pd.DataFrame({
        'TEXT': results.keys(), 
        'LIBRARY': LIBRARYs,
        'AUTHOR': AUTHORs,
        'TRANSLATION': TRANSLATIONs,
        'AUTHOR_LIBRARY': AUTHOR_LIBRARYs,
        'freq_diff': results.values(),
        'word_diff': word_count_diffs
    })
    results.sort_values('freq_diff', ascending=False).reset_index(drop=True)
    print('- Done!')
    return results
    
def get_plt_colors(whos):
    colors = []
    color_dict = {'OT': 'blue', 'NT': 'dodgerblue', 'Control': 'green', 'NH': 'purple'}
    for who in whos:
        who = who.split('_')[-1]
        colors.append(color_dict[who])
    return colors
    
def word_freq_and_count_plot(results, who='AUTHOR_LIBRARY'):
    # - Data:
    results_agr = results.groupby(who).agg({'freq_diff': 'mean', 'word_diff': 'mean'}).reset_index().sort_values('freq_diff', ascending=False).reset_index(drop=True)
    X = results_agr['freq_diff']
    Y = results_agr['word_diff']
    whos = results_agr[who]
    
    # - Plot the data:
    colors = get_plt_colors(whos)
    fig = plt.figure(figsize=(20,10))
    plt.scatter(X, Y, c=colors, marker='o', s=200)
    for i, txt in enumerate(whos):
        plt.annotate(txt, (X[i], Y[i]), 
                     verticalalignment='bottom', 
                     fontsize={'AUTHOR_LIBRARY': 10, 'LIBRARY': 15}[who], 
                     horizontalalignment='left', 
                     rotation=10)
        
    # - Plot Labels and Title:
    font1 = {'family':'serif','color':'black','size':25}
    font2 = {'family':'serif','color':'darkred','size':25}
    plt.title(f"Word Freq and Count diff for every {who}", fontdict = font1, 
              loc = 'left' # def=center
             )
    plt.xlabel(f"Log of Mean Abs sentence Word Freq Diff*", fontdict = font2)
    plt.ylabel(f"Mean sentence words count more by*", fontdict = font2)
        
    plt.show()
    print(f'*between the [{who}] and the Bible (or with the rest of the Bible excluding the text, if the text is part of the Bible itself)')
    print('- Dark Blue: The Bible - Old Testament')
    print('- Light Blue: The Bible - New Testament')
    print('- Purple: Nag Hammadi')
    print('- Green: Control group')

def perm_test(full_sim_sample, real_sample, P=100000, rounder_dgts=7):
    """Sample output:
    Doing permutation test for real sample of lenght [6] and [10000] permutations...
    - real_mean_dif: 0.5038873
    - sims_mean_dif (ave): 0.0008777
    - P-value based on mean   difs: [0.08%]

    Normal hypothesis confirm:
    - P-value based on mean is smaller than (0.05)**[6] as % or [5.0%], aka Zero-Hypothesis may be True: [False]
    """
    full_sim_sample = list(full_sim_sample)
    real_sample = list(real_sample)
    sampl_size = len(real_sample)
    print(f'Doing permutation test for real sample of lenght [{sampl_size}] and [{P}] permutations...')
    sim_sample = random.sample(full_sim_sample, sampl_size)
    full_list = real_sample+sim_sample
    # Real mean_dif:
    real_mean_dif = abs(np.mean(real_sample) - np.mean(sim_sample))
    print('- real_mean_dif:', round(real_mean_dif,7))
    # P permutation tests:
    bigger_mean_dif = 0
    sim_mean_difs = []
    for i in range(P):
        random.shuffle(full_list)
        # - Mean test:
        perm_mean_dif = abs(np.mean(full_list[:sampl_size]) - np.mean(full_list[sampl_size:]))
        sim_mean_difs.append(perm_mean_dif)
        if perm_mean_dif >= real_mean_dif:
            bigger_mean_dif+=1
    print('- sims_mean_dif (ave):', round(np.mean(sim_mean_difs),rounder_dgts))
    # Evaluate the p-value:
    p_value_on_means_perc = bigger_mean_dif*100/P
    print(f'- P-value based on mean |difs: [{p_value_on_means_perc}%]')
    # - Hypothesis confirm:
    print()
    print('Normal hypothesis confirm:')
    lowest_p_value_perc = (0.05)*100
    p_value_on_means_confirmed = p_value_on_means_perc > lowest_p_value_perc
    print(f'- P-value based on mean is smaller than [{lowest_p_value_perc}%], aka Zero-Hypothesis may be True: [{p_value_on_means_confirmed}]')
    return p_value_on_means_perc
    
if __name__ == '__main__':
    Apocryphon = 'temp_data/The Apocryphon of John.txt'
    Revelation = 'temp_data/The Revelation of Saint John the Divine.txt'
    freq_perm_test(dp.parse_text(Revelation), dp.parse_text(Apocryphon), n_tests=10, perms_per_test=100)