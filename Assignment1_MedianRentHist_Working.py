# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:26:15 2020

@author: admin

"""

import matplotlib.pyplot as plt
import numpy as np

def textBasedAnalysis(fdata):
    print("textBasedAnalysis"+"-"*30)
    title = "Median Rent by Town and Flat Type"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    print("There are {} rows in this dataset".format(len(fdata)))
    #print(fdata)
    
    #null_rows = np.isnan(fdata['price'])
    #print(null_rows)
    priceData = fdata[fdata['rent'] > 0]

    print("\n{} rows have valid values in the price columns".format(len(priceData)))
    #print("{} rows has null values in the price columns".format(len(fdata)-len(nonnull_values)))
   
    set_qtr = set(priceData['qtr'])
    set_town = set(priceData['town'])
    set_type = set(priceData['type'])
    set_rent = set(priceData['rent'])

    print(str(len(set_qtr)) + " unique values in qtr column")
    print(str(len(set_town )) + " unique values in town column")
    print(str(len(set_type )) + " unique values in type column")
    print(str(len(set_rent )) + " unique values in price column")
           
    max_row_index = np.argmax(priceData['rent'])
    min_row_index = np.argmin(priceData['rent'])
    var = np.var(priceData['rent'])
    std = np.std(priceData['rent'])

    print()
    print("The mean Resale Price over the years is {:.0f}".format(np.mean(priceData['rent'])))
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
                                      ('rent','i4')],
                               missing_values=['na','-'],
                               filling_values=[0])
    #print(d)
    textBasedAnalysis(d)

    #Data Cleaning
    
    #remove rows with missing prices
    d = d[d['rent'] > 0]
    
    return d

#Median Resale prices by Town for a given period (years)
def processData(fdata, startYear, endYear, flatType, townList):
    print("processData"+"-"*30)

    #Filter for that Flat type
    fdata = fdata[(np.char.upper(fdata['type'])==np.char.upper(flatType)) ]
    
    townRentDict={}
    years = np.arange(startYear, endYear+1)  #last x years
    
    #for every town, get the average median rent for the last x years
    for town in townList:
        #print("*"+town)
        #filter for this town
        townData = fdata[(np.char.upper(fdata['town'])==town)]
        #print(townData)

        # for this year, find Average Median Rent
        townRent= []
        for yr in years:
            print(yr)
            tmp = townData[np.char.find(townData['qtr'], str(yr)) > -1]
            #print("="*20)
            print(tmp)
            #only find avg if there r data for the year
            if (len(tmp)>0):
                medianRent = tmp['rent'].mean()
                townRent.append(medianRent)
            else:
                townRent.append(0)

        townRentDict[town]=townRent
    return townRentDict

#display line chart
def displayLineChart(chartData,flatType,startYear, endYear,townList):
    print("displayLineChart"+"-"*30)
    #print(chartData)

    title = "Median Rent from {} to {} ({} Flats)".format(startYear,endYear,flatType)
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    years = np.arange(startYear, endYear+1) 
    loc = np.arange(len(years))
    plt.xticks(loc, years, rotation=30)
 
    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.xlabel('Years')
    plt.ylabel('Median Rent')
    plt.title(title)

    for town in townList:
        ax1.plot(chartData[town], label=town, marker="o")
        print("median rent in {} in {} : {:.0f}".format(town,endYear,chartData[town][-1]))

    plt.legend(loc='upper right');

    #plt.savefig('Line_'+flatType+".png")
    
    plt.show()
    
#display chart
def displayHistogram(chartData,flatType,startYear, endYear,townList,colorList):
    print("displayHistogram"+"-"*30)
    print(chartData)

    title = "Median Rent from {} to {} ({} Flats)".format(startYear,endYear,flatType)
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    plt.xlabel('Median Rent')
    plt.title(title)
    
    i=1
    for town in townList:   
        plt.figure(i) # first figure
        # Create bins of 2000 each
        #newBins = np.arange(min(chartData[town]), max(chartData[town]), 20) # fixed bin size
        hist_all = plt.hist(chartData[town],alpha=0.5, 
                            color=['red'],
                            label=townList)
        plt.xlabel('Median Rent')
        plt.title(title)
        i=i+1
    

    '''
    plt.figure(2) # second figure
    plt.hist(values_TotalHospitalAdmissions,  
             alpha=0.5, 
             color=['red'])
    plt.title("Total Hospital Admissions",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    
    plt.figure(3) # second figure
    plt.hist(values_Polyclinics,  
             alpha=0.5, 
             color=['green'])
    plt.title("Polyclinics",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    
    plt.figure(4) # second figure
    plt.hist(values_DaySurgeries,  
             alpha=0.5, 
             color=['blue'])
    plt.title("Day Surgeries",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    
    plt.figure(5) # second figure
    plt.hist(values_DaySurgeries,  
             alpha=0.5, 
             color=['yellow'])
    plt.title("A&E",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    
    
    plt.figure(6) # second figure
    plt.hist(values_SpecialistOutpatientClinics,  
             alpha=0.5, 
             color=['cyan'])
    plt.title("Specialist Outpatient Clinics",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    plt.xticks(rotation='vertical')
    
    plt.figure(7) # second figure
    plt.hist(values_DentalClinics,  
             alpha=0.5, 
             color=['magenta'])
    plt.title("Dental Clinics",fontsize=20)
    plt.ylabel('Number of patients',fontsize=10)
    plt.xticks(rotation='vertical')
    '''
    plt.legend()
    plt.show()

    
#main
f = "D:/tsl/sp/pythonForDataScience/Assignments/assignment1/median-rent-by-town-and-flat-type.csv"

preferredTowns=['WOODLANDS','CHOA CHU KANG','JURONG WEST','BUKIT BATOK','JURONG EAST']
colorList = ["red","blue","green","yellow","grey"]

flatType="4-RM"
data1=extractData(f)
townPrice10Y=processData(data1, 2011, 2020,flatType, preferredTowns)
#displayLineChart(townPrice10Y,flatType, 2011, 2020, preferredTowns)
displayHistogram(townPrice10Y,flatType, 2011, 2020, preferredTowns,colorList)
