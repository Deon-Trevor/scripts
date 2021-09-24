#!/usr/bin/python3

import dns.resolver
import re
import sys
from colorama import Fore, init, Style

def getSPF(resolver, domain):
	spfRegex = re.compile("^\"(v=spf1).*\"$")

	try:
		answer = resolver.resolve(domain, 'txt')

		for item in answer.response.answer:
			for line in item.items:
				if spfRegex.match(line.to_text()):
					return str(line)

	except dns.resolver.NoAnswer:
		return False

def getDMARC(resolver, domain):
	spfRegex = re.compile("^\"(v=DMARC).*\"$")

	try:
		answer = resolver.resolve("_dmarc." + domain, 'txt')

		for item in answer.response.answer:
			for line in item.items:
				if spfRegex.match(line.to_text()):
					return str(line)

	except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
		return False

def main():
	domain = sys.argv[1]
	resolver = dns.resolver.Resolver()
	spfRecord = getSPF(resolver, domain)
	spoofable = False

	if spfRecord:
		spfRecord = spfRecord.strip('"')
		print("\n[" + Fore.BLUE + "X" + Style.RESET_ALL + "] SPF record found: ")
		print(spfRecord)

		if "~all" not in spfRecord and "-all" not in spfRecord:
			print("\n[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " does not contain \"-all\" or \"~all\" in the SPF record.")
			spoofable = True
	else:
		print("\n[" + Fore.GREEN + "+" + Style.RESET_ALL + "] SPF record not found for " + domain)
		spoofable = True

	dmarcRecord = getDMARC(resolver, domain)
	dmarcTagRegex = r";\s*p=([^;]*)\s*;"
	dmarcTagMatch = None

	if dmarcRecord:
		dmarcRecord = dmarcRecord.strip('"')
		dmarcTagMatch = re.search(dmarcTagRegex, dmarcRecord)
	dmarcTag = None 

	if dmarcTagMatch:
		dmarcTag = dmarcTagMatch.group(1)

	if dmarcRecord:
		print("\n[" + Fore.BLUE + "X" + Style.RESET_ALL + "] DMARC record found: ")
		print(dmarcRecord)

		if not dmarcTagMatch:
			print("\n[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " does not have a policy set in the DMARC record.")
			spoofable = True

		elif dmarcTag == "none":
			print("\n[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " has policy set to \"none\" in the DMARC record.")
			spoofable = True
	else:
		print("\n[" + Fore.GREEN + "+" + Style.RESET_ALL + "] DMARC record not found for " + domain)
		spoofable = True

	if spoofable:
		print("\n" + Fore.YELLOW + domain + " CAN be spoofed.")

	else:
		print("\n" + Fore.RED + domain + " can NOT be spoofed.")

if __name__== "__main__":
	init(autoreset=True)
	main()