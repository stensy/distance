"""

zipmortestimate.py

This script should do the following:

I. take the ZIP code database and calculate the following:
    1. total population for each county
    2. percentage population of each ZIP code within a county
    3. which ZIPs belong to multiple counties

II. take the county mortality database and estimate:
    1. mortality in each ZIP based on percentage of county pop

"""

import csv

tofile = raw_input('Enter outfile. >')
countydict = {}
### read from countymort.csv in form countydict[FIPS] = (countyPop, breastMort, lungMort, prostMort, coloMort)

zipdict = {}
### read from zipsformortcomb.csv in from zipdict[ZIP] = (zipPop, FIPS)

countyzipdict = {}
### countyzipdict in format [FIPS] = ([zips])

countypopdict = {}
### countypopdict in format [FIPS] = countypop

with open('countymort.csv', 'rU') as countydictin:
	### countydict will be in format countydict[FIPS] = (countyPop, breastMort, lungMort, prostMort, coloMort)
	countydictreader = csv.reader(countydictin)
	countydictreader.next()
	for row in countydictreader:
		countydict[row[0]] = (row[1], row[2], row[3], row[4], row[5])

with open('zipsformortcomb.csv', 'rU') as zipdictin:
	### zipdict is in format zipdict[ZIP] = (zipPop, FIPS)
	zipdictreader = csv.reader(zipdictin)
	zipdictreader.next()
	for row in zipdictreader:
		zipdict[row[0]] = (row[1], row[8])

for key, (pop, fips) in zipdict.items():
	if fips in countyzipdict:
		countyzipdict[fips].append(key)
	else:
		countyzipdict[fips] = [key]

	if fips in countypopdict:
		countypopdict[fips] += int(pop)
	else:
		countypopdict[fips] = int(pop)

with open(tofile, 'wb') as zipoutfile:
	zipfilewriter = csv.writer(zipoutfile)
	zipfilewriter.writerow(['zip', 'zipPop', 'county', 'countyPop', 'zipProp', 
		'zipBreastMort', 'zipLungMort', 'zipProstMort', 'zipColoMort'])

	for key, (pop, fips) in zipdict.items():
		zipBreastMort = "unassigned"
		zipLungMort = "unassigned"
		zipProstMort = "unassigned"
		zipColoMort = "unassigned"

		try:
			(countyPop, countyBreastMort, countyLungMort, countyProstMort, countyColoMort) = countydict[fips]
			countyPop = countypopdict[fips]
		except:
			(countyPop, countyBreastMort, countyLungMort, countyProstMort, countyColoMort) = ("CountyKeyError", "CountyKeyError","CountyKeyError","CountyKeyError","CountyKeyError")

		try:
			zipProp = float(pop) / float(countyPop)
		except:
			zipProp = "ErrorInZipProp"

		try:	
			zipBreastMort = zipProp * float(countyBreastMort)
		except:
			zipBreastMort = "ErrorInCountyBreastMort"

		try:
			zipLungMort = zipProp * float(countyLungMort)
		except:
			zipLungMort = "ErrorInCountyLungMort"

		try:
			zipProstMort = zipProp * float(countyProstMort)
		except:
			zipProstMort = "ErrorInCountyProstMort"

		try:
			zipColoMort = zipProp * float(countyColoMort)
		except:
			zipColoMort = "ErrorInCountyColoMort"

		zipfilewriter.writerow([key, pop, fips, countyPop, zipProp, zipBreastMort, 
			zipLungMort, zipProstMort, zipColoMort])


