# CurrencyText

A tiny, dependency-free command line tool that writes money amounts in
words - the way invoices, quotations, cheques and payment records need
them - and can also convert an amount into a second currency with a rate
you supply.

```
1234.50 EUR: one thousand two hundred thirty-four euros and fifty cents
```

## Why

Amounts in figures are easy to mistype and easy to alter. That is why
invoices, quotations, contracts and cheques also carry the amount in
words: the words are the cross-check. Writing them by hand is slow and
error prone, especially for long numbers and second currencies.
CurrencyText produces the wording in one command, correctly spelled,
with the right singular and plural forms, ready to paste into a document.

It is useful for:

- Invoices and quotations where the total must appear in words
- Cheque and payment-order wording
- Contracts and agreements that state amounts both ways
- Bookkeeping notes and payment records
- Quick conversions for a client quote in another currency, with the
  converted total also written out in words

## Features

- Zero dependencies - pure Python 3 standard library
- Currencies: EUR, GBP, USD, PKR
- Handles 0 to 999,999,999 plus cents, pence or paisa
- Correct singular forms: one euro, one pound, one penny, one rupee
- Optional conversion with your own rate (no internet, no API keys,
  no stale exchange rates - the rate you type is the rate it uses)
- Converted amount printed in figures and in words

## Install

No installation and no dependencies. Clone the repo and run it with
Python 3:

```bash
git clone https://github.com/ahsanhani/currencytext.git
cd currencytext
python3 currencytext.py --help
```

## Usage

```bash
# Basic: an invoice total in euros, written out
python3 currencytext.py --amount 1234.50

# Singular forms in pounds
python3 currencytext.py --amount 1 --currency GBP

# A quotation in dollars
python3 currencytext.py --amount 499.99 --currency USD

# Convert a euro price into rupees at your own rate, both in words
python3 currencytext.py --amount 100 --currency EUR --convert-to PKR --rate 300
```

See [examples.md](examples.md) for full sample runs with real output.

## Roadmap

- More currencies (AED, INR, TRY and others)
- Urdu wording output for PKR amounts
- A "cheque mode" that capitalises the wording and fills the line
- Read the amount from stdin for use in scripts

## Contributing

Issues and pull requests are welcome. New currency names and subunit
rules are a single entry in the CURRENCIES table in currencytext.py -
if your currency is missing, add it and open a pull request.

## License

MIT - see [LICENSE](LICENSE).
