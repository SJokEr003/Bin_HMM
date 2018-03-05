import nltk
from nltk.corpus import brown

# Pre-processing training sets
sents = brown.tagged_sents(tagset = 'universal')  # Get training set
train_length = 2  # Define size of training set

start = (u'<s>', u'START')
end = (u'</s>', u'END')
new_sents = []

# Add start and end tag
for sent in sents[0: train_length]:
    list.insert(sent, 0, start)
    list.append(sent, end)
    new_sents.append(sent)

"""
Calculate emission
1. Get frequency for each word
2. Get frequency of each word being tagged as XX
3. Calculate emission
"""


def word_freq():
    word_frequencies = {}
    for sent in new_sents[0: train_length]:
        words = [w for (w, _) in sent]
        tags = [t for (_, t) in sent]
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] + 1
            else:
                word_frequencies[word] = 1
    return word_frequencies


def tagged_freq():
    tag_frequencies = {}
    for sent in new_sents[0: train_length]:
        for token in sent:
            if token[0] not in tag_frequencies:
                tag_frequencies[token[0]] = {}
                tag_frequencies[token[0]][token[1]] = 1
            else:
                if token[1] in tag_frequencies[token[0]]:
                    tag_frequencies[token[0]][token[1]] += 1
                else:
                    tag_frequencies[token[0]][token[1]] = 1
    return tag_frequencies


def emission_probability():
    ep = {}
    tf = tagged_freq()
    wf = word_freq()
    for sent in new_sents[0:train_length]:
        for token in sent:
            if token[0] not in ep:
                ep[token[0]] = {}
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
            else:
                ep[token[0]][token[1]] = tf[token[0]][token[1]] / (1.0 * wf[token[0]])
    return ep


"""
Calculate transition
1. Get tag frequencies
2. Get tag pairs
3. Calculate frequencies of pairs
4. Calculate transition
"""


def tags_freq():
    tags_frequencies = {}
    for sent in new_sents[0: train_length]:
        tags = [t for (_, t) in sent]
        for tag in tags:
            if tag in tags_frequencies:
                tags_frequencies[tag] += 1
            else:
                tags_frequencies[tag] = 1
    return tags_frequencies


def tag_pair():
    tag_pairs = []
    for sent in new_sents[0: train_length]:
        tags = [t for (_, t) in sent]
        pairs = list(nltk.bigrams(tags))
        tag_pairs.extend(pairs)
    return tag_pairs


def pair_freq():
    tp = tag_pair()
    pf = {}
    for token in tp:
        if token[0] not in pf:
            pf[token[0]] = {}
            pf[token[0]][token[1]] = 1
        else:
            if token[1] in pf[token[0]]:
                pf[token[0]][token[1]] += 1
            else:
                pf[token[0]][token[1]] = 1
    return pf


def transition_probability():
    trans_pro = {}
    tag_p = tag_pair()
    tag_freq = tags_freq()
    pairs_freq = pair_freq()
    print pairs_freq
    # for sent in new_sents[0:train_length]:
    for p in tag_p:
        if p not in trans_pro:
            trans_pro[p] = pairs_freq[p[0]][p[1]] / (1.0 * tag_freq[p[0]])
    print trans_pro
    return trans_pro


transition_probability()
