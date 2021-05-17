#!/usr/bin/env python3

def countPercent(x, y):
    return format(float(x/y*100), '.2f')
    
def printFrame(frameStr, refresh='refresh'):
    if refresh=='refresh':
        print("\033c")
    print(frameStr)

def cls(): print("\033c")
    
def printProgressBar(percent, width=20, title="Progressbar", refresh='refresh'):
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
    if refresh=='norefresh':
        printFrame(frameStr, 'norefresh')
    else:
        printFrame(frameStr)


def readVcf(): 
    ### To get addressbook input readVcf()[0]
    ### to get vcf keys input readVcf()[1]
    ## Read vCard File
    f=open("contacts.vcf")
    string=f.read()
    f.close()
    
    ## Replace separators
    string=string.replace("BEGIN:VCARD\nVERSION:3.0","==") 
    string=string.replace("\nEND:VCARD","")
    contactsOrig=string.split("\n==\n") ### Each person separated with ==
    
    
    ## Assign entries to list
    for personNr in range(len(contactsOrig)):
        person=contactsOrig[personNr]
        attributes=person.split("\n") ## each attribute separated with \n
        contactsOrig[personNr]=attributes
    

    contactsStr=""
    
    
    contactsDict={
     "FN:": "name",
     "EMAIL;TYPE=INTERNET;TYPE=HOME:": "email1",
     "item1.EMAIL;TYPE=INTERNET:": "email2",
     "EMAIL;TYPE=INTERNET:": "email3",
     "item1.EMAIL;TYPE=INTERNET": "email4",
     "TEL;TYPE=CELL:": "mobile",
     "TEL;TYPE=WORK:": "workphone",
     "TEL;TYPE=HOME:": "phone",
     "item1.TEL:": "phone",
     "ADR;TYPE=HOME:": "address"
    }
    
    contactsNew=[list(contactsDict.values())]
    vcfKeys=list(contactsDict.keys())
  
    for personNr in range(len(contactsOrig)):
        contactsNew.append([""]*(len(contactsNew[0])))    
        for attrNr in range(len(contactsOrig[personNr])):
            for vcfKeyNr in range(len(vcfKeys)):
                if (vcfKeys[vcfKeyNr] in contactsOrig[personNr][attrNr])==True:
                    contactsNew[personNr+1][vcfKeyNr]=contactsOrig[personNr][attrNr].strip(vcfKeys[vcfKeyNr])
    
    #readVcfReturn=[contactsNew, contactsDict]
    return contactsNew

def testAlgo():
    contactsBook=readVcf()
    print(type(contactsBook))

def makeDictBook():
    origBook=readVcf()
    dictBookKeys=origBook[0]
    dictBook=[]
    bookRange=range(len(origBook))
    
    for personNr in bookRange:
        dictBook.append(dict({}))
        dictBook[personNr]=dict({})
        for attrNr in range(len(origBook[personNr])):
            attrKey=origBook[0][attrNr]
            dictBook[personNr][attrKey]=origBook[personNr][attrNr]    
    
    return dictBook

def getBookRange():
    bookRange = range(1, len(readVcf()))
    return bookRange



def makeEmailOneString(personNr):
    dictBookItem=makeDictBook()[personNr]
    emailList=[]
    emailKeys=['email1','email2','email3', 'email4']
    for key in emailKeys:
        emailValue=dictBookItem[key]
        if emailValue:
            emailList.append(emailValue)
    emailStr=",".join(emailList)
    return emailStr

## To test only
def splitAddressTest(personNr):
    dictBookItem=makeDictBook()[personNr]['address']
    addressList=[]
    addressList.append([""]*6)
    addressList=addressList[0]
    if dictBookItem:
        addressList=dictBookItem.split(";")
    return addressList
##
    
def splitAddressString(personNr):
    dictBookItem=makeDictBook()[personNr]['address']
    addressList=[]
    addressList=dictBookItem.split(";")
    addressListIndex=[0, 5, 1, 2, 3, 4]
    addressListRange=range(len(addressList))
    
    addressDict={
    'address': '',
    'address2': '',
    'city': '',
    'state': '',
    'zip': '',
    'country': ''
    }
    
    addressDictKeys=list(addressDict.keys())
    
    for index in addressListRange:
        addrKey=addressDictKeys[index]
        if len(addressList) > addressListIndex[index]:
            addressDict[addrKey]=addressList[index]
                    
    return addressDict
  
    
def makeTxtBook():
    contactsBook=readVcf()
    contactsStr="# TXT Book"
    for personNr in range(len(contactsBook)):
        contactsStr+="["+str(personNr)+"]\n"
        for attrNr in range(len(contactsBook[personNr])):
            contactsStr+=contactsBook[0][attrNr]+": "
            contactsStr+=contactsBook[personNr][attrNr]+"\n"
        contactsStr+="\n\n"

    f=open("txtbook.txt", "w")
    f.write(contactsStr)
    f.close()
  
if __name__ == '__main__':
    print("Type ./vCardConverter.py")
    


    

    






#print(str(item))


