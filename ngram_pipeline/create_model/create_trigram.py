import numpy as np


from collections import defaultdict


def corpus_to_trigram(src_file: str, tgt_file: str) -> None: 
    """@Re: None"""
    trigram_probs = defaultdict(int)
    
    tot_trigram_count = 0    # NOT UNIQUE BUT ALL

    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        for line in srcf:
            words = line.strip().split(" ")
            # increment count for word in monogram_probs
            for j in range(2, len(words)):      # skip first (since trigrams)
                trigram = " ".join(words[j-2: j+1])
                trigram_probs[trigram] += 1
                tot_trigram_count += 1
                if tot_trigram_count%10_000==0:
                    print(tot_trigram_count)
    
    with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
        for word, count in trigram_probs.items():
            if count > 4:
                tgtf.write(f"{word} {count}\n")  # np.log(count/corpus_length)
                
    print(f"Done parsing {tot_trigram_count} number of trigrams")


def main():
    sample_trigram_model = "trigram_model.en"

    #NOPE NOTE NOTE
    # directory = "/Users/oskarwallberg/Desktop/en-fr.txt/" NOTE
    # large_file = "UNPC.en-fr-cleaned.en"
    # corpus_to_trigram(src_file=directory+large_file, tgt_file="data/models/"+sample_trigram_model)NOTE

    # clean_sample_file = "UNPC-en-sample-cleaned.en" NOTE
    # sample_trigram_model = "trigram_model.en"
    # corpus_to_trigram(src_file="data/cleaned/"+clean_sample_file, tgt_file="data/models/"+sample_trigram_model)NOTE
    

    

if __name__=="__main__":
    main()


