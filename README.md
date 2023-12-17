
## Förbättrad Direktöversättning
___
Detta är en skoluppgift av:
- Oskar Wallberg oskarew@kth.ug.se
- Alexander Karolin akarolin@kth.ug.se

Instruktioner för att köra programmet:


### Länkar till data
___
* Exakt länk till lexikon
https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf

* OPUS data för N-gram modeller - Ladda ned fr-en (ca 4 GB)
https://opus.nlpl.eu/NLLB-v1.php  

* OPUS data sv-en till Seq2Seq - Ladda ned sv-en (ca 200 MB)
https://opus.nlpl.eu/Europarl.php 


### Sätta upp lexikal direktöversättning
___
Sätta upp lexikon
* translator_pipeline/
    - parse_xdxf.py                 # 2: för att rensa och städa lexikon för senare översättningar
    - save_xdxf.py                  # 1: för att ladda ned och spara lexikon fil
    - test_direct_translation.py    # 3: testkör lexikal översättning


### Sätta upp n-gram modell
___
* ngram_pipeline/
    * create_model/
        - create_bigram.py      # 3: compile bigram frequencies (approx 5 min)
        - create_monogram.py    # 2: compile monogram frequencies (approx 10 min)
        - create_triram.py      # 4: compile trigram frequencies (approx 20-40 min)
    * data_processing/
        - data_cleaning.py      # 1: clean n-gram data
        - data_sampling.py      # NOTE: to create sample data (not up to date)
    * run_model/
        - run_bigram.py         # -//-
        - run_monogram.py       # -//-
        - run_trigram.py        # 5: run trigram model (requires both mono-, bi- and tri-gram to be compiled)


### Sätta upp seq2seq modell
___
* seq2seq_pipeline/
    * data_processing/
        - data_cleaning.ipynb           # 1: clean and process data, set filters to select sentences of certain length
    * model/
        - encoder_decoder.py            # NOTE: contains code for encoder and decoder classes
        - get_vocabulary.py             # NOTE: contains code to get vocab from respective eng / swe corpus
        - seq2seq_training.ipynb        # 2: run and train model. Takes approx 30 min (7 epochs tot)
