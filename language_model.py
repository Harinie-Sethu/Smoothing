from collections import defaultdict
import re
import random
import math
import sys


def pre_process(text):
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

# sentences = text.split('.')
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
        sentences[i] = [word if word_freq[word]
                        > 5 else '<UNK>' for word in words]

    # pad sentence start with <s> and sentence end with </s>
    sentences = [['<s>'] + sent + ['</s>'] for sent in sentences]

    return sentences


unigram_model = {}
bigram_model = {}
trigram_model = {}
fourgram_model = {}


def n_gram_maker(sentences, n):

    # ngram_dict associates each n-gram with a corresponding value that indicates the number of tokens in the n-gram
    # ngram_dict[1] refers to unigram
    # ngram_dict = {1: unigram, 2: bigram, 3: trigram, 4: fourgram}

    for sent in sentences:
        # sent = ["<s>"] + sent + ["</s>"]

        for i in range(len(sent) - 1):
            # unigram
            token = sent[i]
            unigram_model[token] = unigram_model.get(token, 0) + 1

            # bigram
            if i < len(sent) - 2:
                next_token = sent[i + 1]
                if token in bigram_model:
                    if next_token in bigram_model[token]:
                        bigram_model[token][next_token] += 1
                    else:
                        bigram_model[token][next_token] = 1
                else:
                    bigram_model[token] = {next_token: 1}

            # trigram
            if i < len(sent) - 3:
                next_next_token = sent[i + 2]
                if token in trigram_model:
                    if next_token in trigram_model[token]:
                        if next_next_token in trigram_model[token][next_token]:
                            trigram_model[token][next_token][next_next_token] += 1
                        else:
                            trigram_model[token][next_token][next_next_token] = 1
                    else:
                        trigram_model[token][next_token] = {next_next_token: 1}
                else:
                    trigram_model[token] = {next_token: {next_next_token: 1}}

            # fourgram
            if i < len(sent) - 4:
                next_next_next_token = sent[i + 3]
                if token in fourgram_model:
                    if next_token in fourgram_model[token]:
                        if next_next_token in fourgram_model[token][next_token]:
                            if next_next_next_token in fourgram_model[token][next_token][next_next_token]:
                                fourgram_model[token][next_token][next_next_token][next_next_next_token] += 1
                            else:
                                fourgram_model[token][next_token][next_next_token][next_next_next_token] = 1
                        else:
                            fourgram_model[token][next_token][next_next_token] = {
                                next_next_next_token: 1}
                    else:
                        fourgram_model[token][next_token] = {
                            next_next_token: {next_next_next_token: 1}}
                else:
                    fourgram_model[token] = {next_token: {
                        next_next_token: {next_next_next_token: 1}}}

    return unigram_model, bigram_model, trigram_model, fourgram_model


def wb_smoothing(n, n_gram):
    # if len(n_gram) < n:
    #     return 0
    if n == 1:
        if n_gram[0] in unigram_model:
            return (unigram_model[n_gram[0]] + 1) / (sum(unigram_model.values()) + len(unigram_model))
        else:
            return 1 / len(unigram_model)

    elif n == 2:
        if n_gram[0] in bigram_model and n_gram[1] in bigram_model[n_gram[0]]:
            num = bigram_model[n_gram[0]][n_gram[1]]
            denom = sum(bigram_model[n_gram[0]].values()
                        ) + len(bigram_model[n_gram[0]])
            lambda_ = len(bigram_model[n_gram[0]]) / denom
            return (num + lambda_ * wb_smoothing(1, [n_gram[1]])) / denom
        else:
            return wb_smoothing(1, [n_gram[1]])

    elif n == 3:
        if n_gram[0] in trigram_model and n_gram[1] in trigram_model[n_gram[0]] and n_gram[2] in trigram_model[n_gram[0]][n_gram[1]]:
            num = trigram_model[n_gram[0]][n_gram[1]][n_gram[2]]
            denom = sum(trigram_model[n_gram[0]][n_gram[1]].values(
            )) + len(trigram_model[n_gram[0]][n_gram[1]])
            lambda_ = len(trigram_model[n_gram[0]][n_gram[1]]) / denom
            return (num + lambda_ * wb_smoothing(2, [n_gram[1], n_gram[2]])) / denom
        else:
            return wb_smoothing(2, [n_gram[1], n_gram[2]])

    elif n == 4:
        if n_gram[0] in fourgram_model and n_gram[1] in fourgram_model[n_gram[0]] and n_gram[2] in fourgram_model[n_gram[0]][n_gram[1]] and n_gram[3] in fourgram_model[n_gram[0]][n_gram[1]][n_gram[2]]:
            num = fourgram_model[n_gram[0]][n_gram[1]][n_gram[2]][n_gram[3]]
            denom = sum(fourgram_model[n_gram[0]][n_gram[1]][n_gram[2]].values(
            )) + len(fourgram_model[n_gram[0]][n_gram[1]][n_gram[2]])
            lambda_ = len(fourgram_model[n_gram[0]]
                          [n_gram[1]][n_gram[2]]) / denom
            return (num + lambda_ * wb_smoothing(3, [n_gram[1], n_gram[2], n_gram]))
        else:
            return wb_smoothing(3, [n_gram[1], n_gram[2], n_gram[3]])
    else:
        return ('Enter a lower order n (n<5)\n')


