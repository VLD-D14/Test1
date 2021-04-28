from pandas_datareader import data
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import dataframe as df
import numpy as np

#Import Air traffic
Airtraffic= pd.read_csv(r"C:\Users\Vincent\Desktop\python\Air_Traffic_Passenger_Statistics.csv")

#Inspect Data
print(Airtraffic.head())
print(Airtraffic.info())
print(Airtraffic.columns)

#Convert  Activity Period from int64 to datetime64[ns]
Airtraffic['Activity Period']= pd.to_datetime(Airtraffic['Activity Period'], format='%Y%m')
Airtraffic.set_index('Activity Period', inplace=True)

#Format DataFrame by using a pivot table to add all passenger to calculate the number of passsenger per month in '000
pivot = Airtraffic.pivot_table(index=['Activity Period'], values=['Passenger Count'], aggfunc=np.sum).div(1000000)
Traffic= pivot['2014':]

#Identify the lowest point of the data
print(' min value')
print(Traffic.idxmin())

#Inspect the amended Data
print(Traffic.head())
print(Traffic.tail())
print(Traffic.info())

#Import Data from yahoo finance to compare the correlation between the market and the number of passengers. Using the NYSE ARCA AIRLINE INDEX
AirIndex = ['^XAL']
start=datetime.datetime(2014,1,2)
end=datetime.datetime(2021,1,1)
AirExtract= data.DataReader(AirIndex,'yahoo',start,end)
print(AirExtract.head())

#Seclection of the Adj price
Air_Close=AirExtract["Adj Close"]

#Format the 2 Dataframes , by using the sampling period "Monthly". We will use the monthly mean for the index and amend the format of CSV to match
Airq= Air_Close.resample('M').mean()
Traffic1= Traffic.resample('M').sum()

#Merge the 2 dataframes
merge= [ Traffic1, Airq]
Twin= pd.concat(merge, axis=1)


#Plot the information to see any paterns
fig, ax = plt.subplots()
axb = ax.twinx()

#format the graph
ax.set_xlabel('Time')
ax.set_ylabel('Number of Passengers in Million',color='blue')
ax.set_title('Passenger Air Traffic versus the Airlines Index')
ax.grid(True)

# Annotate the date at lowest spot
ax.plot(Twin.index, Twin["Passenger Count"], color='blue', label='Passengers in M')
ax.legend(loc='best')
ax.annotate("Global Lockdown April 20", xy=(pd.Timestamp('2020-04-01'), 0.2),xytext=(pd.Timestamp('2017-01-01'), 1), arrowprops={'arrowstyle':'->', 'color':'gray'})
ax.set_ylim(ymin=0)

# Plotting on the second y-axis
axb.set_ylabel('Share Price in $',color='orange')
axb.plot(Twin.index, Twin["^XAL"], color='orange', label='Index Price')
axb.legend(loc='best')

#Grid formatting
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.show()


#Create a list of of stock using tickers
Stocks = ['AF.PA','DAL','^XAL','AIR.PA', 'BA']

# extract using API Yahoo finance , the funtion start and end were already define on the 1st data set
AirStocks= data.DataReader(Stocks,'yahoo',start,end).rolling(10).mean()

#inspect date
print(AirStocks.head())


#Merge DataFrame and and drop missing values
Airshare= pd.concat([AirStocks['Adj Close']], axis=1).dropna()

#Normalise the share price facilitate comparison
FirstPrice= Airshare.iloc[0]
Norm= Airshare.div(FirstPrice).mul(100)

#Inspect Data
print(Norm.head(15))

# Use subplot to analize the 2 industries:  Airlines and Aircraft Manufacturers
fig, ax = plt.subplots(2,1, sharey=True)

#Separate the 2 industies on the graphs
ax[0].plot(Norm.index,Norm["AF.PA"], label='Air France')
ax[0].plot(Norm.index,Norm["DAL"],label='Delta Air Lines', color='red')
ax[0].plot(Norm.index,Norm["^XAL"],label='Airline Index', color='black')
ax[1].plot(Norm.index,Norm["AIR.PA"],label='Airbus',color='orange')
ax[1].plot(Norm.index,Norm["BA"],label='Boeing',color='green')

#Set the X and Y axis
ax[0].set_xlabel('Time (in years)')
ax[1].set_xlabel('Time (in years)')
ax[0].set_ylabel('Share Price Airlines companies', color='blue')
ax[1].set_ylabel('Share Price Aircraft Manufacturers', color='green')

# Create a grib to facilate interpretation and comaprisons
ax[0].grid(b=True, which='major', color='#666666', linestyle='-')
ax[0].grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax[1].grid(b=True, which='major', color='#666666', linestyle='-')
ax[1].grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax[0].minorticks_on()
ax[1].minorticks_on()

#Add legend and title
ax[0].legend()
ax[1].legend()
ax[0].set_title('Air Industry overview through Share Price Variation')

plt.show()


# Using loop to find the lowest value of Air France
test = Norm["AF.PA"]
minimum = test[0]
for number in test:
    if minimum > number:
       minimum = number

Loss= (100-(minimum))
print('At the top of the crisis Air france had lost',Loss, 'percent of their value compare to 2014')

