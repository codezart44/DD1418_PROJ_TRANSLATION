import numpy as np

ONE_IN_SELECTED = 1000

def sample_random_lines(src_file: str, tgt_file: str) -> None:
    """"""
    assert tgt_file != "UNPC.en-fr.en", "Cannot overwrite large raw file."
    print(f"Sampling from {src_file} to {tgt_file}.")

    with open(file=src_file, mode="r", encoding="utf-8") as srcf:
        with open(file=tgt_file, mode="w", encoding="utf-8") as tgtf:
            for i, line in enumerate(srcf):
                if i%ONE_IN_SELECTED==0:
                    tgtf.write(line)
    
    print(f"Done sampling. {i} lines read. {int(i/ONE_IN_SELECTED)} lines sampled.")

def main():
    directory = "/Users/oskarwallberg/Desktop/en-fr.txt/"
    large_file = "UNPC.en-fr.en"
    sample_file = "UNPC-en-sample.en"
    local_file = "data/raw/"+sample_file
    sample_random_lines(src_file=directory+large_file, tgt_file=directory+sample_file)
    sample_random_lines(src_file=directory+large_file, tgt_file=local_file)


if __name__=="__main__":
    main()