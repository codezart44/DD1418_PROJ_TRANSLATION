
import numpy as np
import pandas as pd
import pickle as pl



class MonogramModel:
    def __init__(self, model_file: str, lexicon: dict) -> None:
        self.lexicon = lexicon

        self.monogram_probs = dict()
        self.monogram_data = list()
        self.__init_model(model_file=model_file)

    def __init_model(self, model_file):
        with open(file=model_file, mode="r", encoding="utf-8") as mf:
            for line in mf:
                word, logprob = line.strip().split(" ")
                self.monogram_probs[word] = logprob
        
    def translate(self, text: str) -> str:
        """@Re: ..."""
        input_words = text.lower().strip().split(" ")
        output_words = []

        # print(self.monogram_data)
        # # for trigram of w1, w2, w3, find all rows (trigrams) with:
        # # w1 & w2 anywhere (even w3) in any order,
        # # For any one of those rows, does w3 or any of its synonyms fit in. Which trigram is most likely? 
        # quit()

        for inp in input_words:
            translations = self.lexicon.get(inp, None)   # [..., ... ,...], [inp]

            if translations is None:
                output_words.append(inp)        # add input word back, not found in lexicon
                continue
            
            # print(translations)
            # print([int(self.monogram_probs.get(trn, 0)) for trn in translations])
            best_trn_idx = np.argmax([self.monogram_probs.get(trn, 0) for trn in translations])
            best_translation = translations[best_trn_idx]
            output_words.append(best_translation)
        
        return " ".join(output_words)




def lexical_translate(lexicon: dict, sentence: str):
    """@Re: String of words translated from source language to target language"""
    src_words = sentence.lower().strip().split(' ')
    target_words = [lexicon.get(word, [word])[0] for word in src_words]
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
        "the normal frequency of inspection authorised by the competent authority shall be one every two years",
        "the manufacturer or the holder of approval is responsible for carrying out a statistical study of the test results in order to meet the specifications laid down for verification of conformity of production in paragraph of this [Name]",
        "the deposit is economic the reserves are assigned the code reserve",
        "included the following issues energy demand modelling and policy analysis applied systems approach in the development of subregional and regional programmers policy and programmes of enhancing energy efficiency in the [Name] countries methodology of forecasting the future energy demand in the [Name] countries etc",
        "these [Name] and the indicators they target are shown in [Name]",
        "the major coal consuming sectors such as the metallurgical chemicalz and building materials industries have grown steadily but coal demand by those sectors has changed little because of the implementation of industrial and product restructuring and technological upgrading",
    ]

    swe_sentences = [
        "normal frekvens för inspektion godkänna av kompetent myndighet ska vara en varje två år",
        "tillverkare eller innehavare av godkännande ansvara för utföra statistisk studie av test resultat för att möta specifikation fastställa för verifiering av överensstämmelse av produktion i stycke av detta [Namn]",
        "insättning vara ekonomisk reserv tilldela kod reserv",
        "inkludera följande frågor energi efterfrågan modellering och policy analys tillämpa system tillvägagångssätt i utveckling av subregional och regional programmera policy och program för förbättra energi effektivitet i [Namn] länder metodik för prognos framtid energi efterfrågan i [Namn] länder etc",
        "dessa [Namn] och indikator de mål visa i [Namn]",
        "stor kol konsumera sektor såsom metallurgisk kemisk och byggnad material industri växa stadigt men kol efterfrågan av de sektor ändra lite på grund av genomförande av industriell och produkt omstrukturering och teknologisk uppgradering",
    ]
    
    # sentence = "värld finnas säkerligen redo och i behov av ett mera effektiv USA"       # surely the world is ready for and urgently in need of a more effective <Name>


    monogram_file = "monogram_model.en"
    monogram_model = MonogramModel(model_file="data/models/"+monogram_file, lexicon=sv_en_lexicon)

    for i, sentence in enumerate(swe_sentences):
        lexical_translation = lexical_translate(lexicon=sv_en_lexicon, sentence=sentence)
        monogram_translation = monogram_model.translate(text=sentence)

        printf_translation(src_sentence=sentence, trn_sentence=eng_sentences[i], tgt_sentence=lexical_translation)
        printf_translation(src_sentence=sentence, trn_sentence=eng_sentences[i], tgt_sentence=monogram_translation)

        inp = input("Next: ")
        if inp == "":
            continue
        else:
            break

    quit()


    
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence2)
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence3)
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence4)
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence5)
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence6)
    lexical_translate(lexicon=sv_en_lexicon, sentence=sentence7)

    # improved monogram translations



    # print
    # printf_translation(src_sentence=sentence1, tgt_sentence=)
    # printf_translation(src_sentence=sentence2, tgt_sentence=)
    # printf_translation(src_sentence=sentence3, tgt_sentence=)
    # printf_translation(src_sentence=sentence4, tgt_sentence=)
    # printf_translation(src_sentence=sentence5, tgt_sentence=)
    # printf_translation(src_sentence=sentence6, tgt_sentence=)
    # printf_translation(src_sentence=sentence7, tgt_sentence=)




if __name__=="__main__":
    main()
