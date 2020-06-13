data/ptwiki-20200501-rev-data.json:
	./wikipedians/utilities/extract_rev_data.py \
	  data/ptwiki-20200501-stub-meta-history*.xml.gz --debug --verbose > $@

data/ptwiki-20200501-monthy-user-edits-5+.csv: \
		data/ptwiki-20200501-rev-data.json
	cat $< | ./wikipedians/utilities/aggregate.py --min-edits=5 --monthly \
		--verbose > $@

data/ptwiki-20200501-monthy-main-user-edits-5+.csv: \
		data/ptwiki-20200501-monthy-user-edits-5+.csv
	cat $< | ./wikipedians/utilities/filter.py --ns=0 --verbose > $@

data/ptwiki-20200501-pivot-table-monthy-main-user-edits-5+.csv: \
		data/ptwiki-20200501-monthy-main-user-edits-5+.csv
	cat $< | ./wikipedians/utilities/pivot_table.py --verbose > $@
