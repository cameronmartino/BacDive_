#!/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import json
import os

'''

This program collects all type strains from the DSMZ metadata collections api


'''

class BacdiveClient(object):
    headers = {'Accept': 'application/json'} #output application type (json by deafault)
    USERNAME = '' # username for bacdive api
    PASSWORD = '' # password for bacdive api
    credentials = HTTPBasicAuth(USERNAME, PASSWORD) # feed api credentials

#   _____________________________________________________________________________________________________________________________________

    def getAllLinksone(self):
        #To get a list with links to the Detail View for BacDive ID, but only for the first page.
        #To consider the other pages, you habve to change the url to 'http://bacdive.dsmz.de/api/bacdive/bacdive_id/?page=2' etc.
        
        #INPUT:
        response = requests.get('http://bacdive.dsmz.de/api/bacdive/bacdive_id/',headers=self.headers,auth=self.credentials)
            
        if response.status_code == 200: # check response code
            results = response.json()
            #OUTPUT:
            #object of type 'dict' with the fields 'count', 'previous', 'results', 'next'
            #the entries in field 'results' contain the URLs to correspondong strains separated by ',' e.g. {u'url:url1},{u'url:url2},{u'url:url3},etc
            return results

    def getAllLinksrest(self,next_page):
        #To get a list with links to the Detail View for BacDive ID, but only for the first page.
        #To consider the other pages, you habve to change the url to 'http://bacdive.dsmz.de/api/bacdive/bacdive_id/?page=2' etc.
        
        #INPUT:
        print 'http://bacdive.dsmz.de/api/bacdive/bacdive_id/?page=%s'%str(next_page)
        response = requests.get('http://bacdive.dsmz.de/api/bacdive/bacdive_id/?page=%s'%str(next_page),headers=self.headers,auth=self.credentials)
            
        if response.status_code == 200: # check response code
            results = response.json()
            #OUTPUT:
            #object of type 'dict' with the fields 'count', 'previous', 'results', 'next'
            #the entries in field 'results' contain the URLs to correspondong strains separated by ',' e.g. {u'url:url1},{u'url:url2},{u'url:url3},etc
            return results


    def getAllfiles(self,bacdive_id):
        # To get a JSON for each bac dive id
        
        # INPUT:
        response = requests.get('%s?format=json'%bacdive_id,headers=self.headers,auth=self.credentials)

        if response.status_code == 200: # check response code
            
            results = response.json()
        
            if "taxonomy_name" in results: # check id is in dict
                if "strains" in results["taxonomy_name"]: # check id is in dict
                    if not results["taxonomy_name"]["strains"]: # check list is not empty
                        return
                    else:
                        for s in results["taxonomy_name"]["strains"]:
                            if "is_type_strain" in s: # check id is in list of dict
                                if str(s["is_type_strain"]) == 'True': # if true write out
                                    # write that bacteria.json to file
                                    save_name=bacdive_id.split("/")
                                    #write out json file
                                    with open("%s.json"%(str(save_name[-2])), 'w') as outfile:
                                        json.dump(results, outfile)
                                    outfile.close()
                                    #OUTPUT: JSON file for bacdive id written to file
                                    return
                                else:
                                    # do not write out that bacteria to file if not type strain
                                    continue
                            else:
                                continue
                                
        return
            
    def run(self):
        q=406 #starting page
        #  Run the client in output directory
        os.chdir("/Users/cameronmartino/bin/bacdive")
        
        # get first page of urls
        print "Running page: 1 of bacterial ids from bac dive api"
        allLinks = self.getAllLinksone()
        for urldict in allLinks["results"]:
                print urldict["url"]
                temp_file = self.getAllfiles(urldict["url"])
        
        # run all other pages
        while q<=548: #end page
            print "Running page: %s of bacterial ids from bac dive api"%q
            allLinks = self.getAllLinksrest(str(q))
            #if allLinks["results"] is list or allLinks["results"] is tuple or allLinks["results"] is dict:
            for urldict in allLinks["results"]:
                print urldict["url"]
                temp_file = self.getAllfiles(urldict["url"])
            q+=1 #next page

if __name__ == '__main__':
    BacdiveClient().run()
