#!/usr/bin/env python

#######################################
#  ABOUT:
#  This program converts contacs.vcf
#  imported from google contacts
#  to simple addressbooks eg. abook
#  Google imports vCard and csv 
#  but there is too much of datas, 
#  so import eg. to Thunderbird or simpler
#  software is sometimes annoying.
#  I made this software to make simple address book
#  containing only basic informations:
#   * Full name
#   * Emails
#   * Phones
#   * Address
#
#  CONVENTIONS:
#  Every global variable has 
#  'g' prefix, so eg. 
#  gContactsBook is a global variable.
#  Every entry is generated by one function with argument
#  containing person number (personNr),
#  and entire book is created by loop for person number
#  from global variable gPersonNrs, created from gContactsRange 
#  Google book section reads contacts.vcf from google server
#  and converts to global list containing dictionares (gContactsBook).
#  
#### Common







def listKeys(*, prefix="", key="", count=5, suffix=""):
    listKeysList=[]
    for i in range(0,count):
        listKeyStr=str(prefix) + str(key) + str(i+1) + str(suffix)
        listKeysList.append(listKeyStr)
    return listKeysList

## Transform
def joinEmails(personNr):
    dictBookItem=gContactsBook[personNr]
    dictBookItemKeys=list( dictBookItem.keys() )
    emailList=[]
    emailKeys=listKeys(key='email')
    for key in emailKeys:
        if key in dictBookItemKeys:
            emailValue=dictBookItem[key]
            emailList.append(emailValue)
    emailStr=",".join(emailList)
    return emailStr

def splitAddressString(personNr):
    dictBookItem=gContactsBook[personNr]
    dictBookItemKeys=list(dictBookItem.keys())
    addressList=[]

    if 'address' in dictBookItemKeys:
        addressList=dictBookItem['address'].split(";")

    addressDict={
    'address': '',
    'city': '',
    'state': '',
    'zip': '',
    'country': '',
    'address2': ''
    }

    addressDictKeys=list( addressDict.keys() )
    addressListRange=range(0, len(addressList)-2)
    
    if 'address' in dictBookItemKeys:
        for index in addressListRange:
            addrKey=addressDictKeys[index]
            addressDict[addrKey]=addressList[index]
    
    return addressDict
    
## TransformEnd

## SearchEngine
def findItemNr(name, *, get='list'):
    #googleInit()
    #global gPersonNrs, gContactsBook
    searchResults=[]
    searchResultsStr=""
    
    for i in gPersonNrs:
        ind=i
        gContactsBook[ind]['number']=i
        if 'name' in list(gContactsBook[ind].keys()):
            if name in gContactsBook[ind]['name']:
                searchResults.append(gContactsBook[ind])
    
    searchResultsLen=len(searchResults)
    searchResultsRange=list(range(searchResultsLen))
                
    
    if get=='string':
        for i in searchResultsRange:
            personNr=searchResults[i]['number']
            searchResultsStr+="[{}]\n".format(str(personNr))
            for key in list(searchResults[i].keys()):
                if key!='number':
                    searchResultsStr+=f"{key} = {(searchResults[i][key])} \n"
            searchResultsStr+="\n"        
        searchResultsStr+="\nFound {} elements\n".format(str(searchResultsLen))                
                
    if get=='string':
        return searchResultsStr
    elif get=='list':
        return searchResults
    else: return "Invalid argument"
    
