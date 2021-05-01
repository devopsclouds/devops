import getpass
import configparser
import os
##define a function for proxy
username = input(" Please enter account-01 username: ")
password = getpass.getpass(prompt=" Please enter account-01 password: ")

def callProxy():
    
    cp= configparser.RawConfigParser()
    cp.read(r"..\config\app.properties")
    http = cp.get("DEFAULT", "http")
    colon = cp.get("DEFAULT", "colon")
    at_rate_of = cp.get("DEFAULT", "at_rate_of")
    host = cp.get("DEFAULT", "host")
    http_proxy = http+username+colon+password+at_rate_of+host

    https_proxy = http+username+colon+password+at_rate_of+host
    os.environ['HTTP_PROXY'] = http_proxy
    os.environ['HTTPS_PROXY'] = https_proxy
    os.environ['http_proxy'] = http_proxy
    os.environ['https_proxy'] = http_proxy
    os.environ['NO_PROXY'] = ".ae.sda.corp.telstra.com,.corp.telstra.com,thyra.telstra.com,localhost,127.0.0.1"
    os.environ['NOPROXY'] = ".ae.sda.corp.telstra.com,.corp.telstra.com,thyra.telstra.com,localhost,127.0.0.1"
    os.environ['no_proxy'] = ".ae.sda.corp.telstra.com,.corp.telstra.com,thyra.telstra.com,localhost,127.0.0.1" 
    os.environ['noproxy'] = ".ae.sda.corp.telstra.com,.corp.telstra.com,thyra.telstra.com,localhost,127.0.0.1"

