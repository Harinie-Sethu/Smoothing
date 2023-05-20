# Smoothing
Kneser-Ney smoothing and Witten-Bell smoothing on "Pride and Prejudice" and "Ulysses" corpus.

## Tokenizer
- it can be found in 'tokenizer.py'
- The tokenizer has been run on both corpus.
- The cleaned and tokenized corpus can be found as 'Ulysses-JamesJoyce.txt' and 'PrideandPrejudice-JaneAusten.txt'

## Statistical Language Model
### a) Witten Bell
- It is run by using the command: 'python3 language_model.py w ./Ulysses-JamesJoyce.txt'
- After the training is done, it will show 'trained'
- After that, it will ask for input sentence. Enter input sentence after that.
- It will output its probability and perplexity
### a) Kneser Ney
- It is run by using the command: 'python3 language_model.py k ./Ulysses-JamesJoyce.txt'
- After the training is done, it will show 'trained'
- After that, it will ask for input sentence. YOu can then add your input sentence
- It will output its probability and perplexity

- The datasets given were also divided into training and testing. The perplexities of the outcome of both the corpus' testing data on both the smoothings have been stored in their respective .txt files.

## Report and Analysis
## Report

### LM1
- On “Pride and Prejudice” corpus:
- LM 1: tokenization + 4-gram LM + Kneser-Ney smoothing.
- Perplexity of testing data : 104.68868940535138
- Perplexity of training data: 111.73519227944156

### LM2
- On “Pride and Prejudice” corpus:
- LM 2: tokenization + 4-gram LM + Witten-Bell smoothing.
- Perplexity of testing data: 109.59482480400595
- Perplexity of training data: 120.41318512335977

### LM3
- On “Ulysses” corpus:
- LM 3: tokenization + 4-gram LM + Kneser-Ney smoothing.
- Perplexity of testing data: 166.72150714570842
- Perplexity of training data: 213.04528280609296

### LM4
- On "Ulysses" corpus:
- LM 4: tokenization + 4-gram LM + Witten-Bell smoothing.
- Perplexity of testing data: 191.32053634387663  
- Perplexity of training data: 182.32482769093608  

### Tabular Form
| Model | Test_DataSet | Train DataSet  
| :---: | :---:        |  
| LM 1  | 104.68868940535138 | 111.73519227944156 |  
| LM 2  | 109.59482480400595 | 120.41318512335977 |  
| LM 3  | 166.72150714570842 | 213.04528280609296 |  
| LM 4  | 191.32053634387663 | 182.32482769093608 |  

## Metrics
- Perplexity is a metric that measures how well a language model predicts the next word.
- A lower perplexity score indicates a better-performing model. 

## Observation
- LM1 has the lowest perplexity on the "Pride and Prejudice" corpus, followed by LM2. 
- On the other hand, for the "Ulysses" corpus, LM3 has a lower perplexity than LM4.

## Analysis and Discussion
- Both models work differently, and their performance can vary depending on the corpus and the n-gram size used
- Kneser-Ney smoothing is known to perform well on large corpora and with higher order n-grams.
- Witten-Bell smoothing is typically used when the corpus is small and with lower order n-grams.
- Here, the performance of Kneser-Ney is better on both corpora, indicating that it is more suitable for these particular language modeling tasks.

- Compared to the n-gram language models, a neural model would capture more complex patterns and dependencies between tokens, which would lead to lower perplexity scores and better overall performance. 
- Training it would however take more time, data and computational resources. 
