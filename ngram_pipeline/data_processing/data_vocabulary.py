
# import nltk
# # nltk.download("words")



def parse_vocab(src_file: str) -> set:
    """@Re: Set of all unique words (vocabulary)"""
    vocab = set()
    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        for i, line in enumerate(srcf):
            vocab.update(line.strip().split(" "))
    return vocab
        

def write_vocab(vocab: set, tgt_file: str) -> None:
    """@Re: None"""
    with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
        for i, word in enumerate(vocab):
            tgtf.write(word+"\n")


def main():
    quit()  # NOT NEEDED

    directory = "/Users/oskarwallberg/Desktop/en-fr.txt/"
    sample_file = "UNPC-en-sample-cleaned.en"
    sample_vocab_file = "UNPC-en-sample-vocab.en"
    sample_vocab = parse_vocab(src_file=directory+sample_file)

    write_vocab(vocab=sample_vocab, tgt_file= "data/cleaned/"+sample_vocab_file)

    # large_file = "UNPC.en-fr-cleaned.en"
    # large_vocab = read_vocab(src_file=directory+large_file)


    



if __name__=="__main__":
    main()