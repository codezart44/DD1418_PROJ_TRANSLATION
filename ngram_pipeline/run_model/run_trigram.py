
import numpy as np
import pandas as pd
import pickle as pl
from collections import defaultdict

from nltk.translate.bleu_score import sentence_bleu


# to create a default dict of a default dict of a dict of probs!
def default_dict():
    return defaultdict(dict)



class TrigramModel:
    def __init__(self, trigram_file: str, bigram_file: str, monogram_file: str, lexicon: dict) -> None:
        self.lexicon = lexicon

        self.monogram_probs = dict()
        self.bigram_probs = defaultdict(dict)
        self.trigram_probs = defaultdict(default_dict)
        self.__init_model(trigram_file=trigram_file, bigram_file=bigram_file, monogram_file=monogram_file)

    
    def __init_model(self, trigram_file: str, bigram_file: str, monogram_file: str):
        with open(file=trigram_file, mode="r", encoding="utf-8") as mf:
            for line in mf:
                word1, word2, word3, logprob = line.strip().split(" ")
                self.trigram_probs[word1][word2][word3] = logprob
        with open(file=bigram_file, mode="r", encoding="utf-8") as mf:
            for line in mf:
                word1, word2, logprob = line.strip().split(" ")
                self.bigram_probs[word1][word2] = logprob
        with open(file=monogram_file, mode="r", encoding="utf-8") as mf:
            for line in mf:
                word, logprob = line.strip().split(" ")
                self.monogram_probs[word] = logprob
    

    def use_monogram(self, swe_word: str) -> str:
        """@Re: String of best monogram translation, Or input word if none found"""
        translations: list[str] = self.lexicon.get(swe_word, None)

        if translations is None or len(translations)==0:
            return swe_word         # add input word back, not found in lexicon

        best_trn_idx = np.argmax([int(self.monogram_probs.get(trn.lower(), 0)) for trn in translations])
        best_translation = translations[best_trn_idx]

        return best_translation


    def use_bigram(self, prev_trn: str, swe_word: str) -> str:
        """@Re: String of best trigram translation, or input word if none found"""
        translations: list[str] = self.lexicon.get(swe_word, None)   # [..., ... ,...], [inp]

        if translations is None or len(translations)==0:
            return swe_word         # return input word if not found

        trn_probs = [int(self.bigram_probs.get(prev_trn.lower(), {}).get(trn.lower(), 0)) for trn in translations]  # NOTE actually counts atm
        
        if sum(trn_probs) == 0: # NOTE NOTE NOTE change later XXX  XXX
            best_translation = self.use_monogram(swe_word=swe_word)
            return best_translation
        
        best_trn_idx = np.argmax(trn_probs)
        best_translation = translations[best_trn_idx]

        return best_translation
    

    def use_trigram(self, prev2_trn: str, prev1_trn: str, swe_word: str) -> str:
        """@Re: String of best bigram translation, or input word if none found"""
        translations: list[str] = self.lexicon.get(swe_word, None)

        if translations is None or len(translations)==0:
            return swe_word         # return input word if not found

        trn_probs = [int(self.trigram_probs.get(prev2_trn.lower(), {}).get(prev1_trn.lower(), {}).get(trn.lower(), 0)) for trn in translations]  # NOTE actually counts atm
        
        if sum(trn_probs) == 0: 
            best_translation = self.use_bigram(prev_trn=prev1_trn, swe_word=swe_word)
            return best_translation
        
        best_trn_idx = np.argmax(trn_probs)
        best_translation = translations[best_trn_idx]

        return best_translation


    def translate(self, text: str) -> str:
        """@Re: String of best trigram translation, or input word if none found"""

        input_words = ["<SOS>", "<SOS>"] + text.lower().strip().split(" ")
        output_words = ["<SOS>", "<SOS>"]

        for i in range(2, len(input_words)):
            prev2_trn = output_words[i-2]
            prev1_trn = output_words[i-1]
            swe_word = input_words[i]
            trn = self.use_trigram(prev2_trn=prev2_trn, prev1_trn=prev1_trn, swe_word=swe_word)
            output_words.append(trn)
        
        return " ".join(output_words[2:])




def lexical_translate(lexicon: dict, sentence: str):
    """@Re: String of words translated from source language to target language"""
    src_words = sentence.lower().strip().split(' ')
    target_words = []
    for word in src_words:
        translations = lexicon.get(word, [word])
        if len(translations) == 0: 
            target_words.append(word)
        else:
            target_words.append(translations[0])
    translated_sentence = " ".join(target_words)
    return translated_sentence






