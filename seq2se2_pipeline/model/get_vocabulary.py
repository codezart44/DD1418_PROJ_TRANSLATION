

def get_vocab(clean_file: str, max_lines:int=20_000) -> int:
    """@Re: int"""
    vocab = set()
    with open(file=clean_file, mode="r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_lines and i == max_lines: break
            vocab.update(line.strip().split(" "))
    return vocab


def main():
    swe_clean_file = "data/cleaned/europarl-v6-cleaned-filtered.sv"
    eng_clean_file = "data/cleaned/europarl-v6-cleaned-filtered.en"
    swe_vocab = get_vocab(clean_file=swe_clean_file, max_lines=10000)
    eng_vocab = get_vocab(clean_file=eng_clean_file, max_lines=10000)

    print(len(eng_vocab))
    print(len(swe_vocab))


if __name__=="__main__":
    main()
    