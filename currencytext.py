#!/usr/bin/env python3
"""CurrencyText - write money amounts in words, the way invoices and cheques need them.

A tiny, dependency-free Python 3 tool. Give it an amount and a currency and
it prints the amount in words, for example:

    1234.50 EUR -> one thousand two hundred thirty-four euros and fifty cents

Optionally it also converts the amount into a second currency using a rate
you supply, and writes the converted amount in words too.

Usage:
    python3 currencytext.py --amount 1234.50
    python3 currencytext.py --amount 1 --currency GBP
    python3 currencytext.py --amount 100 --currency EUR --convert-to PKR --rate 300
"""

import argparse
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]

# code -> (singular, plural, subunit singular, subunit plural)
CURRENCIES = {
    "EUR": ("euro", "euros", "cent", "cents"),
    "GBP": ("pound", "pounds", "penny", "pence"),
    "USD": ("dollar", "dollars", "cent", "cents"),
    "PKR": ("rupee", "rupees", "paisa", "paisa"),
}

MAX_WHOLE = 999_999_999


def under_thousand(n):
    """Words for 0 <= n < 1000 (American style, no internal 'and')."""
    parts = []
    hundreds, rest = divmod(n, 100)
    if hundreds:
        parts.append(ONES[hundreds] + " hundred")
    if rest >= 20:
        tens, ones = divmod(rest, 10)
        word = TENS[tens]
        if ones:
            word += "-" + ONES[ones]
        parts.append(word)
    elif rest > 0:
        parts.append(ONES[rest])
    return " ".join(parts)


def number_words(n):
    """Words for a whole number from 0 to 999,999,999."""
    if n == 0:
        return "zero"
    parts = []
    millions, rest = divmod(n, 1_000_000)
    thousands, rest = divmod(rest, 1_000)
    if millions:
        parts.append(under_thousand(millions) + " million")
    if thousands:
        parts.append(under_thousand(thousands) + " thousand")
    if rest:
        parts.append(under_thousand(rest))
    return " ".join(parts)


def split_amount(amount):
    """Split a Decimal amount into (whole units, hundredths), rounding half up."""
    total_hundredths = int((amount * 100).quantize(Decimal("1"),
                                                    rounding=ROUND_HALF_UP))
    return divmod(total_hundredths, 100)


def amount_in_words(amount, code):
    """Full wording for an amount, e.g. 'one pound and one penny'."""
    singular, plural, sub_singular, sub_plural = CURRENCIES[code]
    whole, hundredths = split_amount(amount)
    if whole == 0 and hundredths == 0:
        return "zero " + plural
    parts = []
    if whole:
        parts.append(number_words(whole) + " " + (singular if whole == 1
                                                  else plural))
    if hundredths:
        parts.append(number_words(hundredths) + " "
                     + (sub_singular if hundredths == 1 else sub_plural))
    return " and ".join(parts)


def parse_decimal(text, label):
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        raise SystemExit("error: {} must be a number, got {!r}".format(label,
                                                                       text))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write a money amount in words, with optional conversion.")
    parser.add_argument("--amount", required=True,
                        help="Amount, e.g. 1234.50")
    parser.add_argument("--currency", default="EUR",
                        choices=sorted(CURRENCIES.keys()),
                        help="Currency of the amount (default: EUR)")
    parser.add_argument("--convert-to", default=None,
                        choices=sorted(CURRENCIES.keys()),
                        help="Optional second currency to convert into")
    parser.add_argument("--rate", default=None,
                        help="Units of the target currency per 1 unit of the "
                             "source (required with --convert-to)")
    args = parser.parse_args(argv)

    if args.convert_to and args.rate is None:
        parser.error("--rate is required when --convert-to is used")
    if args.rate is not None and not args.convert_to:
        parser.error("--rate only makes sense together with --convert-to")

    amount = parse_decimal(args.amount, "--amount")
    if amount < 0:
        parser.error("--amount must not be negative")
    whole, _ = split_amount(amount)
    if whole > MAX_WHOLE:
        parser.error("--amount is too large; maximum is 999,999,999.99")

    print("{:.2f} {}: {}".format(amount, args.currency,
                                 amount_in_words(amount, args.currency)))

    if args.convert_to:
        rate = parse_decimal(args.rate, "--rate")
        if rate <= 0:
            parser.error("--rate must be greater than zero")
        converted = (amount * rate).quantize(Decimal("0.01"),
                                              rounding=ROUND_HALF_UP)
        conv_whole, _ = split_amount(converted)
        if conv_whole > MAX_WHOLE:
            parser.error("converted amount is too large to write in words; "
                         "maximum is 999,999,999.99")
        print("= {:.2f} {}: {}".format(converted, args.convert_to,
                                       amount_in_words(converted,
                                                       args.convert_to)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
