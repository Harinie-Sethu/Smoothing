import re
from collections import defaultdict

def pre_process(text):
    # Convert to lowercase
    text = text.lower()

    # Replace URLs with <URL>
    text = re.sub(
        r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '<URL>', text)

    # Replace hashtags with <HASHTAG>
    text = re.sub(r'#\w+', '<HASHTAG>', text)

    # Replace mentions with <MENTION>
    text = re.sub(r'@\w+', '<MENTION>', text)

    # Replace with <PERCENT>
    text = re.sub(r'(\d+(\.\d+)?%)', "<PERCENT>", text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # replace numbers with <NUM>
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " <NUM> ", text)
    text = re.sub(r'\b\d+\w*\b', '<NUM>', text)
    text = re.sub(r'\w*\d\w*', '<NUM>', text)

    # contractions
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"won't", "will not", text)

    # hypens and underscore characters at beginning and end of words
    text = re.sub(r'(\b|\-|_)(\w+)\-?(\b|\-|_)', r'\2 ', text)
    text = re.sub(r'(\b|\-|_)(\w+)\-?(\b|\-|_)', r'\2 ', text)

    # Ensure that there's a space between punctuation and words
    text = re.sub(r'(\w)([.,!?])', r'\1 \2', text)
    text = re.sub(r'([.,!?])(\w)', r'\1 \2', text)

    sentences = text

# make dict word freq
# word_freq = defaultdict(int)
# for sent in sentences:
#     # for word in sent:
#     for word in sent.split():
#         word_freq[word] += 1
    sentences = text.split('.')

# make dict word freq
    word_freq = defaultdict(int)
    for sent in sentences:
        sent = re.sub(r'[^\w\s\.\-]+', '', sent)
        sent = re.sub('([;:.,!?()])', r' \1 ', sent)
        words = sent.strip().split()  # split the sentence into a list of words
        for word in words:
            word_freq[word] += 1

    # vocab contains unique tokens with freq > 5
    # set(list of words) = set of words
    # vocab = key-value pairs in the word_freq dict with freq > 5
    vocabulary = set([word for word, count in word_freq.items() if count > 5])

# add the following tokens to vocab: UNK, <s>, </s>
    vocabulary.add('<UNK>')
    vocabulary.add('<s>')
    vocabulary.add('</s>')

# set the words with freq < 5 = UNK
    for i, sent in enumerate(sentences):
        words = sent.split()  # split the sentence into a list of words
        sentences[i] = [word if word_freq[word] > 5 else '<UNK>' for word in words]

    # pad sentence start with <s> and sentence end with </s>
    sentences = [['<s>'] + sent + ['</s>'] for sent in sentences]

    return sentences

# def tokenizee(text):
#     text = cleean(text)
#     sentences = text.split('.')
#     tokenized_sentences = []

#     for sentence in sentences:
#         # tokens = sentence.split()
#         sentence = re.sub(r'[^\w\s\.\-]+', '', sentence)
#         tokens = sentence.strip().split()
#         tokenized_sentences.append(tokens)

#     return tokenized_sentences

#for Ulysses
with open('Ulysses - James Joyce.txt') as file:
    fdata = file.read()

# cleaned_text = cleean(text)
fdata = pre_process(fdata)
# out = " ".join(map(str, tokenized_text))

f = open('Ulysses-JamesJoyce.txt', 'w')
for sentence in fdata:
    f.write(' '.join(sentence) + '\n')



#for pride and prejudice
with open('Pride and Prejudice - Jane Austen.txt') as file:
    fdata = file.read()

# cleaned_text = cleean(text)
fdata = pre_process(fdata)
# out = " ".join(map(str, tokenized_text))

f = open('PrideandPrejudice-JaneAusten.txt', 'w')
for sentence in fdata:
    f.write(' '.join(sentence) + '\n')