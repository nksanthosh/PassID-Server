'''
    File name: builder.py
    Author: ZeroPass - Nejc Skerjanc
    License: MIT lincense
    Python Version: 3.6
'''

from ldif3 import LDIFParser
from asn1crypto import crl, x509
import re

from pymrtd.pki.crl import CertificateRevocationList
from pymrtd.pki.x509 import DocumentSignerCertificate

from database.storage.certificateRevocationListStorage import writeToDB_CRL, readFromDB_CRL
from database.storage.x509Storage import writeToDB_DSC, readFromDB_DSC
from database.storage.x509Storage import CscaCertificate

from pymrtd.pki.ml import CscaMasterList
from database.storage.storageManager import Connection

from settings import config


class Builder:
    """Building database structures and connections between certificates"""

    def __init__(self, cscaFile, dscCrlFile):
        """CSCAfile and dscCrlFIle need to be in ldif format - downloaded from ICAO website"""
        conn = Connection(config["database"]["user"], config["database"]["pass"], config["database"]["db"])
        self.parseDscCrlFile(dscCrlFile, conn)
        #self.parseCSCAFile(cscaFile, conn)

    def parseDscCrlFile(self, dscCrlFile, connection: Connection):
        """Parsing DSC/CRL file"""
        parser = LDIFParser(dscCrlFile)
        for dn, entry in parser.parse():
            if 'userCertificate;binary' in entry:
                countryCode = re.findall(r'[c,C]{1}=(.*)(,dc=data){1}', dn)[0][0]
                dsc = x509.Certificate.load(*entry['userCertificate;binary'])
                #parse to our object
                dsc.__class__ = DocumentSignerCertificate
                dsc.__init__()
                #write to DB
                writeToDB_DSC(dsc, countryCode, connection)

            if 'certificateRevocationList;binary' in entry:
                countryCode = re.findall(r'[c,C]{1}=(.*)(,dc=data){1}', dn)[0][0]
                revocationList = crl.CertificateList.load(*entry['certificateRevocationList;binary'])
                #parse to our object
                revocationList.__class__ = CertificateRevocationList
                revocationList.__init__()
                #write to DB
                writeToDB_CRL(revocationList, countryCode, connection)

    def parseCSCAFile(self, CSCAFile, connection: Connection):
        """Parsing CSCA file"""
        ml = CscaMasterList(CSCAFile)
        r = 9
