import matplotlib.pyplot as plot
from scipy import stats
import AQI




monitor = AQI.AQIMonitor()

x = list(range(24, 0, -1))
y = monitor.get_last_24hrs_AQI("Seattle", "Washington", "United States")
y = [aqi for aqi in y if not aqi == None]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def get_point(x):
    return slope * x + intercept

bestfitline = list(map(get_point, x))


plot.scatter(x, y)
plot.plot(x, bestfitline)
plot.show()