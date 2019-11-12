from scraperParser import retrievedData
from scraperParser import tickerSymbol
import sys
import pandas as pd


def tupleDataCreation(dataSet):
    '''
    tupleDataCreation creates a pair of lists in order to allow csv creation
    ---param
    dataSet: dictionary
    ---return
    a pair of lists
    '''
    return(list(dataSet.keys()), list(dataSet.values()))
#end of tupleDataCreation

keyList, valueList = tupleDataCreation(retrievedData)

def checkFile(fileName):
    '''
    checkFile checks if a file with a given name exists within the computer folder
    ---param
    fileName: string
    ---return:
    boolean
    '''
    name = "C:\\Users\\tomti\\TOM TIAN\\tomwork\\Projects\\webScraping\\files\\" + fileName + ".csv"
    try:
        test = open(name)
        return(True)
    except:
        return(False)
#end of checkFile

def generateFile(inputFile):
    fileExists = checkFile(tickerSymbol)
    if (fileExists):
        #with open("C:\\Users\\tomti\\TOM TIAN\\tomwork\\Projects\\webScraping\\files\\" + tickerSymbol + ".csv") as f:
           # f.write('\n')
        inputFile.to_csv(r'C:\Users\tomti\TOM TIAN\tomwork\Projects\webScraping\files\GOOGL.csv', index=None, header=False, mode = "a") 
    else:
        print("Ran")
        export = inputFile.to_csv(r'C:\Users\tomti\TOM TIAN\tomwork\Projects\webScraping\files\GOOGL.csv', index=None, header=True)
    #end of if
#end of generateFile

inputList = [valueList]
df = pd.DataFrame(inputList, columns=keyList)


generateFile(df)
