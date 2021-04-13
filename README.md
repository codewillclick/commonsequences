# commonsequences
Output a list of the N most common K-word sequences in an input text, with count mapping.

## requirements

100 most common three word sequences
map between each sequence and number of times encountered

## usage

Using the class itself looks like this.  Gathering the ordering of the most-frequent sequences is implemented within an `if __name__ == 'main'` block.

```python
import json
import comseq from comseq

com = comseq()
com.eval(count=3, argv=sys.argv)

print(json.dumps(com.table,indent=2))
```

## tests run

```shell
python3 comseq.py test/origin-of-species.txt > test/origin-of-species.out
python3 comseq.py test/quick-test.txt test/quick-test-2.txt > test/quick-tests.out
```

## uncertainties

Intended name of evaluating module is uncertain.  Should it be `solution.py`, or is `comseq.py` accceptable?