def findWhoHasKey(*, key='', get='list', listNumbers=False):
    searchResults=[]
    searchResultsStr=""
    searchResultsNrs=[]
    
    if key=='':
        return "No key typed to search"
        
    for i in gPersonNrs:
        ind=int(i)
        gContactsBook[i]['number']=ind
        if key in list(gContactsBook[ind].keys()):
            searchResults.append(gContactsBook[ind])
    
    searchResultsLen=len(searchResults)        
    searchResultsRange=list(range(searchResultsLen))
    
    if get=='string':
        for i in searchResultsRange:
            personNr=searchResults[i]['number']
            searchResultsNrs.append(str(personNr))
            searchResultsStr+="[{}]\n".format(str(personNr))
            for key in list(searchResults[i].keys()):
                if key!='number':
                    searchResultsStr+=f"{key} = {str(searchResults[i][key])} \n"
            searchResultsStr+="\n"        
        searchResultsStr+="\nFound {} elements\n".format(str(searchResultsLen))
    
    if get=='string':
        if listNumbers:
            listNumbersStr=", ".join(searchResultsNrs)
            searchResultsStr+=f"\n {listNumbersStr} \n"
        return searchResultsStr
    elif get=='list':
        return searchResults
    else: return "Invalid argument"
    

## SearchEngineEnd
######################################################

### TUI Interface
def countPercent(x, y):
    return format(float(x/y*100), '.2f')
    
def printFrame(frameStr, *, refresh=True):
    if refresh:
        print("\033c")
    print(frameStr)

def cls(): print("\033c")
    
