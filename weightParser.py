import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
import sys
from parse import parseWeights

def rolling_average(a, n=3):
	tmp = np.cumsum(a, dtype=float)
	tmp[n:] = tmp[n:] - tmp[:-n]
	return tmp[n-1:] / n

def main():
	# consts
	n = 5  # rolling average number of elements
	size = 1.91
	sizeInCm = int(size*100)
	#check args
	hkfile = 'Export.xml'
	outfile = 'output'
	if len(sys.argv) > 1:
		hkfile = sys.argv[1]
		if len(sys.argv) > 2:
			outfile = sys.argv[2]

	print("Importing HKData from %s, writing output to %s" %(hkfile,outfile))
	dates, weights = parseWeights(hkfile)
	bmi = list(map(lambda x: float(x)/(size**2), weights))
	print(weights)
	# calculate min / max values for plot
	minDate = min(dates)
	maxDate = max(dates)
	minBmi = min(bmi)
	maxBmi = max(bmi)
	minWeight = min(weights)
	maxWeight = max(weights)
	avweights = rolling_average(np.asarray(weights,dtype=float),n)
	avbmi = rolling_average(np.asarray(bmi,dtype=float),n)
	overWeight = 25*(size**2)
	print(maxWeight)

	# prepare plotting
	x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
	offset = (n-1) // 2
	fig = plt.figure(figsize=(20,15))
	ax = plt.subplot(211)
	plt.title('BMI')

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
	plt.axhspan(25,maxBmi,color='y',alpha =0.3)
	if (minBmi < 20):
	    plt.axhspan(15,20,color='y',alpha =0.3)

	ax.set_xlim(mdates.datestr2num(dates[offset]),mdates.datestr2num(dates[-offset]))
	ax.set_ylabel('BMI')
	ax.yaxis.grid(color='black',linestyle='dotted')
	plt.plot(x[offset:-offset],avbmi[:],c='blue',linewidth = 2.0)
	plt.gcf().autofmt_xdate()
	# print(ax.get_xlim())
	# plt.savefig('test.png')

	ax = plt.subplot(212)
	plt.title('WEIGHT')
	ax.set_xlim(mdates.datestr2num(dates[offset]),mdates.datestr2num(dates[-offset]))
	ax.set_ylabel('Weight')
	ax.yaxis.grid(color='black',linestyle='dotted')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
	plt.axhspan(overWeight,maxWeight,color='y',alpha =0.3)
	# plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	# plt.gca().xaxis.set_major_locator(mdates.DayLocator())

	plt.plot(x[offset:-offset],avweights[:],c='green',linewidth=2.0)
	plt.gcf().autofmt_xdate()
	plt.savefig('test.png')


if __name__ == "__main__":
	main()