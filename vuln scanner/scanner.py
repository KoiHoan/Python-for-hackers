#!usr/bin/env python
import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup
class Scanner:
    def __init__(self, url,ignore_links):
        self.target_url = url
        self.target_links = []
        self.session = requests.session()
        self.ignore_links = ignore_links

    def check_request(self,url):
        # url = f"{url}"
        try:
            return self.session.get(url)
        except requests.exceptions.ConnectionError:
            pass

    def extract_links_from(self,url):
        response = self.check_request(url)
        return re.findall('href="(.*?)"', response.text) #? is for non-greedy match
    
    def extract_forms(self,url):
        response = self.check_request(url)
        parsed_html = BeautifulSoup(response.text, 'html.parser')
        return parsed_html.findAll("form")
    
    def submit_form(self, form, value, baseurl):
        action=form.get("action")
        post_url=urlparse.urljoin(baseurl, action)
        method=form.get("method")
        post_data={}
        for field in form.findAll("input"):
            field_name=field.get("name")
            field_type=field.get("type")
            field_value=field.get("value")
            if field_type=="text":
                field_value=value
            post_data[field_name]=field_value
        if method=="post":
            return self.session.post(post_url,data=post_data)
        return self.session.get(post_url,params=post_data) 

    def crawl(self,url=None):
        if url==None:
            url=self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            link=urlparse.urljoin(url, link) #join the base url with the relative url
            # print(link)
            if "#" in link:
                link = link.split("#")[0] #remove the anchor part of the url
            if self.target_url in link and link not in self.target_links and link not in self.ignore_links: #remove external links and duplicates
                self.target_links.append(link)
                print(link)
                self.crawl(link) #crawl found links

    def run_scanner(self):
        for link in self.target_links:
            forms=self.extract_forms(link)
            for form in forms:
                print('[+] Testing form in '+link)
                is_vulnerable_to_xss=self.test_xss_in_form(form,link)
                if is_vulnerable_to_xss:
                    print('\n\n[***] XSS discovered in '+link+' in the following form:')
                    print(form)
                    print('\n')
            if "=" in link:
                print('[+] Testing '+link)
                is_vulnerable_to_xss=self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print('\n\n[***] XSS discovered in '+link)
                    print('\n')            

    def test_xss_in_form(self, form, url):
        xss_test_script="<sCript>alert('test')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        # print(response.text)   
        return xss_test_script in response.text
    
    def test_xss_in_link(self, url):
        xss_test_script="<sCript>alert('test')</scriPt>"
        url=url.replace("=","="+xss_test_script)
        # print(url)
        response = self.check_request(url)
        return xss_test_script in response.text