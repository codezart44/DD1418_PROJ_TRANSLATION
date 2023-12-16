import numpy as np


from collections import defaultdict


def corpus_to_bigram(src_file: str, tgt_file: str) -> None: 
    """@Re: None"""
    bigram_probs = defaultdict(int)
    
    tot_bigram_count = 0    # NOT UNIQUE BUT ALL

    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        for line in srcf:
            words = line.strip().split(" ")
            # increment count for word in monogram_probs
            for j in range(1, len(words)):      # skip first (since bigrams)
                bigram = " ".join(words[j-1: j+1])
                bigram_probs[bigram] += 1
                tot_bigram_count += 1
                if tot_bigram_count%10_000==0:
                    print(tot_bigram_count)
    
    with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
        for word, count in bigram_probs.items():
            if count > 4:
                tgtf.write(f"{word} {count}\n")  # np.log(count/corpus_length)
                
    print(f"Done parsing {tot_bigram_count} number of bigrams")


def main():
    sample_bigram_model = "bigram_model.en"

    directory = "/Users/oskarwallberg/Desktop/en-fr.txt/"
    large_file = "UNPC.en-fr-cleaned.en"
    corpus_to_bigram(src_file=directory+large_file, tgt_file="data/models/"+sample_bigram_model)

    # clean_sample_file = "UNPC-en-sample-cleaned.en"
    # corpus_to_bigram(src_file="data/cleaned/"+clean_sample_file, tgt_file="data/models/"+sample_bigram_model)

    

if __name__=="__main__":
    main()






# def get_unq_bigrams(src_file: str) -> set():
#     """@Re: Set of uniqie bigrams."""
#     unq_bi = set()
#     with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        # for i, line in enumerate(srcf):
        #     words = line.strip().split(" ")
        #     for j in range(1, len(words)):      # skip first (since bigrams)
        #         bigram = " ".join(words[j-1: j+1])
#                 print(bigram)
#     return unq_bi