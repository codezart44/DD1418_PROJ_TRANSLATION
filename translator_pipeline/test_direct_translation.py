import pickle as pl



def translate(lexicon: dict, sentence: str):
    """@Re: String of words translated from source language to target language"""
    src_words = sentence.lower().strip().split(' ')
    target_words = [lexicon.get(word, [word])[0] for word in src_words]
    translated_sentence = " ".join(target_words)

    return translated_sentence


def printf_translation(src_sentence: str, tgt_sentence: str) -> None:
    """@Re: None"""
    num_underscores = max(len(src_sentence), len(tgt_sentence)) + 5
    print("\n".join([
        "Translated:",
        "-"*num_underscores,
        f"Src: {src_sentence}",
        f"Tgt: {tgt_sentence}",
        "-"*num_underscores,
    ]))


def main():
    with open(file="data/lexicon/sv_en_lexicon.pkl", mode="rb") as f:
        sv_en_lexicon: dict = pl.load(file=f)

    print(sv_en_lexicon["arg"])
    quit()

    sentence1 = "Hej jag heta Oskar"
    sentence2 = "Mitt namn vara Oskar"
    sentence3 = "Jag ska gå till en butik"
    sentence4 = "Hur kan man vara så bra"
    sentence5 = "Vi ska krossa denna uppgift"
    sentence6 = "En hund och en katt satt bredvid ett träd"

    printf_translation(src_sentence=sentence1, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence1))
    printf_translation(src_sentence=sentence2, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence2))
    printf_translation(src_sentence=sentence3, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence3))
    printf_translation(src_sentence=sentence4, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence4))
    printf_translation(src_sentence=sentence5, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence5))
    printf_translation(src_sentence=sentence6, tgt_sentence=translate(lexicon=sv_en_lexicon, sentence=sentence6))




if __name__=="__main__":
    main()
