#!/usr/bin/python3
import os
import requests

Target_Domain = input("\nEnter Target domain\n> ")

host_io_token = os.environ["HOST_TOKEN"] # host.io api key
request = requests.get("https://host.io/api/web/{}?token={}".format(Target_Domain, host_io_token))
response = request.json()

if "error" in response:
    #If host.io doesn't have any results we do it a bit more manually
    print("\nRegistrar:\n\t")
    OrgAbuseEmail = "'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}\\b' | grep 'abuse'" # regex to filter for abuse contact
    os.system("whois {} | grep -E -o {}".format(Target_Domain, OrgAbuseEmail))
    print("\nFetching IP address.....")
    os.system("nslookup {}".format(Target_Domain))
    Target_IP = input("Enter IP address:\n> ")
    print("\nHosting Provider:\n")
    os.system("querycontacts {}".format(Target_IP)) # pip install querycontacts
    print("")

else:
    print("\nRegistrar:\n\t")
    OrgAbuseEmail = "'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}\\b' | grep 'abuse'"
    os.system("whois {} | grep -E -o {}".format(Target_Domain, OrgAbuseEmail))
    print("\nHosting Provider:\n")
    os.system("querycontacts {}".format(response["ip"]))
    print("")
