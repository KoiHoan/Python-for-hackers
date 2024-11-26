#!usr/bin/env python
import scanner
import requests


target_url="http://192.168.209.130/dvwa/"
data_dic={"username":"admin","password":"password","Login":"submit"}
ignore_links=['http://192.168.209.130/dvwa/logout.php']


vuln_scanner = scanner.Scanner(target_url,ignore_links)
response = vuln_scanner.session.post(target_url+"login.php",data=data_dic)
vuln_scanner.crawl()
vuln_scanner.run_scanner()
# forms=vuln_scanner.extract_forms("http://192.168.209.130/dvwa/vulnerabilities/xss_r/")
# print(forms)
# response = vuln_scanner.test_xss_in_link("http://192.168.209.130/dvwa/vulnerabilities/xss_r/?name=khoi")
# print(response)
# vuln_scanner.crawl()

