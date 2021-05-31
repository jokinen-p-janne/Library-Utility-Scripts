# Book Loan Counter

Reads in a csv file of all the books we have, and a file of all the loan transactions. Outputs a csv file of all the bots with their loan amounts and the latest date for a loan.

## Why?

The system we have is unreliable when it comes to loan amounts. There is no way to output loans at a book level. Instead the loan amounts are kept at a book copy level. There is no way to output this information via the reporting tools and counting them by hand is too time consuming.

## How to use

We need to generate two csv files from the system: A list of all the books and a list of all the loan transactions

### List of books

    "Raportit" => "Kokoelmatilasto"

Choose the following columns:

- Hyllypaikka
- Sijainti
- Osasto
- Julkaisuvuosi
- Kieli
- Aineistolaji
- Julkaisutyyppi
- ISBN/ISSN
- Nimeke
- Tekijä
- Signum

Choose the appropiate library and unit

Do the search and save to file

Manually add the headers because the system is shit and wont add them itself.

Name the book file "kaikki_nimekkeet.csv" and the loans file "kaikki_lainat.csv". Place both in the data dir.

Run the script

    python3 app.py

Import the output.csv into spreadsheet software of your choosing.

Take a shot.

Lament how shit the system is for the 30th time that day.