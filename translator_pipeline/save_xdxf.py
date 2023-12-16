import requests
# import pickle as pl

def download_file(url: str, filename: str) -> None:
    """@Re: None"""
    response = requests.get(url=url)

    if response.ok:         # same as status code 200
        with open(file=filename, mode="wb") as f:
            f.write(response.content)
        print(f"Downloaded file saved as {filename}")
    else:
        print(f"Failed to retrieve file. Status code {response.status_code}")


url = "https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf"
filename = "sv_en_lexicon.xdxf"        # .xdxf - XML Dictionary Exchange Format
download_file(url=url, filename="data/lexicon/"+filename)

