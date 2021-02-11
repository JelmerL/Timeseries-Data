# Reading in large weather information files and making continuous timeseries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

print("This program extracts data of weatherstations in Brazil by region, concatenates data and summarizes as well as provides plotting functions")
print(" ")
print(" ")
print("This program needs to be run interactively with -i in order to be able to call scripts")

userinput= input("Would you like to investigate daily or 3xdaily data:")
print(" ")

if userinput == 'daily':

    #set current working directory
    os.chdir('C:\\Users')
    #Check if working directory is correct
    print(os.getcwd())

    print(" ")
    print(" Usable commands in this program are:")
    print(" readweather()")
    print(" prerunreadweather()")
    print(" readnewregion()")
    print(" selectmonthly()")
    print(" plotprecipmonth()")
    print(" plotprecip()")
    print(" plottemp()")
    print(" ")
    print(" ")
    print("This program comes preloaded with a sample weatherdatafile for testing")
    print(" ")

    def prerunreadweather():
        global weatherdatafull
        os.chdir()
        weatherdatafull = pd.read_csv("weatherdataselection.csv", parse_dates = True, index_col='Data');
        os.chdir()
        global code
        code='MG'
        global start
        start="2001-01-01"
        global end
        end="2016-01-01"
        global datacomb
        datacomb="7D"
        print("Sucessfully read in sample file weatherdata")
        
    os.chdir()
    prerunreadweather()
    os.chdir()

    def readweather():
        
        #Reading in list with characteristics of files
        global index
        index = pd.read_csv('INDEX.csv',usecols = ['Filenumber','Province']);

        #Automating extraction of column filename on basis of province and full rows
        global province
        province = index[index.Province == 'MG'];
        global filenames
        filenames = province['Filenumber'].astype(str) + '.csv';
        global weatherdatafull
        weatherdatafull = pd.DataFrame();
        
        for file in filenames:
            if os.path.isfile(file):
                print(file)
                global weatherdata
                weatherdata = pd.read_csv(file, skiprows = 15, parse_dates = True, keep_date_col = True,dayfirst = True,sep=';',index_col='Data')
                weatherdata = weatherdata['2001-01-01':'2016-01-01']
                print("Succesfully read in new file")
                weatherdatafull = pd.concat([weatherdatafull,weatherdata], axis=0).sort_index()
                print("Succesfully added data to cumulative file")


        weatherdatafull = weatherdatafull.resample('7D', how='mean', label='right') #resamples by month or whatever you want. Not perfect yet but has potential.
        print("succesfully resampled to weekly groups mean")
        os.chdir()
        weatherdatafull.to_csv("weatherdataselection.csv")
        os.chdir()
        print("succesfully saved file to csv")

    def readnewregion():
        
        #Reading in list with characteristics of files
        global index
        index = pd.read_csv('INDEX.csv',usecols = ['Filenumber','Province'])
        global provincecode
        provincecode = index['Province'].astype(str) #NOT READING FOR SOME REASON
        print("Files read");
        global code
        code = str(input('Input region code in capitals:'));
        global start
        start = str(input('Input start date in YEAR-MONTH-DAY format:'))
        global end
        end = str(input('Input end date in YEAR-MONTH-DAY format:'))
        global datacomb
        datacomb = str(input('Input averaging style for data resampling, example 7D = seven days: ')) 
        #Automating extraction of column filename on basis of province and full rows
        
        global province
        province = index[index.Province == code]
        global filenames
        filenames = province['Filenumber'].astype(str) + '.csv'
        global weatherdatafull
        weatherdatafull = pd.DataFrame()
            
        for file in filenames:
            if os.path.isfile(file):
                print(file)
                weatherdata = pd.read_csv(file, skiprows = 15, parse_dates = True, keep_date_col = True,dayfirst = True,sep=';',index_col='Data')
                weatherdata = weatherdata[start:end]
                print("Succesfully read in new file")
                weatherdatafull = pd.concat([weatherdatafull,weatherdata], axis=0).sort_index()
                print("Succesfully added data to cumulative file")

        weatherdatafull.to_csv("RAW" + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
        weatherdatafullres = weatherdatafull.resample(datacomb, how='mean', label='right')
        print("succesfully resampled to weekly groups mean")
        del weatherdatafullres['Hora']
        del weatherdatafullres['Estacao']
        del weatherdatafullres['Unnamed: 11']
        os.chdir()
        weatherdatafullres.to_csv(code + "_" + start + "_" + end + "_" + datacomb + ".csv")
        os.chdir()
        print("succesfully saved file to csv")


    def selectmonthly():

            global monthcode
            global weatherdatamonth
            global selectedmonths
            global code
            global start
            global end
            global datacomb
            
            print("With this function you can select and merge up to 6 specific months")
            print("If you have not read in the files please do so before using this function")
            userinput = str(input("Have you already read in the base file, yes or no?: "))

            if userinput == 'yes':

                userinput = str(input("Do you want to use the base file or a specific region and daterange file, answer base or daterange?:"))

                if userinput == 'base':
                                      
                    monthcode = int(input("Input month number: "))
                    weatherdatamonth = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                    selectedmonths = "month"
                    selectedmonths = selectedmonths + str(monthcode)
                    
                    Userinput = input("Add more data?")

                    while Userinput == 'yes':
                    

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth1 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth1], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth2 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth2], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth3 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth3], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth4 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth4], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth5 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth5], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")
                    
                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth6 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth6], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                    else: print("You've got it")
                    os.chdir()
                    weatherdatamonth.to_csv(selectedmonths + " " + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                    os.chdir()
                    print("Succesfully saved file to output folder")

                if userinput == 'daterange':

                    print(" ")
                    code = str(input("What is the region code of the file?: "))
                    start = str(input("What is the start date of the file(YEAR-MONTH-DAY format)?: "))
                    end = str(input("What is the end dae of the file (YEAR-MONTH-DAY format)?: "))
                    datacomb = str(input("What is the data combination method (7D,30D,2M etc)?: "))                                  
                    print(" ")
                    
                    global weatherdatarange
                    os.chdir()
                    weatherdatarange = pd.read_csv(code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                    os.chdir()
                    monthcode = int(input("Input month number: "))
                    weatherdatamonth = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                    selectedmonths = "month"
                    selectedmonths = selectedmonths + str(monthcode)
                    
                    Userinput = input("Add more data?")

                    while Userinput == 'yes':
                    

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth1 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth1], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth2 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth2], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth3 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth3], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth4 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth4], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth5 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth5], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")
                    
                        if Userinput == 'yes':
                            monthcode = int(input("Ok, Input month number: "))
                            weatherdatamonth6 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                            weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth6], axis=0).sort_index()
                            selectedmonths=selectedmonths+str(monthcode)
                        if Userinput == 'no':
                            break
                        
                        Userinput = input("Add more data?")

                    else: print("You've got it")
                    os.chdir()
                    weatherdatamonth.to_csv(selectedmonths + " " + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                    os.chdir()
                    print("succesfully saved file to output folder")

            if userinput == 'no':
                print("Please do so before you use this function")

        
    def plotprecipmonth():

        plt.plot(weatherdatamonth['Precipitacao'])
        plt.ylabel('Precipitation mm/week')
        plt.xlabel('Time (years)')
        plt.show()
        
    def plotprecip():

        plt.plot(weatherdatafull['Precipitacao'])
        plt.ylabel('Precipitation mm/week')
        plt.xlabel('Time (years)')
        plt.show()

    def plottemp():

        global y1
        global y2
        global x
        global weatherdatafull2
        
        y1 = weatherdatafull['TempMaxima']
        y2 = weatherdatafull['TempMinima']
        weatherdatafull2 = weatherdatafull.reset_index()
        x = weatherdatafull2['Data']
        
        plt.plot(x,y1,x,y2)
        plt.ylabel('Max/Min temperature Celcius')
        plt.xlabel('Time (years)')
        plt.show()
    
if userinput == '3xdaily':

    #set current working directory
    os.chdir()
    #Check if working directory is correct
    print(os.getcwd())

    print(" ")
    print(" Usable commands in this program are:")
    print(" readweather()")
    print(" prerunreadweather()")
    print(" readnewregion()")
    print(" selectmonthly()")
    print(" plothumidity()")
    print(" plotatm()")
    print(" plottemp()")
    print(" ")
    print("This program comes preloaded with a sample weatherdatafile for testing")
    print(" ")

    
    
    def readweather():
        
        #Reading in list with characteristics of files
        global index
        index = pd.read_csv('INDEX.csv',usecols = ['Filenumber','Province']);

        #Automating extraction of column filename on basis of province and full rows
        global province
        province = index[index.Province == 'MG'];
        global filenames
        filenames = province['Filenumber'].astype(str) + '.csv';
        global weatherdatafull
        weatherdatafull = pd.DataFrame();
        
        for file in filenames:
            if os.path.isfile(file):
                print(file)
                global weatherdata
                weatherdata = pd.read_csv(file, skiprows = 16, parse_dates = True, keep_date_col = False,dayfirst = True,sep=';',index_col=1)
                weatherdata.index.name = 'Data'
                weatherdata.columns=['Estacao','Hora','TempBulboSeco','TempBulboUmido','UmidadeRelativa','PressaoAtmEstacao','DirecaoVento','VelocidadeVentoNebulosidade','Cloudiness','Unknown']
                del weatherdata['Unknown']
                weatherdata = weatherdata['2001-01-01':'2016-01-01']
                print("Succesfully read in new file")
                weatherdatafull = pd.concat([weatherdatafull,weatherdata], axis=0).sort_index()
                print("Succesfully added data to cumulative file")


        weatherdatafull = weatherdatafull.resample('7D', how='mean', label='right')
        print("succesfully resampled to weekly groups mean")
        os.chdir()
        weatherdatafull.to_csv("weatherdataselection.csv")
        os.chdir()
        print("succesfully saved file to csv")

    def prerunreadweather():
            global weatherdatafull
            os.chdir()
            weatherdatafull = pd.read_csv("weatherdataselection.csv",  parse_dates = True, index_col='Data');
            os.chdir()
            global code
            code='MG'
            global start
            start="2001-01-01"
            global end
            end="2016-01-01"
            global datacomb
            datacomb="7D"

    os.chdir()
    prerunreadweather()
    os.chdir()
    
    def readnewregion():
        
        #Reading in list with characteristics of files
        global index
        index = pd.read_csv('INDEX.csv',usecols = ['Filenumber','Province'])
        global provincecode
        provincecode = index['Province'].astype(str) 
        print("Files read");
        global code
        code = str(input('Input region code in capitals:'));
        global start
        start = str(input('Input start date in YEAR-MONTH-DAY format:'))
        global end
        end = str(input('Input end date in YEAR-MONTH-DAY format:'))
        global datacomb
        datacomb = str(input('Input averaging style for data resampling, example 7D = seven days: ')) 

        #Automating extraction of column filename on basis of province and full rows
        
        global province
        province = index[index.Province == code]
        global filenames
        filenames = province['Filenumber'].astype(str) + '.csv'
        global weatherdatafull
        weatherdatafull = pd.DataFrame()
            
        for file in filenames:
            if os.path.isfile(file):
                print(file)
                weatherdata = pd.read_csv(file, skiprows = 16, parse_dates = True, keep_date_col = False,dayfirst = True,sep=';',index_col=1)
                weatherdata.index.name = 'Data'
                weatherdata.columns=['Estacao','Hora','TempBulboSeco','TempBulboUmido','UmidadeRelativa','PressaoAtmEstacao','DirecaoVento','VelocidadeVentoNebulosidade','Cloudiness','Unknown']
                del weatherdata['Unknown']
                weatherdata = weatherdata[start:end]
                print("Succesfully read in new file")
                weatherdatafull = pd.concat([weatherdatafull,weatherdata], axis=0).sort_index()
                print("Succesfully added data to cumulative file")

        weatherdatafull.to_csv("RAW" + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
        weatherdatafullres = weatherdatafull.resample(datacomb, how='mean', label='right') #resamples by month or whatever you want. Not perfect yet but has potential.
        print("succesfully resampled to weekly groups mean")
        del weatherdatafullres['Hora']
        del weatherdatafullres['Estacao']
        os.chdir()
        weatherdatafullres.to_csv(code + "_" + start + "_" + end + "_" + datacomb + ".csv")
        os.chdir()
        print("succesfully saved file to csv")


    def selectmonthly():
        
        global monthcode
        global weatherdatamonth
        global selectedmonths
        global code
        global start
        global end
        global datacomb
        
        print("With this function you can select and merge up to 6 specific months")
        print("If you have not read in the files please do so before using this function")
        userinput = str(input("Have you already read in the base file, yes or no?: "))

        if userinput == 'yes':

            userinput = str(input("Do you want to use the base file or a specific region and daterange file, answer base or daterange?:"))

            if userinput == 'base':
                                  
                monthcode = int(input("Input month number: "))
                weatherdatamonth = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                selectedmonths = "month"
                selectedmonths = selectedmonths + str(monthcode)
                
                Userinput = input("Add more data?")

                while Userinput == 'yes':
                

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth1 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth1], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth2 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth2], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth3 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth3], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth4 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth4], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth5 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth5], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")
                
                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth6 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth6], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                else: print("You've got it")
                os.chdir()
                weatherdatamonth.to_csv(selectedmonths + " " + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                os.chdir()
                print("succesfully saved file to output folder")

            if userinput == 'daterange':

                print(" ")
                code = str(input("What is the region code of the file?: "))
                start = str(input("What is the start date of the file(YEAR-MONTH-DAY format)?: "))
                end = str(input("What is the end dae of the file (YEAR-MONTH-DAY format)?: "))
                datacomb = str(input("What is the data combination method (7D,30D,2M etc)?: "))                                  
                print(" ")
                
                global weatherdatarange
                os.chdir()
                weatherdatarange = pd.read_csv(code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                os.chdir()
                monthcode = int(input("Input month number: "))
                weatherdatamonth = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                selectedmonths = "month"
                selectedmonths = selectedmonths + str(monthcode)
                
                Userinput = input("Add more data?")

                while Userinput == 'yes':
                

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth1 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth1], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth2 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth2], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth3 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth3], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth4 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth4], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth5 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth5], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")
                
                    if Userinput == 'yes':
                        monthcode = int(input("Ok, Input month number: "))
                        weatherdatamonth6 = weatherdatafull.loc[weatherdatafull.index.month == monthcode]
                        weatherdatamonth = pd.concat([weatherdatamonth, weatherdatamonth6], axis=0).sort_index()
                        selectedmonths=selectedmonths+str(monthcode)
                    if Userinput == 'no':
                        break
                    
                    Userinput = input("Add more data?")

                else: print("You've got it")
                os.chdir()
                weatherdatamonth.to_csv(selectedmonths + " " + code + "_" + start + "_" + end + "_" + datacomb + ".csv")
                os.chdir()
                print("succesfully saved file to output folder")

            

        if userinput == 'no':
            print("Please do so before you use this function")
                                  
    def plothumidity():

        plt.plot(weatherdatafull['UmidadeRelativa'])
        plt.ylabel('Relative humidity (%)')
        plt.xlabel('Time (years)')
        plt.show()
        
    def plotatm():

        plt.plot(weatherdatafull['PressaoAtmEstacao'])
        plt.ylabel('Atmospheric pressure (atm)')
        plt.xlabel('Time (years)')
        plt.show()

    def plottemp():

        global y1
        global y2
        global x
        global weatherdatafull2
        
        y1 = weatherdatafull['TempBulboSeco']
        y2 = weatherdatafull['TempBulboUmido']
        weatherdatafull2 = weatherdatafull.reset_index()
        x = weatherdatafull2['Data']
        
        plt.plot(x,y1,x,y2)
        plt.ylabel('Wet and Dry bulb temperature Celcius')
        plt.xlabel('Time (years)')
        plt.show()
