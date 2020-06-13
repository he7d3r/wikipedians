# wikipedians
wikipedians helps us explore patterns in wikipedians' edits.

# Examples
## Extract revision metadata from dump
```
./wikipedians/utilities/extract_rev_data.py \
	data/ptwiki-20200501-stub-meta-history*.xml.gz --debug --verbose > \
		data/edits-1.json
```
Example output:
```
{"t": 1577700000, "u": "Alice", "n": 0}
{"t": 1577800000, "u": "Alice", "n": 0}
{"t": 1577830000, "u": "Carol", "n": 0}
{"t": 1577860000, "u": "Alice", "n": 0}
{"t": 1577890000, "u": "Alice", "n": 1}
{"t": 1577890000, "u": "Alice", "n": 2}
{"t": 1577900000, "u": "Alice", "n": 0}
{"t": 1578000000, "u": "Bob", "n": 0}
{"t": 1578100000, "u": "Alice", "n": 0}
{"t": 1578200000, "u": "Bob", "n": 4}
```


## Aggregate user edits
Get total number of edits by month, user and namespace, for users with at least
5 edits:
```
cat data/edits-1.json | ./wikipedians/utilities/aggregate.py --min-edits=2 \
	--verbose > data/edits-2.csv
```
Example output:
```
timestamp,user,namespace,edits
2019-12-30,Alice,0,1
2019-12-31,Alice,0,1
2020-01-01,Alice,0,2
2020-01-01,Alice,1,1
2020-01-01,Alice,2,1
2020-01-02,Bob,0,1
2020-01-04,Alice,0,1
2020-01-05,Bob,4,1
```

## Restrict the edits to specific namespaces
Discard edits outside the main (article) namespace:
```
cat data/edits-2.csv | ./wikipedians/utilities/filter.py --ns=0 --verbose > \
	data/edits-3.csv
```
Example output:
```
timestamp,user,edits
2019-12-30,Alice,1
2019-12-31,Alice,1
2020-01-01,Alice,2
2020-01-02,Bob,1
2020-01-04,Alice,1
```

## Generate a pivot table
Create a column for each period and a row for each user
```
cat data/edits-3.csv | ./wikipedians/utilities/pivot_table.py --verbose > \
	data/edits-4.csv
```
Example output:
```
user,2019-12-30,2019-12-31,2020-01-01,2020-01-02,2020-01-04
Alice,1.0,1.0,2.0,,1.0
Bob,,,,1.0,
```
