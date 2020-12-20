# Part one

[Example](https://regexper.com/#a%28%28aa%7Cbb%29%28ab%7Cba%29%7C%28ab%7Cba%29%28aa%7Cbb%29%29b)

# Part two

[Rules 8 and 11, approximated](https://regexper.com/#%2842%29*%2842%29*%2831%29*)

Rule 11 cannot be expressed as a regular expression.
It is essentially `(42){n}(31){n}`.

This means: Rule 0 becomes `n*(rule 42) + m*(rule 42) + m*(rule 31)`, or "(n+m) times rule 42 followed by m times rule 31, where n > m > 0".

```
while 42 gives a match:
  i++
while 31 gives a match:
  j++
return i > j > 0
```