def kn_smoothing(n, n_gram):
    d1 = 0.75
    if len(n_gram) < n:
        return 0
    if n == 1:
        count = unigram_model.get(n_gram[0], 0)
        total_count = sum(unigram_model.values())
        return max(count - d1, 0) / total_count + d1 / len(unigram_model)

    elif n == 2:
        if len(n_gram) == 1:
            return kn_smoothing(1, n_gram)
        else:
            w1 = n_gram[0]
            w2 = n_gram[1]
            count_w1w2 = bigram_model.get(w1, {}).get(w2, 0)
            count_w1 = unigram_model.get(w1, 0)
            if count_w1 == 0:  # Backoff to unigram model
                return kn_smoothing(1, [w1])
            total_count = sum(unigram_model.values())
            lambda_1 = d1 * len(set(bigram_model.keys())) / count_w1
            p_continuation = kn_smoothing(1, [w2])
            return max(count_w1w2 - d1, 0) / count_w1 + lambda_1 * p_continuation
    elif n == 3:
        if len(n_gram) == 1:
            return kn_smoothing(2, n_gram)
        else:
            w1 = n_gram[0]
            w2 = n_gram[1]
            w3 = n_gram[2]
            count_w1w2w3 = trigram_model.get(w1, {}).get(w2, {}).get(w3, 0)
            count_w1w2 = bigram_model.get(w1, {}).get(w2, 0)
            if count_w1w2 == 0:  # Backoff to bigram model
                return kn_smoothing(2, [w2, w3])
            lambda_2 = d1 * len(set(trigram_model.keys())) / count_w1w2
            p_continuation = kn_smoothing(2, [w2, w3])
            return max(count_w1w2w3 - d1, 0) / count_w1w2 + lambda_2 * p_continuation
    elif n == 4:
        if len(n_gram) == 1:
            return kn_smoothing(3, n_gram)
        else:
            w1 = n_gram[0]
            w2 = n_gram[1]
            w3 = n_gram[2]
            w4 = n_gram[3]
            count_w1w2w3w4 = fourgram_model.get(
                w1, {}).get(w2, {}).get(w3, {}).get(w4, 0)
            count_w1w2w3 = trigram_model.get(w1, {}).get(w2, {}).get(w3, 0)
            if count_w1w2w3 == 0:  # Backoff to trigram model
                return kn_smoothing(3, [w2, w3, w4])
            lambda_3 = d1 * len(set(fourgram_model.keys())) / count_w1w2w3
            p_continuation = kn_smoothing(3, [w2, w3, w4])
            return max(count_w1w2w3w4 - d1, 0) / count_w1w2w3 + lambda_3 * p_continuation
    else:
        return ('Enter a lower order n (n<5)\n')


def perp(test_set, method, n):

    if method == 'wb':
        # probability = [wb_smoothing(n, test_set[i-2:i+1])
        #                for i in range(2, len(test_set))]
        probability = [wb_smoothing(n, test_set[i-n:i])
                       for i in range(n, len(test_set))]
    elif method == 'kn':
        # probability = [kn_smoothing(n, test_set[i-2:i+1])
        #                for i in range(2, len(test_set))]
        probability = [kn_smoothing(n, test_set[i-n:i])
                       for i in range(n, len(test_set))]

# Calculate joint probability of test set
    joint_prob = 1
    for prob in probability:
        joint_prob *= prob

    epsilon = 1e-10  # small constant to add to avoid taking logarithm of 0

    joint_prob = max(joint_prob, epsilon)
    # entropy = -1/len(test_set) * math.log2(joint_prob)

# Calculate entropy of test set
    entropy = -1/len(test_set) * math.log2(joint_prob)

# Calculate perplexity score
    perplexity = 2**entropy
    return perplexity


smoothing_type = sys.argv[1]
corpus_path = sys.argv[2]

# processing dataset
with open(corpus_path) as file:
    fdata = file.read()

fdata = pre_process(fdata)
n_gram_maker(fdata, 4)
print("Trained\n")

# taking sentence input
input_sent = input("input sentence: \n")
input_sent = input_sent.lower()


sen_temp = []
for i in input_sent:
    i = re.sub(r'[^\w\s\.\-]+', '', i)
    i = re.sub('([;:.,!?()])', r' \1 ', i)
    if i in unigram_model:
        sen_temp.append(i)
    else:
        sen_temp.append("<UNK>")
input_sent = sen_temp
# input_sent = pre_process(input_sent)
# input_sent = tuple(input_sent)
if smoothing_type == 'k':
    # use Kneser-Ney smoothing
    probability = kn_smoothing(4, input_sent)
    perplex = perp(input_sent, 'kn', 4)
    print('probability: ', probability)
    print('\n')
    print('perplexity: ', perplex)
    print('\n')
elif smoothing_type == 'w':
    # use Witten-Bell smoothing
    probability = wb_smoothing(4, input_sent)
    perplex = perp(input_sent, 'wb', 4)
    print('probability: ', probability)
    print('\n')
    print('perplexity: ', perplex)
    print('\n')

else:
    print("Unknown smoothing type. Please use k for Kneser-Ney or w for Witten-Bell.")
    sys.exit(1)
