import json
import collections
from nltk.corpus import brown

# Read trained model from file
print "Reading model"
emf = open('Emission.json', 'r')
emission = json.load(emf)
trf = open('Transition.json', 'r')
tr = json.load(trf)
transition = {}
for key in tr:
    t_key = key[3: len(key) - 2].split(',')
    transition[(t_key[0][:-1], t_key[1][3:])] = tr[key]

# Set testing sets
sents = brown.tagged_sents(tagset='universal')  # Get corpus
training_sents = []
test_length = int(0.1 * len(sents))
# test_length = 1
testing_sents = []
for sent in sents[len(sents) - test_length: len(sents)]:
    testing_sents.append(sent)
# Collect pairs of tags
pairs = []
for token in transition:
    pairs.append(token)


def viterbi(emissions, transitions, test_sents):
    print "Running Viterbi algorithm"
    vtb = collections.OrderedDict()
    vtbs = []
    from_list = []
    maxp = 0
    temp_key2 = ''
    for sent in test_sents:
        i = 0
        for token in sent:
            if i == 0:
                if token[0] in emissions:
                    for key in emissions[token[0]]:
                        probability = emissions[token[0]][key] * transitions[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START', key)] = probability
                        else:
                            vtb[i][(u'START', key)] = probability
                else:
                    for key in emissions['UNK']:
                        probability = emissions['UNK'][key] * transitions[(u'START', key)]
                        # probability = 1 * transitions[(u'START', key)]
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][(u'START', key)] = probability
                        else:
                            vtb[i][(u'START', key)] = probability
            else:
                if token[0] in emissions:
                    for key in emissions[token[0]]:
                        # maxp = 0
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i - 1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = emissions[token[0]][key] * transitions[key2] * vtb[i - 1][t]
                                    if observe > maxp:
                                        maxp = observe
                                        temp_key2 = key2
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
                        maxp = 0
                        from_list = []
                else:
                    for key in emissions['UNK']:
                        for tk in pairs:
                            if tk[1] == key:
                                temp_from = (tk[0], tk[1])
                                from_list.append(temp_from)
                        for t in vtb[i - 1]:
                            for key2 in from_list:
                                if key2[0] == t[1]:
                                    observe = emissions['UNK'][key] * transitions[key2] * vtb[i - 1][t]
                                    # observe = 1 * transitions[key2] * vtb[i - 1][t]
                                    if observe > maxp:
                                        maxp = observe
                                        temp_key2 = key2
                        if i not in vtb:
                            vtb[i] = {}
                            vtb[i][temp_key2] = maxp
                        else:
                            vtb[i][temp_key2] = maxp
                        maxp = 0
                        from_list = []
            i += 1
            if i == len(sent):
                last = vtb[i - 1]
                for tag in last:
                    probability = last[tag] * transitions[(tag[1], u'END')]
                    if i not in vtb:
                        vtb[i] = {}
                        vtb[i][(tag[1], u'END')] = probability
                    else:
                        vtb[i][(tag[1], u'END')] = probability
        vtbs.append(vtb)
        vtb = collections.OrderedDict()
    return vtbs


def backpoint(test_sents):
    vs = viterbi(emission, transition, test_sents)
    max_prob = 0
    tag = ''
    test_tag = []
    test_tags = []
    print "Choosing tags"
    for v in vs:
        # print len(v)
        print v
        j = next(reversed(v))
        print "len: ", len(v)
        print "j: ", j
        for tag_prob in v[j]:
            if v[j][tag_prob] > max_prob:
                max_prob = v[j][tag_prob]
                tag = tag_prob[0]
        list.insert(test_tag, 0, tag)
        j = j - 1
        print "j after last: ", j
        while j > 0:
            for probs in v[j]:
                if probs[1] == tag:
                    list.insert(test_tag, 0, probs[0])
            tag = test_tag[0]
            j -= 1
        test_tags.append(test_tag)
        test_tag = []
        max_prob = 0
    return test_tags


def calculate_accuracy(test_sents):
    test_tags = backpoint(test_sents)
    origin_tags = []
    total_tag = 0
    right_tag = 0
    for sent in test_sents:
        tags = [t for (_, t) in sent]
        origin_tags.append(tags)
        total_tag += len(tags)
    i = 0
    while i < len(test_tags):
        # print "T: ", test_tags[i]
        # print "O: ", origin_tags[i]
        j = 0
        while j < len(test_tags[i]):
            if test_tags[i][j] == origin_tags[i][j]:
                right_tag += 1
            j += 1
        i += 1
    print "Total words: ", total_tag
    print "Right guessed: ", right_tag
    accuracy = right_tag / (1.0 * total_tag)
    print "Accuracy: ", accuracy


calculate_accuracy(testing_sents)
