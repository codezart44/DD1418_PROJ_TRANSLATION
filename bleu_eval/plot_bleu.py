import matplotlib.pyplot as plt
import numpy as np
from nltk.translate.bleu_score import sentence_bleu

swe_sentences = [
    "jag skulle vilja ge dem till belgien",
    "en man ska laga mat i ett hem",
    "det tycka jag vara helt oacceptabelt .",
    "vi ha rösta om ändringsförslag .",
    "härmed förklara jag sammanträde avsluta ",
]

lexicon_trn = [
    "i should want give them another belgien".split(),
    "a husband have to legal food as a home".split(),
    "it imagine I am completely unacceptable .".split(),
    "we be provided with vote about amendment proposal .".split(),
    "hereby declare I conference bring to an end .".split(),
]

n_gram_trn = [
    "i would want give them more belgien".split(),
    "a person shall make food for a house".split(),
    "that think I am completely unacceptable .".split(),
    "we have vote of amendment proposal .".split(),
    "herewith state I meeting complete .".split(),
]

seq2seq = [
    "i should like to give them to belgium .".split(),
    "a picture in related sectors confirms over .".split(),
    "i find that most unacceptable .".split(),
    "we have voted against amendment no .".split(),
    "the debate is adjourned .".split(),
]

references = [
    ["i would like to give them to belgium".split(), "i would like to give it to belgium".split(), "i'd like to give them to belgium".split()],
    ["a man should cook in a home".split(), "a man to cook in a home".split(), "a man is to cook in a home".split()],
    ["i find that completely unacceptable".split(), "i find that totally unacceptable".split(), "i find this totally unacceptable".split()],
    ["we have voted on amendments".split(), "we voted on amendments".split(), "we would have voted on amendments".split()],
    ["i hereby declare the sitting closed".split(), "i hereby declare the meeting closed".split(), "i hereby declare this sitting closed".split()],
]








def plot_bleu_score(bleu_scores):
    """Plot BLEU scores"""
    num_sen = np.arange(len(bleu_scores[0]))  # num sentence
    bleu_lex = bleu_scores[0]
    bleu_ngr = bleu_scores[1]
    bleu_s2s = bleu_scores[2]

    print(np.mean(bleu_lex))
    print(np.mean(bleu_ngr))
    print(np.mean(bleu_s2s))
    
    # Width and offsets for bars
    width = 0.3
    offset = width
    pairs1 = num_sen - offset  # offset for Lexicon
    pairs2 = num_sen  # offset for N-Gram
    pairs3 = num_sen + offset  # offset for Seq2Seq

    # Creating horizontal bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(pairs1, bleu_lex, height=width, color='orange', alpha=0.6, label='Lexicon')
    ax.barh(pairs2, bleu_ngr, height=width, color='yellow', alpha=0.6, label="N-Gram")
    ax.barh(pairs3, bleu_s2s, height=width, color='green', alpha=0.6, label="Seq2Seq")

    # Adding labels and title
    ax.set_xlabel('BLEU Score [0-1] (Bilingual Evaluation Understudy)')
    ax.set_ylabel('Sentence')
    ax.set_title('BLEU Score of Lexical Translation vs N-gram Translation vs Seq2Seq Translation')
    ax.set_yticks(num_sen, [f'Sentence {5-i}' for i in num_sen])  # Labeling pairs
    ax.legend()

    # Show plot
    plt.show()


def main():
    # Example data
    blue_scores = [[],[],[]]
    for i, model_trn in enumerate([lexicon_trn, n_gram_trn, seq2seq]):
        for j in range(len(swe_sentences)):
            swe_sentence = swe_sentences[j]
            trn = model_trn[j]
            refs = references[j]
            blue_scores[i].append(sentence_bleu(references=refs, hypothesis=trn, weights=(1,)))
    
    print(blue_scores)
    plot_bleu_score(bleu_scores=blue_scores)



if __name__=="__main__":
    main()