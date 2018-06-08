import os, string, math


def processEmail(email):
    remove_punct = dict.fromkeys(map(ord, string.punctuation), ' ')
    with open(email) as f:
        txt = f.read()
        txt = txt.translate(remove_punct)
        return set(txt.split())


def processClass(emailClass):
    path = './train/' + emailClass + '/'
    email = [processEmail(path + fileName) for fileName in os.listdir(path)]
    return email, len(os.listdir(path))


def getWordFrequency(emailClass):
    emailWordSet, emailCount = processClass(emailClass)
    wordict = {}
    for wordSet in emailWordSet:
        for word in wordSet:
            wordict[word] = wordict.setdefault(word, 0) + 1
    return wordict, emailCount


def runTest(email, threshold=0.95):
    wordSet = processEmail(email)
    posteriorProbabilityOfThisEmail = []
    for word in wordSet:
        if word in posteriorProbability:
            probability = posteriorProbability[word]
        else:
            probability = 0.4
        posteriorProbabilityOfThisEmail.append((word, probability))
    posteriorProbabilityOfThisEmail.sort(key=lambda x: abs(x[1] - 0.5), reverse=True)
    frac = 0;
    for i in range(min(len(posteriorProbabilityOfThisEmail) - 1, 50)):
        frac += math.log(1 - posteriorProbabilityOfThisEmail[i][1]) - math.log(posteriorProbabilityOfThisEmail[i][1])
    frac = 1 / (1 + math.exp(frac))
    return 'spam' if frac > threshold else 'ham'


ham, hamEmailCount = getWordFrequency('ham')
spam, spamEmailCount = getWordFrequency('spam')
posteriorProbability = dict.fromkeys((list(ham) + list(spam)), 0)
ps = spamEmailCount / (spamEmailCount + hamEmailCount)
ph = hamEmailCount / (spamEmailCount + hamEmailCount)
for word in posteriorProbability:
    hamPriority = ham[word] / hamEmailCount if word in ham else 0.01
    spamPriority = spam[word] / spamEmailCount if word in spam else 0.01
    posteriorProbability[word] = spamPriority * ps / (hamPriority * ph + spamPriority * ps)

problem1 = dict.fromkeys(list(spam), 0)


def dict2list(dic: dict):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


for word in problem1:
    problem1[word] = hamEmailCount * spam[word] / (spamEmailCount * ham[word]) if word in ham else 0.01
problem1 = sorted(dict2list(problem1), key=lambda x: x[1], reverse=True)
print("most indicative word: ", problem1)

tp, fp, tn, fn = 0, 0, 0, 0
path = './test/spam/'
for fileName in os.listdir(path):
    result = runTest(path + fileName)
    if result == 'spam':
        tp = tp + 1
    else:
        fn = fn + 1
    print("the result of '", fileName, "' : ", result)

path = './test/ham/'
for fileName in os.listdir(path):
    result = runTest(path + fileName)
    if result == 'ham':
        tn = tn + 1
    else:
        fp = fp + 1
    print("the result of '", fileName, "' : ", result)

print("tp=", tp, " fp=", fp, " tn=", tn, " fn=", fn)
