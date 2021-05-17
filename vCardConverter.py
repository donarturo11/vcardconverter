#!/usr/bin/env python3

from googleVCF import * 
from abookCreator import *

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
"""

if __name__ == '__main__':
    
    
    import sys
        
    arguments=sys.argv
    if '--vcard-to-abook' in arguments:
        mode='cli'
        if '--debug' in arguments:
            mode='debug'
        elif ('--quiet' or '-q') in arguments:
            mode='quiet'
        makeABook(mode)
        
        
    else:
        print(greetingStr)
