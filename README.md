# Bible-vs-NagHammadi-match-score
Is Nag Hammadi library part of the Bible? Use NLP techniques to get match score between the texts and try to answer that controversial question.

<hr>
<br>

## Description and goal:
- **[The Bible](https://en.wikipedia.org/wiki/Bible)**: The early Church arranged scripts, letters, ghospels and other texts related to the teachings of Jesus Christ and created the Bible
- **[Gnostic texts](https://en.wikipedia.org/wiki/Gnostic_texts)**: Other texts were labeled as faked or heresy and were rejected. A lot of those texts were destroyed. They are also known as Gnostic texts
- **[Nag Hammadi library](https://en.wikipedia.org/wiki/Nag_Hammadi_library)**: In the year of 1945 a collection of early Christian and Gnostic texts were discovered near the Upper Egyptian town of Nag Hammadi
- **Zero hypothesis (H0)**: Nag Hammadi/Gnostic texts and Bible texts are written by the same authors
- **Goal**: use modern NLP techniques to try and prove that H0 is wrong

<br>
<hr>
<br>

## The dataset:
- **The raw texts** are in [data](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data): 
- - [The Bible](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Bible%20-%20King%20James) (King James transl) 
- - [Nag Hammadi library](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Nag%20Hammadi)
- - [Control texts](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Control%20texts) that have nothing to do with Christianity
- **[data_prep.py](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/blob/main/data_prep.py)** module contains the functions needed to parse and return the dataframe
```python
>>> import data_prep as dp
>>> df = dp.return_dataset()
>>> list(df.columns)
#OUTPUT: ['sentence', 'NUM', 'LIBRARY', 'AUTHOR', 'TEXT_NAME', 'TRANSLATION', 'char_count', 'words_count']
>>> df.sample(1).sentence
#OUTPUT: 17050    now the lord hath brought it , and done accord..
```
- **[001_dataset_preview.ipynb](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/blob/main/001_dataset_preview.ipynb)** contains usage example of data_prep functions return_dataset() and print_dataset_stats() functions


<br>
<hr>
<br>

## Word frequency and sentence word lenght comparison:
Notebook: **[001_dataset_preview.ipynb002_word_freq_and_count_comparisons.ipynb](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/blob/main/002_word_freq_and_count_comparisons.ipynb)**

### The metrics:
- **Word Count Diff**: The author uses Long or Short sentences?
Measure how much words an average sentence of the authors has, and look at word count difference between the two authors (for example, author A uses 60 words in a sencence on average, while author B uses only 15 - author B uses significantly shorter sencences than author A)
- **Word Freq Diff**: What words the author uses?
Get a list of every word used by both authors, rate the frequency of usage of every word by both authors and take the average of the differences between every word (for example, author A uses the word "love" frequently, while author B doesn't, but uses the word "pain" very much, while author A doesn't)

### The experiment:
- **Rate the Bible authors**: for every author in the Bible, compare his style with the style of the rest of the Bible. This way we will get the bounds of acceptable deviations
- **Rate the Control authors**: now compare the styles of the two Control authors, which have nothing to do with Christianity, and compare them with the Bible. Make sure they are out of the acceptable deviations
- **Rate the Nag Hammadi texts authors**: compare the Nag Hammadi authors and check whether they are within or out of the acceptable deviations

###  The results:
- **Plot**: Once we perform the experiments and rate every author's Word Freq Diff and Word Count Diff, we can plot the results on the X and Y axis and observe whether there is a visible separation
- **P-value by perm test**: we can estimate the P-value of H0 related to each separate metric and prove whether H0 is wrong

![image](https://user-images.githubusercontent.com/45358654/147566664-2798b083-9a16-4fd4-aef7-a76d6007be45.png)
