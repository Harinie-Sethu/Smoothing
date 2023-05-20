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
- After that, it will ask for input sentence. YOu can then add your input sentence
- It will output its probability and perplexity
### a) Kneser Ney
- It is run by using the command: 'python3 language_model.py k ./Ulysses-JamesJoyce.txt'
- After the training is done, it will show 'trained'
- After that, it will ask for input sentence. YOu can then add your input sentence
- It will output its probability and perplexity

- The datasets given were also divided into training and testing. The perplexities of the outcome of both the corpus' testing data on both the smoothings have been stored in their respective .txt files.

