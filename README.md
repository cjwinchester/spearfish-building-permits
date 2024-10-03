# Spearfish building permits
Archiving data extracted from monthly building permit summaries in Spearfish, South Dakota, since January 2013.

Original PDFs [downloaded](download.py) from [the city website](https://www.cityofspearfish.com/Archive.aspx?AMID=37) are stored in [the `pdfs` directory](pdfs). CSV files with data extracted from the PDFs live in [the `data` directory](data). Files are slugged `YYYY-MM` based on the month the report came out.

The [`combine.py`](combine.py) script processes the CSV files into a combined file, [`spearfish-building-permits.csv`](spearfish-building-permits.csv). Burn permits, sign permits, etc. [are excluded](const.py#L15) at this step.