def printf_translation(src_sentence: str, trn_sentence: str, tgt_sentence: str) -> None:
    """@Re: None"""
    num_underscores = max(len(src_sentence), len(trn_sentence), len(tgt_sentence)) + 5
    print("\n".join([
        "Translated:",
        "-"*num_underscores,
        f"Src: {src_sentence}",
        f"Trn: {trn_sentence}",
        f"Tgt: {tgt_sentence}",
        "-"*num_underscores,
    ]))


def main():
    with open(file="data/lexicon/sv_en_lexicon.pkl", mode="rb") as f:
        sv_en_lexicon: dict = pl.load(file=f)
    
    # original language
    eng_sentences = [
        "i find that completely unacceptable",
        "i should like to give them to belgium.",
        "a man should cook in a home",
        # "the normal frequency of inspection authorised by the competent authority shall be one every two years",
        # "the manufacturer or the holder of approval is responsible for carrying out a statistical study of the test results in order to meet the specifications laid down for verification of conformity of production in paragraph of this [Name]",
        # "the deposit is economic the reserves are assigned the code reserve",
        # "included the following issues energy demand modelling and policy analysis applied systems approach in the development of subregional and regional programmers policy and programmes of enhancing energy efficiency in the [Name] countries methodology of forecasting the future energy demand in the [Name] countries etc",
        # "these [Name] and the indicators they target are shown in [Name]",
        # "the major coal consuming sectors such as the metallurgical chemicalz and building materials industries have grown steadily but coal demand by those sectors has changed little because of the implementation of industrial and product restructuring and technological upgrading",
    ]

    swe_sentences = [
        "det tycka jag vara helt oacceptabelt .",
        "jag skulle vilja ge dem till belgien",
        "en man ska laga mat i ett hem",
        # "procent av dessa var barn under fem år .",
        # "vi ha rösta om ändringsförslag .",
        # "härmed förklara jag sammanträde avsluta ."

        # "normal frekvens för inspektion godkänna av kompetent myndighet ska vara en varje två år",
        # "tillverkare eller innehavare av godkännande ansvara för utföra statistisk studie av test resultat för att möta specifikation fastställa för verifiering av överensstämmelse av produktion i stycke av detta [Namn]",
        # "insättning vara ekonomisk reserv tilldela kod reserv",
        # "inkludera följande frågor energi efterfrågan modellering och policy analys tillämpa system tillvägagångssätt i utveckling av subregional och regional programmera policy och program för förbättra energi effektivitet i [Namn] länder metodik för prognos framtid energi efterfrågan i [Namn] länder etc",
        # "dessa [Namn] och indikator dem mål visa i [Namn]",
        # "stor kol konsumera sektor såsom metallurgisk kemisk och byggnad material industri växa stadigt men kol efterfrågan av de sektor ändra lite på grund av genomförande av industriell och produkt omstrukturering och teknologisk uppgradering",
    ]
    
    # swe_sentences2 = [
    #     "med center av tyngdkraft direkt ovanför punkt av genomslag",
    #     "en hund kan springa i en park kuk",
    #     "en kock ska laga mat i ett kök",
    #     "jag vara hungrig kan du laga mat till mig",
    #     "våran tupp vara bäst",
    #     "min häst vara snabbare än din"
    # ]
    # eng_sentences2 = [
    #     "with the centre of gravity directly above the point of impact",
    #     "","","","","",""
    #                   ]
    
    # sentence = "värld finnas säkerligen redo och i behov av ett mera effektiv USA"       # surely the world is ready for and urgently in need of a more effective <Name>


    trigram_file = "trigram_model.en"
    bigram_file = "bigram_model.en"
    monogram_file = "monogram_model.en"
    trigram_model = TrigramModel(
        trigram_file="data/models/"+trigram_file, 
        bigram_file="data/models/"+bigram_file,
        monogram_file="data/models/"+monogram_file, 
        lexicon=sv_en_lexicon
        )

    for i, sentence in enumerate(swe_sentences):
        lexical_translation = lexical_translate(lexicon=sv_en_lexicon, sentence=sentence)
        trigram_translation = trigram_model.translate(text=sentence)

        printf_translation(src_sentence=sentence, trn_sentence=lexical_translation, tgt_sentence=eng_sentences[i])
        printf_translation(src_sentence=sentence, trn_sentence=trigram_translation, tgt_sentence=eng_sentences[i])

        inp = input("Next: ")
        if inp == "":
            continue
        else:
            break






if __name__=="__main__":
    main()
