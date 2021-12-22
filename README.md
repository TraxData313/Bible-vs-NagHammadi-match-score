# Bible-vs-NagHammadi-match-score
Is Nag Hammadi library part of the Bible? Use NLP techniques to get match score between the texts and try to answer that controversial question.

## Description and goal:
- **Bible**: The early Chirch arranged scripts, letters, ghospels and other texts related to Jesus Christ and created the Bible
- **Gnostic**: Other texts were rejected as faked/heresy and were rejected. A lot of those texts were destroyed. They are also known as Gnostic texts
- **Nag Hammadi**: In the 1945 a collection of early Christian and Gnostic texts were discovered near the Upper Egyptian town of Nag Hammadi
- **Zero hypothesis (H0)**: Nag Hammadi/Gnostic texts and Bible texts are written by the same authors
- **Goal**: use modern NLP methods to try and prove that H0 is wrong


## The dataset:
- The raw texts are in data: the Bible (King James transl), Nag Hammadi librarie, Control texts that have nothing to do with Christianity
- data_prep.py module contains the functions needed to parse and return the dataframe
```python
>>> import data_prep as dp
>>> df = dp.return_dataset()
>>> df.sample(5)
                                                 sentence  NUM LIBRARY  ... TRANSLATION char_count words_count
28399  if they say to you , it is in the sea , then t...  010      NH  ...    Thomas O         70          18
22243    the woman answered and said , i have no husband  042      NT  ...  King James         47          10
20788  and he went out from thence , and came into hi...  040      NT  ...  King James         90          19
19486  hold thy peace at the presence of the lord god...  035      OT  ...  King James        145          32
16615  and thou , even thyself , shalt discontinue fr...  023      OT  ...  King James        231          47
>>> list(df.columns)
['sentence', 'NUM', 'LIBRARY', 'AUTHOR', 'TEXT_NAME', 'TRANSLATION', 'char_count', 'words_count']
```
- 001_dataset_preview.ipynb contains usage example of data_prep functions return_dataset() and print_dataset_stats() functions
