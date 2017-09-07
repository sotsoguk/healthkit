from xml.dom import minidom

# parses the 'export.xml' exported from iPhone 
def parseWeights(hkFile, sort=True):
	weights = []
	dates = []
	xmldoc = minidom.parse(hkFile)
	records = xmldoc.getElementsByTagName('Record')
	for r in records:
		if r.attributes['type'].value == "HKQuantityTypeIdentifierBodyMass":
			weight = r.attributes['value'].value
			date = r.attributes['startDate'].value[:10]
			weights.append(float(weight))
			dates.append(date)
	if sort:
		dates, weights = (list(t) for t in zip(*sorted(zip(dates,weights))))
	return dates, weights
