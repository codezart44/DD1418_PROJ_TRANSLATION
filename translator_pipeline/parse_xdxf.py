import xml.etree.ElementTree as ET
import pickle as pl
import numpy as np
import re


def in_alphabet(word: str, alphabet: str):
     """@Re: Boolean for whether word is contained within alphabet or not"""
     return all((c.lower() in alphabet for c in word))



def parse_text(text: str) -> list[str]:
    """@Re: List of text or words parsed."""
    if "|" in text:
        text = text.replace("|", "")

    pattern = r"\s*\[.*?\]|\s*\([^)]*\)"
    if "(" in text:
        if text[0] == "(" and text[-1] == ")":
            for sym in ["(", ")", "[UK]", "[US]"]:
                text = text.replace(sym, "")
        else:
            text = re.sub(pattern=pattern, repl="", string=text).strip()

    words = [text.strip()]

    # symbols indicating words should be separated
    delimitors = "[,;/]"    # multiple words present
    words = re.split(pattern=delimitors, string=text)
    return list(filter(None, words))


def parse_swe_word(text: str) -> str:
    """@Re: String of Swedish word cleaned. Empty string if not allowed."""
    if " " in text:
        return ""        # NOTE can only translate one word at the time anyways
    return text.replace("|", "")


def parse_xdxf_to_dict(xml_file: str):
    """### XML Dictionary Exchange Format file to python dictionary
    * #### Example <ar> block structure:

    >>> <ar>
    >>>     <k>absolut</k>
    >>>     <def>
    >>>         <gr>jj</gr>
    >>>         <dtrn>absolute</dtrn>
    >>>         <tr>absol'u:t</tr>
    >>>         <iref href="http://lexin.nada.kth.se/sound/absolut.mp3" />
    >>>         <sr><kref type="syn">bestämt</kref></sr>
    >>>         <sr><kref type="syn">definitiv</kref></sr>
    >>>         <sr><kref type="syn">definitivt</kref></sr>
    >>>         <sr><kref type="syn">exakt</kref></sr>
    >>>         <sr><kref type="syn">fullkomlig</kref></sr>
    >>>         <sr><kref type="syn">fullkomligt</kref></sr>
    >>>         <sr><kref type="syn">helt</kref></sr>
    >>>         <sr><kref type="syn">otvetydig</kref></sr>
    >>>         <sr><kref type="syn">otvivelaktigt</kref></sr>
    >>>         <sr><kref type="syn">ovillkorlig</kref></sr>
    >>>         <sr><kref type="syn">ovillkorligen</kref></sr>
    >>>         <sr><kref type="syn">precis</kref></sr>
    >>>         <sr><kref type="syn">prompt</kref></sr>
    >>>         <sr><kref type="syn">självklart</kref></sr>
    >>>         <sr><kref type="syn">säkert</kref></sr>
    >>>         <sr><kref type="syn">total</kref></sr>
    >>>         <sr><kref type="syn">tveklöst</kref></sr>
    >>>         <sr><kref type="syn">tvärsäkert</kref></sr>
    >>>         <sr><kref type="syn">verkligen</kref></sr>
    >>>         <ex type="exm"><ex_orig>absolut majoritet</ex_orig><ex_transl>absolute majority</ex_transl>      </ex>
    >>>         <def>fullständig, fullkomlig</def>
    >>>     </def>
    >>> </ar>
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()       # xdxf tag

    sv_en_lexicon = {}

    for ar in root.find("lexicon").findall("ar"):

        # Swedish word to translate 
        swedish_word = ar.find('k').text if ar.find('k') is not None else None

        swedish_word = parse_swe_word(text=swedish_word)
        if swedish_word == "":    # if empty string is returned word is not allowed
            continue

        # block containing all definitions etc.
        definition_block = ar.find('def')

        if swedish_word is not None and definition_block is not None:
            # NOTE select all words containing non alpha chars and edit accordingly

            # direct translations of Swedish word
            translations = list()
            for dtrn in definition_block.findall("dtrn"):
                words = parse_text(text=dtrn.text)      # NOTE Potentially multiple alternatives per dtrn (a, an)
                for w in words:
                    translations.append(w.strip())

            # add swe-eng translation to lexicon
            sv_en_lexicon[swedish_word] = np.unique(sv_en_lexicon.get(swedish_word, []) + translations).tolist()
            
            # NOTE Sometimes the synonyms appear before the actual word causing the synonym translations to be added and used instead of the direct translation
            continue

            # Swedish synonyms with same translation(-s)
            swedish_synonyms = [parse_swe_word(text=synonym.find("kref").text) for synonym in definition_block.findall("sr")]
            
            # update lexicon with all swe synonym eng translations NOTE may not want to include, dilutes result
            for synonym in swedish_synonyms:
                if synonym == "":
                    continue
                sv_en_lexicon[synonym] = np.unique(sv_en_lexicon.get(synonym, []) + translations).tolist()

    return sv_en_lexicon



def main():
    xdxf_file = "data/lexicon/sv_en_lexicon.xdxf"
    sv_en_lexicon = parse_xdxf_to_dict(xml_file=xdxf_file)
    print(f"Number of unique swedish words: {len(sv_en_lexicon)}")

    with open(file="data/lexicon/sv_en_lexicon.pkl", mode="wb") as f:
        pl.dump(obj=sv_en_lexicon, file=f)



if __name__=="__main__":
    main()





