# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:26:15 2020

@author: admin

TOP 10 CHEAPEST RESALE FLAT  (bar chart)

"""

import matplotlib.pyplot as plt
import numpy as np
import operator


def textBasedAnalysis(fdata):
    print("textBasedAnalysis"+"-"*30)
    title = "Median Resale Prices for Registered Applications by Town and Flat Type"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    print("There are {} rows in this dataset".format(len(fdata)))
    #print(fdata)
    
    #null_rows = np.isnan(fdata['price'])
    #print(null_rows)
    priceData = fdata[fdata['price'] > 0]

    print("\n{} rows have valid values in the price columns".format(len(priceData)))
    #print("{} rows has null values in the price columns".format(len(fdata)-len(nonnull_values)))
   
    set_qtr = set(priceData['qtr'])
    set_town = set(priceData['town'])
    set_type = set(priceData['type'])
    set_price = set(priceData['price'])

    print(str(len(set_qtr)) + " unique values in qtr column")
    print(str(len(set_town )) + " unique values in town column")
    print(str(len(set_type )) + " unique values in type column")
    print(str(len(set_price )) + " unique values in price column")
           
    max_row_index = np.argmax(priceData['price'])
    min_row_index = np.argmin(priceData['price'])
    var = np.var(priceData['price'])
    std = np.std(priceData['price'])

    print()
    print("The mean Resale Price over the years is {:.0f}".format(np.mean(priceData['price'])))
    print("The maximum Resale Price was in the year {} in {}({}) at ${:.0f}".format(priceData[max_row_index][0],priceData[max_row_index][1],priceData[max_row_index][2],priceData[max_row_index][3]))
    print("The minimum Resale Price was in the year {} in {}({}) at ${:.0f}".format(priceData[min_row_index][0],priceData[min_row_index][1],priceData[min_row_index][2],priceData[min_row_index][3]))
    print("The variance is {:.0f}".format(var))
    print("The standard deviation is {:.0f}".format(std))
    
#Extract Data
def extractData(f):
    print("extractData"+"-"*30)

    d = np.genfromtxt(f, delimiter=",", skip_header=True,
                               dtype=[('qtr', 'U7'),
                                      ('town', 'U30'),
                                      ('type','U20'), 
                                      ('price','i4')],
                               missing_values=['na','-'],
                               filling_values=[0])
    #print(d)
    textBasedAnalysis(d)

    #Data Cleaning
    
    #remove rows with missing prices
    d = d[d['price'] > 0]
    print(len(d))
    
    return d

#find average Median Rent over last x years for each town and sort in ascending order
#Median Resale prices by Town for a given period (years), sorted ascending/descending
def processData(fdata, startYear, endYear, descending,flatType):
    print("processData"+"-"*30)
    
    #Filter for that Flat type
    fdata = fdata[(np.char.upper(fdata['type'])==np.char.upper(flatType)) ]
    
    #print(fdata["town"])
    
    towns=np.char.upper(fdata['town'])
    all_towns=np.unique(towns)
    
    townPrices10YDict={}
    townAvgPrices10YDict={}
    years = np.arange(startYear, endYear+1)  #last x years
    
    #for every town, get the average median rent for the last x years
    for town in all_towns:
        #filter for this town
        townData = fdata[(np.char.upper(fdata['town'])==town)]

        #filter last 10 years data for this town and find Average Median Rent
        townPrice= []
        for yr in years:
           tmp = townData[np.char.find(townData['qtr'], str(yr)) > -1]
           #only find avg if there r data for the year
           if (len(tmp)>0):
                avgMedianRent = tmp['price'].mean()
                townPrice.append(avgMedianRent)
    
        townPrices10YDict[town]=townPrice
        townAvgPrices10YDict[town]=np.mean(townPrice)
     
    sortByTown = sorted(townAvgPrices10YDict.items(), key=operator.itemgetter(1),reverse=False)
        
    return sortByTown

#display the Chart
def displayBarChart(chartData,flatType, numRec, startYear, endYear,colour):
        print("displayBarChart"+"-"*30)
        #print(chartData)

        years = np.arange(startYear, endYear+1)
        
        #chart only Top x cheapest
        loc = np.arange(len(years))
        #plt.xticks(loc, years, rotation=45)
        xValues=[]
        yValues=[]
        
        for i in range(numRec):
            xValues.append(chartData[i][0])
            yValues.append(chartData[i][1])

        print(xValues)
        print(yValues)
        width = 0.35

        loc = np.arange(len(xValues))

        fig, ax = plt.subplots()
        rects1 = ax.bar(loc - width/2, yValues, width, color=colour)
        
        if (startYear==endYear):
            yearText="for {}".format(startYear)
        else:
            yearText="from {} to {}".format(startYear,endYear)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Towns')
        ax.set_ylabel('Average Median Resale Prices')
        ax.set_title('Top {} Towns with Lowest HDB Resale Prices {} ({} flats)'.format(numRec,yearText,flatType))
        ax.set_xticks(loc)
        ax.set_xticklabels(xValues)
        #ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('${:.0f}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        autolabel(rects1)

        fig.tight_layout()
        plt.xticks(loc, xValues, rotation=30)
        #plt.savefig('Bar_Top " + numRec+ " Cheapest'+flatType+".png")
        plt.show()
    
                    
#main
f = "D:/tsl/sp/pythonForDataScience/Assignments/assignment1/median-resale-prices-for-registered-applications-by-town-and-flat-type.csv"

flatType="3-Room"
data1=extractData(f)
sortAvg10YData=processData(data1, 2015, 2020, False,flatType)
displayBarChart(sortAvg10YData,flatType, 10, 2015, 2020,"green")

flatType="4-Room"
sortAvg10YData=processData(data1, 2015, 2020, False,flatType)
displayBarChart(sortAvg10YData,flatType, 10, 2015, 2020,"blue")

flatType="5-Room"
sortAvg10YData=processData(data1, 2015, 2020, False,flatType)
displayBarChart(sortAvg10YData,flatType, 10, 2015, 2020,"orange")
