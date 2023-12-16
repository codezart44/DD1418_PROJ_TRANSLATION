from nltk.translate.bleu_score import sentence_bleu


hypothesis1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
    'ensures', 'that', 'the', 'military', 'always',
    'obeys', 'the', 'commands', 'of', 'the', 'party']

hypothesis2 = ['It', 'is', 'to', 'insure', 'the', 'troops',
    'forever', 'hearing', 'the', 'activity', 'guidebook',
    'that', 'party', 'direct']

reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
    'ensures', 'that', 'the', 'military', 'will', 'forever',
    'heed', 'Party', 'commands']

reference2 = ['It', 'is', 'the', 'guiding', 'principle', 'which',
    'guarantees', 'the', 'military', 'forces', 'always',
    'being', 'under', 'the', 'command', 'of', 'the',
    'Party']

reference3 = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
    'army', 'always', 'to', 'heed', 'the', 'directions',
    'of', 'the', 'party']

# print(len(hypothesis1))
# print(len(hypothesis1))
# print(len(hypothesis1))

hypothesis3 = "Hey my name is Bill".split(" ")

bleu = sentence_bleu([reference1, reference2, reference3], hypothesis3, weights=(1, )) # doctest: +ELLIPSIS
print(bleu)