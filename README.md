# Bible vs Nag Hammadi match score
Should the gnostic texts found near Nag Hammadi be a part of the Bible? Use modern NLP techniques try to answer that controversial question.

<hr>
<br>

## Description and goal:
- <b style="font-size:120%">**[The Bible](https://en.wikipedia.org/wiki/Bible)**</b>: The early Church arranged scripts, letters, ghospels and other texts related to the teachings of Jesus Christ, and put together the Bible
- <b style="font-size:120%">**[Gnostic texts](https://en.wikipedia.org/wiki/Gnostic_texts)**</b>: There were other texts that were rejected as herecy, claimed not to be Word of God. They are known as Gnostic texts. Most of those texts were lost or destroyed and only mentions of them or questionable copies survived
- <b style="font-size:120%">**[Nag Hammadi library](https://en.wikipedia.org/wiki/Nag_Hammadi_library)**</b>: That changed in the year of 1945, when a collection of early Christian and authentic Gnostic texts were discovered near the Upper Egyptian town of Nag Hammadi
- <b style="font-size:120%">Zero hypothesis (H0)</b>: The Bible and the rejected Gnostic texts are part of the same teaching
- <b style="font-size:120%">The Goal</b>: Use NLP to define the bounds that separate the Bible from other texts that are clearly not part of it (Control texts), then prove that H0 is wrong by observing whether the Gnostic texts fit inside or outside of those bounds

<br>
<hr>
<br>

## The dataset:
- **The raw texts** are in [data](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data): 
- - [The Bible](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Bible%20-%20King%20James) (King James translation) 
- - [Nag Hammadi gnostic texts](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Nag%20Hammadi)
- - [Control texts](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/tree/main/data/Control%20texts)
- **[data_prep.py](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/blob/main/data_prep.py)** module contains the functions needed to parse and return a dataframe containing each sentence of the texts
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

## H0 rejection by Word Frequency and Count comparison:
Calculations and detains in the Notebook: **[002_word_freq_and_count_comparisons.ipynb](https://github.com/TraxData313/Bible-vs-NagHammadi-match-score/blob/main/002_word_freq_and_count_comparisons.ipynb)**

### The metrics:
- <b style="font-size:120%">Word Count Diff</b>: The author uses Long or Short sentences?
Measure how much words an average sentence of the authors has, and look at word count difference between the two authors (for example, author A uses 60 words in a sencence on average, while author B uses only 15 - author B uses significantly shorter sencences than author A)
- <b style="font-size:120%">Word Freq Diff</b>: What words the author uses?
Get a list of every word used by both authors, rate the frequency of usage of every word by both authors and take the average of the differences between every word (for example, author A uses the word "love" frequently, while author B doesn't, but uses the word "pain" very much, while author A doesn't)

### The experiment:
- <b style="font-size:120%">Rate the Bible authors</b>: for every author in the Bible, compare his style with the style of the rest of the Bible. This way we will get the bounds of acceptable deviations
- <b style="font-size:120%">Rate the Control authors</b>: now compare the styles of the two Control authors, which have nothing to do with Christianity, and compare them with the Bible. Make sure they are out of the acceptable deviations
- <b style="font-size:120%">Rate the Nag Hammadi texts authors</b>: compare the Nag Hammadi authors and check whether they are within or out of the acceptable deviations

###  The results:
- <b style="font-size:120%">Plot</b>: Once we perform the experiments and rate every author's Word Freq Diff and Word Count Diff, we can plot the results on the X and Y axis and observe that there is a visible separation
- <b style="font-size:120%">P-value by perm test</b>: We can estimate the P-value of H0 related to each separate metric and prove that H0 is wrong. The observed P-value is below 0.0% for both metrics, proving that H0 is wrong

![image](https://user-images.githubusercontent.com/45358654/147566664-2798b083-9a16-4fd4-aef7-a76d6007be45.png)
