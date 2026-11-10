# Examples

Real output from CurrencyText, captured from actual runs.

## An invoice total in euros

Command:

```bash
python3 currencytext.py --amount 1234.50
```

Output:

```
1234.50 EUR: one thousand two hundred thirty-four euros and fifty cents
```

## Singular forms in pounds

Command:

```bash
python3 currencytext.py --amount 1 --currency GBP
```

Output:

```
1.00 GBP: one pound
```

## A quotation in dollars

Command:

```bash
python3 currencytext.py --amount 499.99 --currency USD
```

Output:

```
499.99 USD: four hundred ninety-nine dollars and ninety-nine cents
```

## A large amount in rupees

Command:

```bash
python3 currencytext.py --amount 250000 --currency PKR
```

Output:

```
250000.00 PKR: two hundred fifty thousand rupees
```

## The smallest amount: one cent

Command:

```bash
python3 currencytext.py --amount 0.01 --currency EUR
```

Output:

```
0.01 EUR: one cent
```

## Convert euros into rupees at your own rate

Command:

```bash
python3 currencytext.py --amount 100 --currency EUR --convert-to PKR --rate 300
```

Output:

```
100.00 EUR: one hundred euros
= 30000.00 PKR: thirty thousand rupees
```

## Convert pounds into dollars

Command:

```bash
python3 currencytext.py --amount 75.20 --currency GBP --convert-to USD --rate 1.27
```

Output:

```
75.20 GBP: seventy-five pounds and twenty pence
= 95.50 USD: ninety-five dollars and fifty cents
```
