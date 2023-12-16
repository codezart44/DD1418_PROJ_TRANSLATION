import numpy as np


from collections import defaultdict


# def read_vocab(src_file: str) -> set():
#     """@Re: Set of model vocabulary."""
#     vocab = list()
#     with open(file=src_file, mode="r", encoding="utf-8") as srcf:
#         for word in srcf:       # each word is a unique word from vocab file
#             vocab.append(word.strip())
#     return vocab


def parse_vocab_to_monogram(src_file: str, tgt_file: str) -> None: 
    """@Re: None"""
    monogram_probs = defaultdict(int)
    
    tot_num_monograms = 0   # NOTE ALL, NOT UNQ

    # w2i = {w: i for i, w in vocab}

    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        for line in srcf:
            for word in line.strip().split(" "):
                # increment count for word in monogram_probs
                tot_num_monograms += 1
                monogram_probs[word] += 1
                if tot_num_monograms%10_000==0:
                    print(tot_num_monograms)
    
    print(f"Done parsing {tot_num_monograms} number of monograms")
    
    with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
        for (word, count) in monogram_probs.items():
            if count > 2:
                tgtf.write(f"{word} {count}\n")  # np.log(count/corpus_length)

    print(f"Done writing {tot_num_monograms} number of monograms")
                





def main():
    sample_monogram_model = "monogram_model.en"


    directory = "/Users/oskarwallberg/Desktop/en-fr.txt/"
    large_file = "UNPC.en-fr-cleaned.en"
    parse_vocab_to_monogram(src_file=directory+large_file, tgt_file="data/models/"+sample_monogram_model)


    # clean_sample_file = "UNPC-en-sample-cleaned.en"
    # parse_vocab_to_monogram(src_file="data/cleaned/"+clean_sample_file, tgt_file="data/models/"+sample_monogram_model)

    



if __name__=="__main__":
    main()