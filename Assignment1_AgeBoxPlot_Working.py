# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:26:15 2020

@author: admin

TOP 10 CHEAPEST RESALE FLAT  (bar chart)

"""

import matplotlib.pyplot as plt
import numpy as np
import datetime

def textBasedAnalysis(fdata):
    print("textBasedAnalysis"+"-"*30)
    title = "Resale Prices for Registered Applications by Town and Flat Type"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    print("There are {} rows in this dataset".format(len(fdata)))
    #print(fdata)
    
    #null_rows = np.isnan(fdata['resale_price'])
    #print(null_rows)
    priceData = fdata[fdata['resale_price'] > 0]

    print("\n{} rows have valid values in the resale_price columns".format(len(priceData)))
    #print("{} rows has null values in the price columns".format(len(fdata)-len(nonnull_values)))
    
    set_qtr  = set(priceData['month'])
    set_town  = set(priceData['town'])
    set_type  = set(priceData['flat_type'])
    set_block = set(priceData['block'])
    set_street = set(priceData['street_name'])
    set_storey = set(priceData['storey_range'])
    set_floor = set(priceData['floor_area_sqm'])
    set_model = set(priceData['flat_model'])
    set_lease = set(priceData['lease_commence_date'])
    set_leaseLeft = set(priceData['remaining_lease'])
    set_price = set(priceData['resale_price'])
    
    print(str(len(set_qtr)) + " unique values in month column")
    print(str(len(set_town )) + " unique values in town column")
    print(str(len(set_type )) + " unique values in flat_type column")
    print(str(len(set_block )) + " unique values in block column")
    print(str(len(set_street )) + " unique values in street_name column")
    print(str(len(set_storey )) + " unique values in storey_range column")
    print(str(len(set_floor )) + " unique values in floor_area_sqm column")
    print(str(len(set_model )) + " unique values in flat_model column")
    print(str(len(set_lease )) + " unique values in lease_commence_date column")
    print(str(len(set_leaseLeft )) + " unique values in remaining_lease column")    
    print(str(len(set_price )) + " unique values in resale_price column")
           
    max_row_index = np.argmax(priceData['resale_price'])
    min_row_index = np.argmin(priceData['resale_price'])
    var = np.var(priceData['resale_price'])
    std = np.std(priceData['resale_price'])

    print()
    print("The mean Resale Price over the years is {:.0f}".format(np.mean(priceData['resale_price'])))
    print("The maximum Resale Price was in the year {} in {}({}) at ${:.0f}".format(priceData[max_row_index][0],priceData[max_row_index][1],priceData[max_row_index][2],priceData[max_row_index][10]))
    print("The minimum Resale Price was in the year {} in {}({}) at ${:.0f}".format(priceData[min_row_index][0],priceData[min_row_index][1],priceData[min_row_index][2],priceData[min_row_index][10]))
    print("The variance is {:.0f}".format(var))
    print("The standard deviation is {:.0f}".format(std))
    
#Extract Data
def extractData(f):
    print("extractData"+"-"*30)

    d = np.genfromtxt(f, delimiter=",", skip_header=True,
                                dtype=[('month','U30'),
                                       ('town','U30'),
                                       ('flat_type','U30'),
                                       ('block','U30'),
                                       ('street_name','U30'),
                                       ('storey_range','U30'),
                                       ('floor_area_sqm','U30'),
                                       ('flat_model','U30'),
                                       ('lease_commence_date','i4'),
                                       ('remaining_lease','U30'),
                                       ('resale_price','i8')],
                               missing_values=['na','-'],
                               filling_values=[0])
    #print(d)

    return d
 

def processData(fdata, startYear, endYear, flatType,townList):
    print("processData"+"-"*30)
    #print(fdata)
 
    #Data Cleaning
    #remove rows with missing prices
    fdata = fdata[fdata['resale_price'] > 0]
    
    #remove rows with missing lease_commence_date
    fdata = fdata[fdata['lease_commence_date'] > 0]
    
    #Filter by Flat type
    fdata = fdata[(np.char.upper(fdata['flat_type'])==np.char.upper(flatType)) ]

    years = np.arange(startYear, endYear+1)  #last x years
    
    currentDateTime = datetime.datetime.now()
    currentYear=int(currentDateTime.strftime("%Y"))
    
    #print(2020-np.array([1919,1818]))
    #print(currentYear)
    
    townAgeDict={}
    #filter by town
    for town in townList:
        #filter for this town
        townData = fdata[(np.char.upper(fdata['town'])==town)]

        #filter last 10 years data for this town and find Average Median Rent
        for yr in years:
            tmp = townData[np.char.find(townData['month'], str(yr)) > -1]

            #only find avg if there r data for the year
            if (len(tmp)>0):
                leaseYear=tmp['lease_commence_date']
                age = currentYear-np.array(leaseYear)

                townAgeDict[town]=(age)
    return townAgeDict
 
#display chart

#display line chart
def displayBoxPlot(chartData,startYear, endYear, flatType):
    print("displayBoxPlot"+"-"*30)

    title = "Age of Flat by Town from {} to {} ({} flats)".format(startYear,endYear,flatType)
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    plt.figure(2, figsize=(30,30))
    plt.title(title,fontsize=10)
    plt.xlabel('Town',fontsize=10)
    plt.ylabel('Age of flats (Years)',fontsize=10)
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10,rotation='horizontal')
    
    labels=[]
    values_combined=[]
    
    for town in chartData:
        labels.append(town)
        values_combined.append(chartData[town])
        
    bp_dict = plt.boxplot(values_combined,labels=labels,patch_artist=True)
    #bp_dict = plt.boxplot(values_combined,labels=labels,patch_artist=True, vert=False)

    ## change outline color, fill color and linewidth of the boxes
    for box in bp_dict['boxes']:
        # change outline color
        box.set( color='#7570b3', linewidth=2)
        # change fill color
        box.set( facecolor = '#1b9e77' )
        
    ## change color and linewidth of the whiskers
    for whisker in bp_dict['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    
    ## change color and linewidth of the caps
    for cap in bp_dict['caps']:
        cap.set(color='#7570b3', linewidth=2)
    
    ## change color and linewidth of the medians
    for median in bp_dict['medians']:
        median.set(color='red', linewidth=2)
    
    ## change the style of fliers and their fill
    for flier in bp_dict['fliers']:
        flier.set(marker='D', color='#e7298a', alpha=0.5)
    
    #print(bp_dict.keys())  

    for line in bp_dict['medians']:
        # get position data for median line
        x, y = line.get_xydata()[1] # top of median line
        # overlay median value
        plt.text(x, y, 'Median:{:.0f}'.format(y),
             horizontalalignment='center',fontsize=8) # draw above, centered
 
    #fliers = []
    for line in bp_dict['fliers']:
        ndarray = line.get_xydata()
        if (len(ndarray)>0):
           max_flier = ndarray[:,1].max()
           max_flier_index = ndarray[:,1].argmax()
           x = ndarray[max_flier_index,0]
           print("Flier: " + str(x) + "," + str(max_flier))
         
           plt.text(x,max_flier,'%.1f' % max_flier,horizontalalignment='center',fontsize=10,color='green') 

    plt.show()    

                  
#main
f1 = "D:/tsl/sp/pythonForDataScience/Assignments/assignment1/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv"
data1=extractData(f1)
f2 = "D:/tsl/sp/pythonForDataScience/Assignments/assignment1/resale-flat-prices-based-on-registration-date-from-jan-2015-to-dec-2016.csv"
data2=extractData(f2)

allData=np.concatenate((data1,data2))
textBasedAnalysis(allData)

towns4Rm=['WOODLANDS','CHOA CHU KANG','JURONG WEST','BUKIT BATOK','JURONG EAST']
flatType="4 ROOM"

townAge=processData(allData, 2016, 2020,flatType,towns4Rm)
displayBoxPlot(townAge,2016, 2020, flatType)


