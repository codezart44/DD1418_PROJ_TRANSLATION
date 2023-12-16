

import nltk
import langdetect

one_letter_words = set([
    "I", "a"
])

two_letter_words = set([
    "am", "an", "as", "at", "be", "by", "do", "go", "he", "hi", "if", "in", "is", "it",
    "me", "my", "no", "of", "on", "or", "so", "to", "up", "us", "we", "ad", 
    "bc", "eg", "ex", "ie", "id", "na", 
    "od", "op", "os", "ox", "pi", "pm", "re", "si", 
    "tv", "ut", "io", "ok", "uk"
])


ENGLISH_ALPHABET = set("abcdefghijklmnopqrstuvwxyz" + " ")      # include space


def __clean_word(raw_word: str) -> str:
    """@Re: String of input word only with alphabetical chars."""
    if __contains_eng_letter(raw_word) and (len(raw_word)>2 or raw_word in one_letter_words or raw_word in two_letter_words):
        return "".join(c for c in raw_word if c.lower() in ENGLISH_ALPHABET).strip()
    return ""

def __contains_eng_letter(word: str) -> bool:
    """@Re: Boolean of if word contains any English letters."""
    return any(c.lower() in ENGLISH_ALPHABET for c in word)


def __tokenize_names(words: list[str]) -> list[str]: 
    """@Re: List of input words where capitalized words have been replaced with name token '<Name>'."""
    tokenized_names = words.copy()
    tokenized_names[1:] = list(map(lambda w: "<Name>" if w[0].isupper() and w!="I" else w.lower(), words[1:]))
    return tokenized_names

def __merge_name_tokens(words: list) -> list[str]:
    """@Re: List of input words where contiguous name tokens '<Name>' have been replaced with a single token."""
    merged_names = []
    for w in words:
        if w == "<Name>" and merged_names[-1] == "<Name>":
            continue
        else:
            merged_names.append(w)
    return merged_names


def __clean_line(raw_line: str) -> str: 
    """@Re: String of input line only with alphabetical chars."""
    words = nltk.word_tokenize(text=raw_line)

    clean_words = [__clean_word(w) for w in words]
    clean_words = list(filter(None, clean_words))

    clean_words = __tokenize_names(words=clean_words)
    clean_words = __merge_name_tokens(words=clean_words)

    if any(clean_words): clean_words[0] = clean_words[0].lower()

    return " ".join(clean_words) + "\n" if len(clean_words) > 2 else ""


def clean_file(src_file: str, tgt_file: str) -> None:
    """"""
    assert tgt_file != "UNPC.en-fr.en", "Cannot overwrite large raw file."
    print(f"Cleaning from {src_file} to {tgt_file}.")

    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
            for i, line in enumerate(srcf):
                cleaned_line = __clean_line(raw_line=line)
                tgtf.write(cleaned_line)

                if i%10_000 == 0:
                    print(i)
    
    print(f"Done cleaning. {i} lines cleaned.")


def main():
    directory = "/Users/oskarwallberg/Desktop/en-fr.txt/"

    
    sample_file = "UNPC-en-sample.en"
    clean_sample_file = "UNPC-en-sample-cleaned.en"
    clean_local_file = "data/cleaned/"+clean_sample_file
    clean_file(src_file=directory+sample_file, tgt_file=directory+clean_sample_file)
    clean_file(src_file=directory+sample_file, tgt_file=clean_local_file)


    # NOTE DO NOT UNCOMMENT THIS; WILL OVERWRITE CLEANED FILE - TAKES 46 MIN TO RUN
    # large_file = "UNPC.en-fr.en" NOTE
    # clean_large_file = "UNPC.en-fr-cleaned.en" NOTE
    # clean_file(src_file=directory+large_file, tgt_file=directory+clean_large_file) NOTE



if __name__=="__main__":
    main()


# The Government informed the Special Rapporteur that the Office of the District Public Prosecutor in Novi Sad had opened a case in connection to the &quot; Gradjanski List incident, and, following enquiries by the Novo Sad Police Department, including an interview with the Editor-in-Chief of Gradjanski List &quot; , Mr. Miodrag Nikić, had found that the abovementioned incident satisfied the essential requirements to initiate a prosecution for the criminal offence of insult, under Article 93, para.2, in connection of para.1 of the Criminal Code of the Republic of Serbia.
# the   <Name>   informed the       <Name>       that the <Name> of the           <Name>           in  <Name>  had opened a case in connection to the  quot      <Name>      incident  and  following enquiries by the            <Name>           including an interview with the      <Name>     of       <Name>     quot          <Name>       had found that the abovementioned incident satisfied the essential requirements to initiate a prosecution for the criminal offence of insult  under   <Name>    para    in connection of para   of the     <Name>    of the   <Name> of  <Name>