def printProgressBar(percent, *, width=20, title="Progressbar", refresh=True):
    percent=float(percent)
    multiply=int(percent//(100/width))
    
    titLineLen=int((width-len(title))//2)
    percentText=str(percent) + "%"
    percentCenterLen=int((width-len(percentText))//2)
    percentCenter=" "*percentCenterLen + percentText + " "*percentCenterLen
    frameStr=""
    frameStr=" " + "="*titLineLen 
    frameStr+= " " + title + " "
    frameStr+= "="*titLineLen + "\n"
    frameStr+= "|" + " "*(width+1) + "|\n"
    frameStr+= "|[" + "#"*multiply + " "*(width-multiply-1) + "]|\n"
    frameStr+="|" + percentCenter + " |\n"
    frameStr+="|" + " "*width + " |"
    if refresh:
        printFrame(frameStr)
    else:
        printFrame(frameStr, refresh=False)


######################################################
### Google Contacts
#
#
# Most important global variables:
# * gContactsBook
# * gContactsRange
# * gPersonNrs
######################################################

def loadGoogleContacts():
    global gGoogleContactsFileIsOpen, gGoogleContactsFile
    
    try:    
        ## open file downloaded as vCard from Google Contacts
        f=open("contacts.vcf") 
        gGoogleContactsFile=f.read()
        f.close()
        gGoogleContactsFileIsOpen=True
    except FileNotFoundError:
        gGoogleContactsFileIsOpen=False

def convertGoogleContacts():    
    ## creates list named gContactsOrig
    # Index of list is contacts number counted from 0 (zero)
    ## gContactsOrig[personNr]
    global gContactsOrig, gPersonNrs, gContactsRange
    ## Replace separators
    if gGoogleContactsFileIsOpen:
        contactsStr=gGoogleContactsFile
        contactsStr=contactsStr.replace("BEGIN:VCARD\nVERSION:3.0","==") 
        contactsStr=contactsStr.replace("\nEND:VCARD","")
        itemFilterList=listKeys(key='item', suffix='.')
        for itemFilterKey in itemFilterList:
            contactsStr=contactsStr.replace(itemFilterKey, "")    
        ### create contacts book as list    
        gContactsOrig=contactsStr.split("\n==\n") 
        gContactsRange=range(0, (len(gContactsOrig)) )
        gPersonNrs=list(gContactsRange)
        return True
    else:
        return False
        
def getContactsFilter():
    global gContactsFilter
    # converts vcard keys to simpler keys
    gContactsFilter={
     "FN:": "name",
     "EMAIL;TYPE=INTERNET;TYPE=HOME:": "email1",
     "EMAIL;TYPE=INTERNET:": "email3",
     "EMAIL;TYPE=INTERNET:": "email4",
     "TEL;TYPE=CELL:": "mobile",
     "TEL;TYPE=WORK:": "workphone",
     "TEL;TYPE=HOME:": "phone",
     "TEL:": "phone",
     "ADR;TYPE=HOME:": "address"
    }
    

def getContactItem(personNr):
    # Converts gContactsOrig list item
    # to dictionary.
    # This procedure returns single item
    # which can be added to global dictionary
    # named gContactsBook
    
    contactFilter=gContactsFilter
    vcfPerson=gContactsOrig[personNr]
    vcfKeys=list(contactFilter.keys())
    filteredKeys=[list(contactFilter.values())]
    attributes=vcfPerson.split("\n") ## each attribute separated with \n
    
    contactItem={}
    
    for vcfKey in vcfKeys:
        for attribute in attributes:
            contactItemKey=contactFilter[vcfKey]
            if vcfKey in attribute:
                contactItem[contactItemKey]=attribute.replace(vcfKey, '')
    return contactItem
    
def createContactsBook():    
    ### Main engine
    ## Create a list containing dictionaries with book keys
    global gContactsBook ## the most important list
    gContactsBook=[]
    for personNr in gPersonNrs:
        contactItem=getContactItem(personNr)
        gContactsBook.append(contactItem)
    
def getGoogleContacts():
    global gGoogleContactsFile, gGoogleContactsFileIsOpen, gContactsOrig
    global gContactsRange
    getContactsFilter()
    loadGoogleContacts()
    if gGoogleContactsFileIsOpen:
        convertGoogleContacts()
        createContactsBook()
        ## empty cache from large variables
        del gGoogleContactsFile
        del gContactsOrig
        return True
    else:
        return False



######################################################
### abook creator

def getABookKeys():
    aBookKeys=['name', 
               'email', 
               'phone', 
               'workphone', 
               'mobile', 
               'address', 
               'address2',
               'city',
               'state',
               'zip',
               'country']
    
    return aBookKeys
        
            
def makeABookEntry(personNr):
    dictBookItem=gContactsBook[personNr]
    dictBookItemKeys=list(dictBookItem.keys())
    
    emailStr=joinEmails(personNr)
    addrStr=splitAddressString(personNr)
    
    addressDict=splitAddressString(personNr)
    addressDictKeys=list(addressDict.keys())
    abookKeys=getABookKeys()
    
    aBookDictPerson={}
    
    for key in abookKeys:
        if (key!='email') and (key not in addressDictKeys):
            try:
                aBookDictPerson[key]=dictBookItem[key]
            except KeyError:
                pass
        if key=='email': 
            try:
                aBookDictPerson['email']=emailStr
            except KeyError:
                print("Email doesn't exist")    
        if key=='address':
            try:
                for addrKey in abookKeys[5:]:
                    aBookDictPerson[addrKey]=addressDict[addrKey]
            except KeyError:
                print("Email doesn't exist")        
                aBookDictPerson[addrKey]=""
    return aBookDictPerson        
    
def makeABookEntryStr(personNr):
    aBookEntry=makeABookEntry(personNr)
    aBookEntryStr=f"[{str(personNr-1)}]\n"
    for key in aBookEntry.keys():
        if aBookEntry[key]:      
            aBookEntryStr+=f"{key}={aBookEntry[key]}\n"
    aBookEntryStr+="\n"
    return aBookEntryStr    

def makeABookHeader(abookVersion):
    # 0.6.1
    headerStr="# abook addressbook file\n\n"
    headerStr+="[format]\n"
    headerStr+="program=abook\n"
    headerStr+=f"version={abookVersion}\n\n\n"
    return headerStr
    
def makeABook(*, mode='tui', saveToFile=True):
    abookVersion="0.6.1"
    dictBook=gContactsBook
    bookRange=gContactsRange
    aBookStr=""
    aBookStr+=makeABookHeader(abookVersion)
    
    for personNr in bookRange:
        
        aBookStr+=makeABookEntryStr(personNr)
        
        percent=countPercent( personNr, max(bookRange) )
        progressStr=f"{str(personNr)} of {str(max(bookRange))} converted"
        progressStrLen=len(progressStr)
        
        if (mode=='tui' or mode=='tui' or mode=="") and saveToFile:
            barWidth=60
            printProgressBar(percent, width=barWidth, title='Converting vCard to abook')
            print("|" + progressStr + " "*(barWidth-progressStrLen) + "|")
            print("="*barWidth)
        elif mode=='debug' and saveToFile:
            print(progressStr)
        elif mode=='quiet' and saveToFile:
            pass
        #print(str(percent) + "%")

    aBookStr+="\n"
    if saveToFile:
        print("Success!!!")
        f=open("addressbook", "w")
        f.write(aBookStr)
        f.close()
    else: 
        print(aBookStr)

######################################################
#### CSV
## Yet not implemented


#### LDIF


### Claws Mail


### Test
def testIt(*, firstLast=True, findItem=False):
    getGoogleContacts()    
    print(f"contacts.vcf is open: {gGoogleContactsFileIsOpen}")
    if firstLast:
        minNr=min(gContactsRange)
        maxNr=max(gContactsRange)
        print(gContactsBook[minNr])
        print(gContactsBook[maxNr])
    if findItem:
        print(findItemNr('Michalik'))
        print(findWhoHasKey(key='address', get='string', listNumbers=True))
    #print(gContactsBook)
    #print(makeEmailOneString(55))
    #print(splitAddressString(34))
    #print(makeABookEntryStr(34))
    #print(makeABookEntryStr(55))


### MAIN

greetingStr="""
Welcome to simple commandline vCardConverter.

Steps to convert:

1) Download contacts.vcf 
   from your google account
   and save it in program directory
   
2) Put option for desired program. 
   Without arguments program 
   prints this help.

Usage:
--vcard-to-abook :     generates addressbook 
                       (after convert put 
                       created file to ~/.abookrc
                       
--find-person 'name':  find person name in book 
                       and returns entry
                       
--find-by-key 'key':   returns all entries 
                       containing 'key'                       
"""

### options

def mainAppOpts():
    argsPossible=[
    '--vcard-to-abook',
    '--find-by-key',
    '--find-person'
    ]
    if '--vcard-to-abook' in arguments:
        argInd=arguments.index('--vcard-to-abook')
        argNext=argInd+1
        mode='cli'
        try:
            if arguments[argNext]=='--debug':
                mode='debug'
            elif ((arguments[argNext]=='--quiet') or (arguments[argNext]=='-q')):
                mode='quiet'
        except IndexError:
            makeABook()
        makeABook(mode=f"{mode}")
    elif '--find-by-key' in arguments:
        try:
            argInd=arguments.index('--find-by-key')
            searchResultsStr=findWhoHasKey(key=f'{arguments[argInd+1]}', get='string', listNumbers=True)
            print(searchResultsStr)
            
        except IndexError:
            print("Missing key")
        
    elif '--find-person' in arguments:
        try:
            argInd=arguments.index('--find-person')
            searchResultsStr=findItemNr(f"{arguments[argInd+1]}", get='string')
            print(searchResultsStr)
            
        except IndexError:
            print("Missing argument")
    
    elif len(arguments)>1 and (arguments[1] not in argsPossible):
        print("Invalid args")
    
        
    


if __name__ == '__main__':
    import sys
    
    
    arguments=sys.argv
    
    run=getGoogleContacts()
    if run and len(arguments)>1:
        mainAppOpts()
        
    elif run and len(arguments)==1:
        print(greetingStr)
        
    elif not run and len(arguments)>=1:
        msg=greetingStr
        msg+="\n\n"
        msg+="WARNING !!!\n"
        msg+="File contacts not found. \n"
        msg+="Please download it from your google account \n"
        print(msg)
        
        
    
    
    

