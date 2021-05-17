from googleVCF import *

def searchAbookPersonNumber(personName):
    personName=str(personName)
    bookRange=getBookRange()
    numbers=[]
    for nr in bookRange:
        if personName in makeABookDict(nr)['name']:
            numbers.append(nr)
    if len(numbers)>0:
        return(numbers)
    else:
        return "Nothing found"
        
        
def makeABookEntry(personNr):
    dictBookItem=makeDictBook()[personNr]      
    addressDict=splitAddressString(personNr)
    
    aBookDictPerson={
    'name': dictBookItem['name'],
    'email': makeEmailOneString(personNr),
    'phone': dictBookItem['phone'],
    'workphone': dictBookItem['workphone'],
    'mobile': dictBookItem['mobile'],
    'address': addressDict['address'],
    'address2': addressDict['address2'],
    'city': addressDict['city'],
    'state': addressDict['state'],
    'zip': addressDict['zip'],
    'country': addressDict['country']
    }
    
    return aBookDictPerson
            
def makeABookEntryStr(personNr):
    aBookEntry=makeABookEntry(personNr)
    aBookEntryStr="[" + str(personNr-1) + "]\n"
    for key in aBookEntry.keys():
        if aBookEntry[key]:      
            aBookEntryStr+=key + "=" + aBookEntry[key] + "\n"
    aBookEntryStr+="\n"
    return aBookEntryStr

def generateABookHeader(abookVersion):
    # 0.6.1
    headerStr="# abook addressbook file\n\n"
    headerStr+="[format]\n"
    headerStr+="program=abook\n"
    headerStr+="version=" + abookVersion + "\n\n\n"
    return headerStr
    
def makeABook(mode='cli'):
    abookVersion="0.6.1"
    dictBook=makeDictBook()
    bookRange=getBookRange()
    aBookStr=""
    aBookStr+=generateABookHeader(abookVersion)
    
    for personNr in bookRange:
        
        aBookStr+=makeABookEntryStr(personNr)
        
        percent=countPercent( personNr, max(bookRange) )
        progressStr=str(personNr) + " of " + str(max(bookRange)) + " converted"
        progressStrLen=len(progressStr)
        
        if mode=='cli' or mode=="":
            barWidth=60
            printProgressBar(percent, barWidth, 'Converting vCard to abook')
            print("|" + progressStr + " "*(barWidth-progressStrLen) + "|")
            print("="*barWidth)
        elif mode=='debug':
            print(progressStr)
        elif mode=='quiet':
            pass
        
        #print(str(percent) + "%")
    aBookStr+="\n"
    print("Success!!!")
    f=open("addressbook", "w")
    f.write(aBookStr)
    f.close()
    
    
    if __name__ == '__main__':
        print("Type ./vCardConverter.py")
        
