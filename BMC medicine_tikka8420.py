# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:16:40 2018

@author: pauli
"""
# Task 1.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 2018 and January 14 2018, and use also google searches: 

#(1) The quality of preventive care for pre-school aged children in Australian general practice
#(2) Louise K. Willes
#(3) 6.12.2018
#(4) 3 reviewers
#(5) Dagmar Haller 
#(6) (366 words), 
#(7a optional) MD PhD, University of Geneva
#(8) Lena Sanci 
#(9) (621 words), 
#(9a optional) Prof., Director, University of Melbourne
#(10) Lisa Whitehead 
#(11) (77 words), 
#(11a optional)Prof., Dean, Edith Cowan University Western Australia

#%%
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd #for importing files
# https://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.html
import numpy as np  #for calculations, array manipulations, and fun :)
import matplotlib.pyplot as plt #for scientifical plots
import os
#%Now I need also selenium
from selenium import webdriver  # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from statistics import mean 
#%%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
#For 2018..   (check th number of these..) 
urln_all='https://bmcmedicine.biomedcentral.com/articles?query=&volume=16&searchType=&tab=keyword'
urln_all2='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=2'
urln_all3='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=3'
urln_all4='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=4'
urln_all5='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=5'
#urln_all6='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=6'
#urln_all7='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=16&page=7'
#%%Here all combined..
utot=[urln_all, urln_all2, urln_all3, urln_all4, urln_all5]#, urln_all6]#, urln_all7]
soupn=[]
responsen=[]
one_a_tagn=[]
pub_date=[]
for i in range(0,len(utot)):
    responsen = requests.get(utot[i])
    soupn = BeautifulSoup(responsen.text, 'html.parser')
    one_a_tagn.append(soupn.findAll('a')) #ok
    pub_date.append(soupn.findAll('Published: ')) 
#%ok
mylistn=[]
for j in range(0,len(one_a_tagn)):   
#https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array
    for i in range(0, len(one_a_tagn[j])):
        mylistn.append((one_a_tagn[j][i]['href'])) #this has all
#%First) Goal would to print all the all articles' peerrieview sigths
#It is every third that we want to print from the list..starting from the first
inda=[]
for i in range(0, len(mylistn)):  
    str = mylistn[i]
    match = re.search(r'track/pdf/10.', str)
# If-statement after search() tests if it succeeded
    if match:
#        print('found', match.group()) ## 'found word:cat'
        inda.append(i-2)
#        print(i-2)  #this is ok   
        #%
thelistn=pd.DataFrame(mylistn)
#%
thelistn=thelistn.iloc[inda]    
#%
pr='/peer-review'
#%The first level for all one article's reviews:this is ist
download_url = 'https://bmcmedicine.biomedcentral.com'+ thelistn+pr 
orig_url = 'https://bmcmedicine.biomedcentral.com'+ thelistn #this is the list to the original..
#the download has the links to all reviews of single paper, but need to fethc one by one  
#%download_url had comhttps that need to go
#Check both orig and download urls for bad links:
inda=[]
for i in range(0, len(orig_url)):  
    str = orig_url.iloc[i][0]
    match = re.search(r'comhttp', str)
# If-statement after search() tests if it succeeded
    if match:
        inda.append(i) 
#        print(i)  #this is ok
orig_url=orig_url.drop(orig_url.index[inda],axis=0) 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
orig_url=orig_url.drop_duplicates()
#% I had comhttps also at download_url..
inda=[]
for i in range(0, len(download_url)):  
    str = download_url.iloc[i][0]
    match = re.search(r'comhttp', str)
# If-statement after search() tests if it succeeded
    if match:
        inda.append(i) 
#        print(i)  #this is ok
download_url=download_url.drop(download_url.index[inda],axis=0) 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
download_url=download_url.drop_duplicates() #the number is 227, while yesterday it was 226...
#%You may need to stop here
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
all_urls = []
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
#driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
#%Ok, eli tässä on jo melkein kaikki metadata.. dates:
def date(url=orig_url.iloc[0,0]):
    #% this straight below is just for testing
#    url=orig_url.iloc[0,0] #rivit vaihtuu, eli eka nolla 1,2, jne.,
    driver.get(url)
    all_spans2=[]
    au=[]
    title=[]
    if driver.find_element_by_xpath("//time")!=[]:
        all_spans2 =driver.find_element_by_xpath("//time")
        date=all_spans2.text
    elif driver.find_element_by_xpath("//time")==[]:
        date.append([i])
    elif len(driver.find_element_by_xpath("//time"))>1:
        try:

            if driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")!=[]:
                all_spans2 =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
                date=all_spans2[0].text
            elif driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")!=[]:
                all_spans2 =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")
                date=all_spans2[0].text
            else:
                date.append([i])
        except:
            pass
        #%
    else:
        date.append([i])
        #%
    try:
        if driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")!=[]:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
            authors=au.text
        elif driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")==[]:
            authors.append([i])
        elif len(driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']"))>1:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
            authors=au[0].text
        elif driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")!=[]:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")
            authors=au.text
        elif len(driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']"))>1:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")
            authors=au[0].text
        else:
            date.append([i])
    except:
        if driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")!=[]:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")
            authors=au.text
        elif len(driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']"))>1:
            au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed js-no-scroll']")
            authors=au[0].text
        else:
            date.append([i])
        
    try:
        if driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title u-h1']")!=[]:
            tita =driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title u-h1']")
            title=tita.text
            #%
        elif driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title u-h1']")==[]:
            title.append([i])
        elif len(driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title u-h1']"))>1:
            tita =driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title u-h1']")
            title=tita[0].text
        else:
            title.append([i])   
    except:
        pass
    try:
        if driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title']")!=[]:
            #        print('ok')
            tita =driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title']")
            title=tita.text
        elif driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title']")==[]:
            title.append([i])
        elif len(driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title']"))>1:
            tita =driver.find_element_by_xpath("//main/article/div/h1[@class='c-article-title']")
            title=tita[0].text
        else:
            title.append([i])
    except:
        title.append([i]) 
    #% Authors were not in one row..
    if "\n" in authors:
        authors=authors.split("\n")
    #    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        from functools import reduce #python 3
        authors2 = reduce(lambda x,y: x+y,authors)
    else:
        authors2=authors
    #%
    return date, authors2, title  
 
#%Here are publication dates and authors for each article, which takes time so better save:
datee_aut2=[]
for i in range(len(orig_url)):
    datee_aut2.append(date(url=orig_url.iloc[i,0]))
#%Datee2 should be saved..(dates, authors and titles without order)
dat=pd.DataFrame(datee_aut2)
dat.to_csv('dates_authors_titles_BMC2018_tikka29520.csv') #you can use this as datee_aut2 in future  
#datee_aut2=[]
#datee_aut2=pd.read_csv("dates_authors_titles_BMC2018_tikka29520.csv")
#datee_aut2=datee_aut2.iloc[:,1:4] #there was an extrac column   
#%This sorting must go hand in hand with orirg_url and download_url:
datee_aut2=pd.DataFrame(datee_aut2)
#datee_aut3=datee_aut2.iloc[:,1:5]
datee_aut3=datee_aut2
datee_aut3.columns = ['Date of Publication', "Writers of Article", "Title of Article"]
orig_url2=orig_url
orig_url2.rename(columns={0:'Link to Publication'}, inplace=True)
download_url2=download_url
download_url2.rename(columns={0:'Link to Review'}, inplace=True)
#%Putting all the datas in one place (dates, authors, titles, and urls)
# not obvious is to reset the index:
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html
auxif=[]
auxif=[datee_aut3.reset_index(drop=True), download_url2.reset_index(drop=True), orig_url2.reset_index(drop=True)]
auxif2=[]
auxif2=pd.concat(auxif, axis=1)   
#%Removing the duplicates, but are these linked similarly as curated 'orig_url'?
#it seems that this is not the case..
#https://www.geeksforgeeks.org/python-remove-duplicates-from-nested-list/
#res = list(set(tuple(sorted(sub)) for sub in datee_aut))
#So keeping the order: results ok :)
#from collections import OrderedDict
#ok=list(OrderedDict.fromkeys(datee_aut2))
##%% Saving
#da_au=pd.DataFrame(ok)
#da_au.to_csv('dates and authors_BMC2018_tikka15420.csv')
##%% Loading:
#da_au=[]
#da_au=pd.read_csv("dates and authors_BMC2018_tikka15420.csv")
#da_au=da_au.iloc[:,1:4] #there was an extrac column
#%This loop seem to be working below (24.1.2018), This takes 10 min, before enter, check if you already have what you need
tinka=[]
linkaas=[]
indaas=[]
for i in range(0,len(auxif2)):
    url=[]
    url=auxif2['Link to Review'][i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    one_a_tag = soup.findAll('a')
    link=[]
    for j in range(0,len(one_a_tag)):
        link.append(one_a_tag[j]['href'])
    ind=[]
    for n in range(0, len(link)):  
        str = link[n]
        match = re.search(r'Report_V', str)#in year 2018 this changes to V1 (or V0?), 2018 this changes to V2
        if match:
            ind.append(n)   
    linka=[]
    linka=pd.DataFrame(link)
    linkaas.append(linka)
    indaas.append(ind)
#%test..
#rint=[]    
#for i in range(len(indaas)):
#    rint.append(len(indaas[i]))
#np.sum(rint)    
#%The previous was also time consuming (5 min), so better save:
#linkaase=pd.DataFrame(linkaas)
#linkaase.to_csv('links_BMC2018_tikka17420.csv')   
#indaase=pd.DataFrame(indaas)
#indaase.to_csv('indeces_BMC2018_tikka17420.csv')
#linkaas=[]
#linkaas=pd.read_csv("links_BMC2018_tikka17420.csv")
#indaas=[]
#indaas=pd.read_csv("indeces_BMC2018_tikka17420.csv") 
##%% Loading:
#da_au=[]
#da_au=pd.read_csv("dates and authors_BMC2018_tikka15420.csv")
#da_au=da_au.iloc[:,1:4] #there was an extrac column 
#% This is why I like to be an engineer:
#%Let's take all the correct links first:
correct=[]
for i in range(len(linkaas)):
    correct.append(linkaas[i].iloc[indaas[i],0])  
#%There must be easier way to do this than this..most of them are V0 in the beginning of years
correct2n0=[]
correct2n1=[]
correct2n2=[]
correct2nn=[]
correct2na=[]
for i in range(len(correct)):
    if list(correct[i])!=[]:
        for j in range(len(correct[i])):
            if 'ReviewerReport_V0' in list(correct[i])[j]:
                correct2n0.append([i])
            elif 'ReviewerReport_V0' not in list(correct[i])[j]:
                continue
        for j in range(len(correct[i])):
            if 'ReviewerReport_V1' in list(correct[i])[j]:
                correct2n1.append([i])
            elif 'ReviewerReport_V1' not in list(correct[i])[j]:
                continue
        for j in range(len(correct[i])):
            if 'ReviewerReport_V2' in list(correct[i])[j]:
                correct2n2.append([i])
            elif 'ReviewerReport_V2' not in list(correct[i])[j]:
                continue
        for j in range(len(correct[i])):
            if 'ReviewerReport_V2' not in list(correct[i])[j]:
                correct2nn.append([i])
            else:
                continue
    if list(correct[i])==[]:
        correct2na.append([i])         
VO_ind=np.unique(correct2n0) #this is ok as such
V1_ind=np.unique(correct2n1) #I nedd indeces that are not in V0
V2_ind=np.unique(correct2n2)
V2n_ind=np.unique(correct2nn)
Vna_ind=np.unique(correct2na)
v1_ok=list(set(V1_ind) - set(VO_ind))
#https://www.programiz.com/python-programming/break-continue
#v2_ok_dif=list(set(V2_ind) - set(VO_ind))
#v2_ok=list(set(v2_ok_dif) - set(v1_ok)) #v2_ok not needed
#naps_na=[]
#for aps in list(Vna_ind):
#    naps_na.append(correct[aps]) #This is not needed, only the list(Vna_ind)
naps0=[]
for aps in list(VO_ind):
    naps0.append(correct[aps])    
naps1=[]
for aps in list(v1_ok):
    naps1.append(correct[aps])
naps00=[]
for i in range(len(naps0)):
    for j in range(len(naps0[i])):
        if 'ReviewerReport_V0' in naps0[i].iloc[j]:
            naps00.append([naps0[i].iloc[j], list(VO_ind)[i]])
        else:
            pass
naps11=[]
for i in range(len(naps1)):
    for j in range(len(naps1[i])):
        if 'ReviewerReport_V1' in naps1[i].iloc[j]:
            naps11.append([naps1[i].iloc[j], list(v1_ok)[i]])
        else:
            pass
naps_tot=naps00+naps11 #test naps_tot for the next file name..
#%This is one of the time consuming internet extraction steps that needs to be done separately:
#One needs to get the right order of pdfs/words already here, 
# note the way the pdfs have been named:
o=[]
i=0
for i in range(len(naps_tot)):
    o.append(np.str(naps_tot[i][1]))
    urllib.request.urlretrieve(naps_tot[i][0], \
                               filename='C:\\python\\BMC2018\\' +o[i]+' '+naps_tot[i][0][-37:])  
    #%you may need to check the range of naps_tot, e.g. from -39 to -37 in year 2018
#https://www.digitalocean.com/community/tutorials/how-to-convert-data-types-in-python-3  
#%%There are two ways to do this. Either converge all the files as one, or import them separately as a big pands frame.
# The method one:
#% Read all files with pdf to word and compress program, e.g.WPS PDF to Word
#the change the compressed doc to csv:
#https://convertio.co/de/docx-csv/
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
#https://stackoverflow.com/questions/22765313/when-import-docx-in-python3-3-i-have-error-importerror-no-module-named-excepti
#directory="C:\python\BMC\merge.csv"
#dataframes = pd.read_csv(directory, header=None)
#dataframes=dataframes.dropna()
#https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/   
#https://www.guru99.com/python-regular-expressions-complete-tutorial.html#3
#The method two: 
#%Now I need to do I loop for all files, and save the results
directory="C:\python\BMC2018\*.docx"
import glob
dataframes = []
all_files2=[]
all_files2=(glob.glob(directory))
#% Here I need to check the order of files for the cal..:
import natsort 
ll=all_files2
ll2=natsort.natsorted(ll)
all_files2=ll2
#%Designation:
nn=[]
for i in range(len(all_files2)):
    nn.append(all_files2[i][18:21])
#%It is here:
nn2=[]    
for i in range(len(nn)):
    nn2.append(int(nn[i].split(' ')[0]))
#% Preliminary info for calculating words funciton:
#    #https://stackoverflow.com/questions/13169725/how-to-convert-a-string-that-has-newline-characters-in-it-into-a-list-in-python
#    #https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
#    #% This is how you delete lists:
#    #https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/
#%Once you have the dataframe well extracted, the below function it should work:
    #%
import PyPDF2, io, requests
page_count=[]
for i in range(len(naps_tot)):
#    if naps_tot[i][0]=='nan':
    if 'static-content.springer.com/openpeerreview' in naps_tot[i][0]:
        response = requests.get(naps_tot[i][0])
        pdf_file = io.BytesIO(response.content) # response being a requests Response object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        page_count.append(num_pages)
    elif 'static-content.springer.com/openpeerreview' not in naps_tot[i][0]:
        page_count.append(0)
    elif naps_tot[i][0]=='nan':
        page_count.append(0)
    else:
        page_count.append(0)
        #%
#%Again for loading and saving:
tnz=pd.DataFrame(page_count)
            #%
#dfee=pd.DataFrame(dfe)
#dfee.to_csv('BMC2018_data_tikka1620.csv')
##%%
#total=pd.read_csv("BMC2018_data_tikka1620.csv")
##total=[]
#total=total.iloc[:,1:]
#dfe=total.values.tolist()
##%%
#tnon=[[] for i in range(403)]
#for i in range(len(total)):
#    for j in range(len(total[i])):
#        if total[i][j]!=[]:
#            text=[]
#            text = total[i][j]
#            text = text.split("', ")
#            for n in range(len(text)):
#                text[n]=text[n].replace("[","")
#                text[n]=text[n].replace("'","")
#                text[n]=text[n].replace("]","")
#            tnon[i].append(text)
#            https://stackoverflow.com/questions/10037742/replace-part-of-a-string-in-python
#            https://stackoverflow.com/questions/5387208/how-to-convert-a-string-to-a-list-in-python/5387227
#%e.g. important for loading:
#dfe=tnon            
#tnaa=[]        
#for i in range(len(tnon)):
#    tnaa.append(tnon[i][0])
    #%his is minimum:       
#total=total.values.tolist()
#total=total.iloc[:,1:] #this is not necessarily needed
#taxi=[]
#for i in range(len(total)): 
#    taxi.append([x for x in total[i] if x == x])
#total=taxi 
#%%
l=[]
for i in range(len(dfe)):
    for j in range(len(dfe[i])):
        if 'Michael Rembis' in dfe[i][j]:
            l.append(i)
            print(i)
    #%%
def words2(df2):
    #%
#    df2=dfe[489] #15 df2s two replace in testing (29520)
    io=[]
    xx=[]
    date=[]
    name=[]
    email=['The authors have adequately address the point raised','See attached marked-up manuscript',
           'Please find the comments in the attachment', 'in a separate file','See uploaded comments',\
           'Please see the attached pdf file','My comments are in a separate file','-- Attached --',\
           'See attachment', 'comments in the attachment', 'please see the attached','see attached',\
           'see attached file', 'See attached document', 'attached file', 'Attached file', 'see attachment'\
           ,'paper is much improved', 'is now acceptable for', 'attached document','have no revisions',\
           'please see uploaded document','Please see comments','Please see the attachment',\
           'The report is attached','the revisions have substantially improved the manuscript',
           'See attached report','Please see attached report','Please see report attached',\
           'report attached', 'attached report','have addressed all of the points','a file was attached'\
           'the revised manuscript is considerably improved','has been done in the report',\
           'document I have uploaded', 'I have uploaded document','listed in my report', 'in my report',\
           'See document uploaded', 'see the uploaded document', 'see uploaded document',\
           'The authors asswered all the reviewers coments', 'have answered all the comments',\
           'send my review before', "Please see the reviewer's report", 'my report is added as a word document',\
           'second revised manuscript', 'have adequately addressed','See uploaded report',
           'good first attempt','revised manuscript','I have no further request', 'open the appendix',\
           'the one I attached was','second revised', 'has been adequately revised', 'has been revised',\
           'I have no further comments', 'much improved','One more thing:']#, 'acceptable for',\
#           'is now acceptable', 'is improved','revisions made']
    appendix=[] 
    appendix2=[]
    for i in range(0, len(df2)):
        stra = (df2.iloc[i])
        match1 = re.search(r'Reviewer\'s report', stra)
        match1a = re.search(r"Reviewer's report:", stra)
        match2 = re.search(r'Are the methods appropriate and well described?', stra)
        match3 = re.search(r'https://', stra)
        match4 = re.search(r'Does the work include the necessary controls?', stra)
        match5 = re.search(r'Are the conclusions drawn adequately supported by the data shown?', stra)
        match6 = re.search(r'Are you able to assess any statistics in the \
                      manuscript or would you recommend an additional statistical review?', stra)
        match7 = re.search(r'I am able to assess the statistics', stra)
        match8 = re.search(r'Quality of written English', stra)
        match8b = re.search(r'Acceptable', stra)
        match8c = re.search(r'Which journal?',stra)
        match9 = re.search(r'Declaration of competing interests', stra)
        match10 = re.search(r'I declare that I have no competing interests.', stra)  
#        match11=re.search(r'The authors have adequately address the point raised', stra)
        
        if match1:
            io.append(i)
        elif match1a:
            io.append(i)
        elif match2:
            io.append(i)
        elif match3:
            io.append(i*100000)
            #%
        elif match4:
            io.append(i)
        elif match5:
            io.append(i)
        elif match6:
            io.append(i)
        elif match7:
            io.append(i)
        elif match8:
            io.append(i)
        elif match8b:
            io.append(i)
        elif match8c:
            io.append(i)
        elif match9:
            io.append(i)
        elif match10:
            io.append(i)
        for x in range(len(email)):
            if email[x] in stra:
                appendix.append(i)
        if 'Version:' in stra:
            if len(stra.split("Date:"))>1:
                date.append(stra.split("Date:")[1].split(" Reviewer:")[0])
            elif len(stra.split("Date:"))==1:
                date.append(stra.split("Date:"))
            else:
                pass
#                date.append('nan')                    
        else:
            pass
#            date.append([]) 
        if 'Reviewer:' in stra:
            if len(stra.split("Reviewer:"))>1:
                name.append(stra.split("Reviewer:")[1])
            elif len(stra.split("Reviewer:"))==1:
                name.append(stra.split("Reviewer:"))
            else:
                pass
    io.append(len(df2))
    io.append(2)
    io=np.sort(io)
            #%
    ox=io[0:3]
    jox=[0,2,2]
    new_list = []
    for element in ox:
        if element in jox:
            new_list.append(element)
    if len(new_list)==3:
        if len(io)>=3:
            io=io[2:]

            #%
    if io[0]==io[1]:
        io=io[1:]
    for i in range(0,len(io)):
        if io[i]>100000:
            io[i]=io[i]/100000
            #%
    dx= [0]
    if len(io)<2:
        io.insert(0,1)
#    https://stackoverflow.com/questions/3525953/check-if-all-values-of-iterable-are-zero
    #%
    for i in range(0,len(io)):
        if isinstance(io[i], float):
           dx.append(io[i])

    if len(io)>=6:
        if 'Quality of written English' not in df2[io[1]]:
            if io[1]+2!=io[2]:
                if io[0]+2==io[1]:
                    if 'Are the methods appropriate and well described?' not in df2[io[1]]:
                        io=io[1:]
        
    io3=[]
    for i in range(len(io)):
        if not isinstance(io[i], float):
           io3.append(io[i])
           #%

    res2=[]
    for i in range(0,(len(io3)-1)):
        a=list(tuple(range(io3[i], io3[i+1])))
#        print(a)
        if len(a)==1:
            res2.append([len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[a[0]]))),i])
        elif len(a)>1:
            for j in range(len(a)):
                res2.append([len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[a[j]]))),i])
        else:
            pass
    res4=pd.DataFrame(res2)
    den=[]
    for i in range(1,(len(io3)-1)):
        if len(res4.loc[res4.iloc[:,1]==i,0])>0:
            den.append(mean(res4.loc[res4.iloc[:,1]==i,0]))
        else:
            pass
    aa=[]
    for i in range(len(den)):
        if den[i]==np.max(den):
            aa.append(i+1)
    if io3[0]==0:
        io3=io3[1:]
    if len(io3)>=4:
        if np.sum(io[0]+io[1])<8:
            if abs(io3[2]-io3[1])>3:
                io3=io3[1:]
            elif abs(io3[3]-io3[2])>3:
                io3=io3[2:]
        elif abs(io3[2]-io3[1])>3:
            io3=io3[1:]
            if io3[0]>3:
               io3[0]=io[0] 
                #%
    if len(io3)>=6:
        if abs(io3[0]-io3[1])<4:        
            io3=io3[aa[0]:]
            #%

    io2=[] 
    if len(io3)>=3:
        a=io3[0:3]
        b=[0, 2, 2]
        c=io3[0:4]
        d=[0, 1, 2, 3]
        new_list = []
        for element in a:
            if element in b:
                new_list.append(element)
        if len(new_list)==3:
            io3=io3[2:]
        new_lista = []
        for element in c:
            if element in d:
                new_lista.append(element)
        if len(new_lista)==4:
            io3=io3[3:]
                        #%
    if len(io3)>1:
        if io3[0]+1!=io3[1]:
            if io3[0]==0 and len(io)>=6:
                if io3[2]+2<io3[3]:
                    io2=list(tuple(range(io3[2]+1, io3[3]))) 
                    #%
            elif io3[0]==2 and io3[1]==4 and len(io)>=6:
                try:
                    if io3[2]>6 or io3[2]>7: 
                        io2=list(tuple(range(io3[1]+1, io3[2])))
                    elif io3[0]+2==io3[1]:
                        io2=list(tuple(range(io3[0]+1, io3[1])))
                except:
                    pass
    
                #%
            
            elif len(io3)>2:
                if io3[1]<io3[2]:
                    tut=[]
                    tat=[]
                    tit=[]
                    for l in range(0,(len(io)-1)):
                        tut.append(abs(io[l+1]-io[l]))
                    for l in range(0,(len(tut)-1)):
                        tat.append(tut[l+1]-tut[l]) 
                    for l in range(0,(len(tat)-1)):
                        if tat[l+1]-tat[l]>1:
                            tit.append(l+1)
        
                    if tit!=[]:
                        if tit[0]>2:    
                            if len(tit)>1:
                                io3[0]=io[tit[0]-1]  
                                io3[1]=io[tit[1]] 
                    else:
                        pass
                else:
                    pass
                #%
                if 4<=len(io):
                    if io[2]+2<io[3]:
                        if np.sum(abs(io3[-1]-io3[-2])+abs(io3[-2]-io3[-3]))<=4:
                            if abs(io3[0]-io3[1])!=abs(io3[0]-io3[1]) and abs(io3[0]-io3[1])<4:
                                io2=list(tuple(range(io[1], io3[2]))) 
                            elif abs(io3[0]-io3[1])==abs(io3[0]-io3[1]) and abs(io3[0]-io3[1])>3:
                                io2=list(tuple(range(io3[0]+1, io3[1])))
                            #%
            elif io3[0]+2<io3[1]:
                if len(io3)>=2:
                    if (io3[0]+io3[1])>=7: 
                            io2=list(tuple(range(io3[0]+1, io3[1])))     
            else:         
                pass
            #%
    
        elif io3[0]+1==io3[1]:
            if np.sum(io3[0:3])<=7:
                io2=list(tuple(range(io3[1], io3[2])))
                #%
            elif len(df2)<=10 and 'Which journal?' in df2.iloc[4]:
                if io3[0]<=3:
                    io2=list(tuple(range(io3[0], io3[1]))) 
            elif 'Are the methods appropriate and well described?' in df2.iloc[3]:
                if np.max(den)==den[0]:
                    io2=[2]
            else:
                io2=list(tuple(range(io3[1]+1, io3[2])))
        #%
    if io2==[]:
        if len(io3)>1:
            if io3[0]+3<io3[1]:
                if io3[-1]==2+io3[-2] or io3[-2]==2+io3[-3]:
                    if 'Quality of written English is good' in df2.iloc[6]:
                        io2=list(tuple(range(io3[0]+1,io3[1]+1)))
                        #%
                    elif len(df2)<=8 and len(io3)==3 and io==io3:
                        io2=[io3[0]+1]
                    else:
                        io2=list(tuple(range(io3[0]+1,io3[1])))
                        #%
                else:
                    io2=list(tuple(range(io3[0],io3[1])))
            elif io3[0]+3>io3[1]:
                if np.sum(io3[0:3])>7:
                    if np.sum(io[0:4])>6:
                        if np.sum(io[0:3])>6 and 'Which journal?' not in df2.iloc[6]:
                            io2.append(io3[0]+1)
                        elif np.sum(io[0:3])<=6 and 'Which journal?' in df2.iloc[6]:
                            io2=[5]
                    elif np.sum(io[0:4])<=6:
                        io2.append(io[1]+1)
            elif io3[0]+3==io3[1]:
                if io3[0]+1<io3[1]:
                    io2=list(tuple(range(io3[0]+1,io3[1])))
            
 #%
    if io2==[]:
        if np.sum(io3[0:3])<=6:
            if len(io3)>=4:
                io2=list(tuple(range(io3[2]+1,io3[3])))
            elif io3[0]+2<io3[1]:
                io2=list(tuple(range(io3[0]+1,io3[1])))
            else:
                if abs(io3[0]-io3[1])<3:
                    io2=list(tuple(range(io3[1]+1,io3[(len(io3)-1)])))
                elif abs(io3[0]-io3[1])>2:
                    io2=list(tuple(range(io3[0]+1,io3[(len(io3)-1)])))
                
                
        elif np.sum(io3[0:3])>6:
            if len(io3)>4:
                io2=list(tuple(range(io3[1]+1,io3[-2])))
            else:
                io2=list(tuple(range(io3[0]+1,io3[-1])))
    if io2==[]:
        if len(io3)>0:
            if len(io3)==2:
                io2=list(tuple(range(io3[0]+1,io3[-1])))
            if len(io3)==1:
                if np.sum(io[0:3])<=6:
                    io2=list(tuple(range(io[2]+1,io[3])))
    if io2!=[]:
        if io2[0]==io3[0]:
            if len(io3)>=len(io) and len(io3)>3 and len(io2)>1:
                io2.pop(0)
            
#        else:
#%            io2=[0,len(df)]
#    if io2==[]:
    x=io[0:3]
    y=[2,2,4]
    new_list = []
    for element in x:
        if element in y:
            new_list.append(element)
            #%
    if len(new_list)==3:
        if len(io3)>=3:
            if sum(io3)<=18:
                io2.append(3)
                #%
    oo=io3[0:2]
    joo=[2,2]
    new_list = []
    for element in oo:
        if element in joo:
            new_list.append(element)
    
    if len(new_list)==2:
        if len(io3)>=3:
#            for i in range(io3)
            io2.append(io3[2])
            if len(io2)==2:
                io2=list(tuple(range(io2[0],io2[1])))
            else:
                pass
            #%
    if len(den)>2:
        if den[2]>den[1]:
            if den[1]>den[0]:
                if len(io2)==1:
                    io2=[]
                    io2=[io3[1]+1]
                   #% 
        elif den[1]>den[0]:
            if len(io2)==1:
                if len(io)<8:
                    if len(io3)+2>=len(io):
                        io2=[]
                        io2=[io3[0]+1]
        elif len(den)==2:
            if den[1]>den[0]:
                if len(io3)==3:
                    io2=[]
                    io2=[io3[1]+1,io3[-1]-1]
                    #%
    elif len(den)==2:
        if den[1]>den[0]:
            if len(io2)==1:
                io2=[]
                io2=list(tuple(range(io3[1]+1,io3[-1]-1)))
        
        
#    else:
#        if len(io2)==1:
            
            
        
#%
#%https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/    
    res=[]
#https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
#'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'

    if len(io2)>1:
        for i in io2:
            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[i]))))
    elif len(io2)==1:
        if io2[0]==3:
            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[3]))))
        elif io2[0]==5:
            if 'Quality of written English' not in df2.iloc[5]:
                res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[5]))))
            else:
                res=[]
                res.append(0)
        elif io2[0]==6:
            if 'Please indicate the quality of language in the manuscript:' not in df2.iloc[6]:
                res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[6]))))
            else:
                res=[]
                res.append(0)
        else:
            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[io2[0]]))))
            #%
    if len(res)==1:
        if res[0]==1:
            pass
        elif res[0]<=4 and res[0]>1:
            if len(io3)>1:
                if 'minor essential' not in df2.iloc[2]:
                    if 'If not, please specify what is required in your comments to the authors. Yes' not in df2.iloc[io3[1]+1]:
                        if 'Major Compulsory Revisions' not in df2.iloc[3]:
                            if 'No specific comment!' not in df2.iloc[3]:
                                if 'a file was attached' not in df2.iloc[3] and io2[0]!=3:
                                    res=[]
                                    res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[io3[1]+1]))))
#                        elif io2[0]==3:
#                            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df2.iloc[3]))))
            #%
        elif res[0]==14:
            if 'Are the methods appropriate and well described?' in df2.iloc[3]:
                if io2[0]<=4:
                    res=[]
                    res.append(0)
            else:
                pass
                #%
    if appendix==[]:
        appendix2.append('no')
    elif appendix!=[]:
        appendix2.append('attached')
    if " Reviewer" in name[0]: #huomaa heittomerkki
        name[0]=name[0].split(" Reviewer")[0]
    else:
        pass
    #%
    if len(name)>0:
        name=name[0][1:(len(name[0])-1)]
    #%
    if len(date)>0:
        date=date[0][1:(len(date[0]))]
#    print(np.sum(res))
        #%
    return  np.sum(res), appendix2, date, name

#% Calculating all the papers in a loop:
#file_count(all_files2): 
import docx2txt
count=[]  
df=[]
result=[]
r2=[]
list2=[]
list3=[]
list4=[]
a=[]
b=[]
for i in range(len(all_files2)):
    result.append(docx2txt.process(all_files2[i]))
    r2.append(result[i].splitlines())
    #%
    list2.append([e for e in r2[i] if e]) 
    list3.append([x.split("\t") for x in list2[i]])
    list4.append([e for e in list3[i] if e])
        
    #%
for i in range(len(list4)):
    for j in range(len(list4[i])):
        if np.shape(list4[i][j])>(1,):
            list4[i][j][0]=(" ".join([e for e in list4[i][j] if e]))
          
dfe=[]
for i in range(len(list4)):
    dfe.append(pd.DataFrame(list4[i])) 
#%
for i in range(len(dfe)):
    dfe[i]=dfe[i].iloc[:,0]  
        #%
count=[]
ff=[]
count1=[]
count2=[]
count3=[]
counta=[]  
countb=[] 
for i in range(len(dfe)):
#    print(i)
    count.append(words2(dfe[i])[0]) #Yes!! Got it!!
    #%
    count1.append(dfe[i][1])
    count2.append(dfe[i][2])
    count3.append(words2(dfe[i])[3]) #dfe[i][3]), name
    counta.append(words2(dfe[i])[2]) #options: words2(dfe[i])[1], dfe[i][0:5], date
    countb.append(words2(dfe[i])[1])
#%Because of these dependencies, you need to do these phases one-by-one
#Title, name, date:
#date=[]
#name=[]
#i=0
#j=0
#for i in range(len(counta)):
#    for j in range(0,len(counta[i])):#check indeces..
#        if 'Version:' in counta[i].iloc[j]:
#            if len(counta[i].iloc[j].split("Date:"))>1:
#                date.append([counta[i].iloc[j].split("Date:")[1].split(" Reviewer:")[0],i])
#            elif len(counta[i].iloc[j].split("Date:"))==1:
#                date.append([counta[i].iloc[j].split("Date:"),i])
#            else:
#                pass
##                date.append('nan')                    
#        else:
#            pass
##            date.append([]) 
#        if 'Reviewer:' in counta[i].iloc[j]:
#            if len(counta[i].iloc[j].split("Reviewer:"))>1:
#                name.append([counta[i].iloc[j].split("Reviewer:")[1],i])
#            elif len(counta[i].iloc[j].split("Reviewer:"))==1:
#                name.append([counta[i].iloc[j].split("Reviewer:"),i])
#            else:
#                pass
##                name.append('nan')
#        else:
#            pass
##            name.append('nan')
#        #%
#for i in range(len(name)):
#    if " Reviewer" in name[i][0]: #huomaa heittomerkki
#        name[i][0]=name[i][0].split(" Reviewer")[0]
#%
#datee=pd.DataFrame(date)
#namee=pd.DataFrame(name)
#nameey = namee.sort_values(1, ascending=False)
#nameey = nameey.drop_duplicates(subset=1, keep='first')
#dateey = datee.sort_values(1, ascending=False)
#dateey = dateey.drop_duplicates(subset=1, keep='first')
##%
#ax2=[]
#for i in range(len(nameey)):
#    for j in range(len(dateey)):
#        if namee.iloc[i,1]==datee.iloc[j,1]:
#            ax2.append([namee.iloc[i,0], datee.iloc[j,0], i])
#nam_dat=pd.DataFrame(ax2)
#%
title_ok=[]
for i in range(len(count)):
    if "Title:" in count1[i]: #huomaa heittomerkki
        title_ok.append(count1[i].split("Title:")[1])
    else:
        title_ok.append('nan')        
#%Dropping extra lines
tok2=[]
for i in range(len(title_ok)):
    tok2.append(title_ok[i][1:(len(title_ok[i])-1)])
    #%
name2=count3
#for i in range(len(nam_dat)):
#    name2.append(nam_dat.loc[i,0][1:(len(nam_dat.loc[i,0])-1)])
#    #%
date2=counta
#for i in range(len(nam_dat)):
#    date2.append(nam_dat.loc[i,1][1:(len(nam_dat.loc[i,1]))])
    #%
#%There could be better solution suggestion than this indexing:
#https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
#%To get the right columns one has to exercise a bit:
ana=[]
for i in range(len(nn2)):
    for j in range(len(auxif2)): 
        if nn2[i]==auxif2.index[j]: 
            #designation is in the first column
            ana.append(auxif2.iloc[j,:])
            #%
pana=pd.DataFrame(ana)
panax=pana.reset_index(drop=True)
#% Finally save the data:
tot_count=[]
count_ok=pd.DataFrame(count) 
title_ok2=pd.DataFrame(tok2)     
date_ok=pd.DataFrame(date2)
name_ok=pd.DataFrame(name2) 
countb=pd.DataFrame(countb)   
#%   
#%Muutetaan naps_tot dataframeks:
frames = [count_ok, title_ok2, name_ok, date_ok, panax, countb, tnz]
tot_count = pd.concat(frames, axis=1) #note the axis! and drop indeces..
#%it worked, yei!! :)
tot_count.columns = ['Review Word Count', "Article's Title", \
   'Reviewer Name', 'Reviewing Date', \
   'Date of Publication','Writers of Article','Title of Article', \
   'Link to All Reviews', 'Link to Publication','Attachments', 'Page Count']# 'Link to PDFs']
tot_count['Journal Name']='BMC Medicine'
#%IF indeces too small or litte, you may need to do...
#tot_count=tot_count.loc[0:340,:]
#tot_count=tot_count.reset_index(drop=True)
#%The form of pdfs are like..
#tot_count['Link to PDFs']=ntg.iloc[xxx,0]
#xxx=ntg.iloc[[22,44,...],0]
#%
ntg=pd.DataFrame(naps_tot) 
ntg2=ntg
ntg2.index=ntg.iloc[:,1]
ntg2=ntg2[0]
#%
#ntg2=ntg2.reset_index(drop=True)
#ntg2=ntg2.sort_index()
#%This automatic index sorting in this package was a life saver today for me!
#http://www.datasciencemadesimple.com/sort-the-dataframe-in-python-pandas-by-index/
#% However some of the pdfs where still mixed..
#%
new=[]
for xx in np.unique(ntg2.index):
    #%
#    new=[]
    ltt=ntg2.sort_index()[xx]
    if len(ltt)<49:
        u=list(ltt)
        new.append(pd.DataFrame(list(np.sort(u))))
    elif len(ltt)>49:
#        print(xx)
        ltt=pd.DataFrame([ltt]) #note all the brackets..
        new.append(ltt)
       
    #%
#https://www.afternerd.com/blog/python-sort-list/
ntg4=pd.concat(new, axis=0)
#ntg4=ntg4.reset_index(drop=True)
#%
tot_count.index=nn2
ntg4.index=nn2
#%
ntg4=pd.DataFrame(ntg4[0])
tot_count['Link to PDF of Reviewer']=ntg4 #.loc[0:329,:]
#%
#%https://cmdlinetips.com/2018/03/how-to-change-column-names-and-row-indexes-in-pandas/
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
#% What is needed from BMC (in relatively) right order:
tot_count["Reviewer's Title"]='nan' #if something is not available, mark it with 'nan'
tot_count["Reviewer's Institution"]='nan' #if something is not available..
tot_counta=[]
tot_counta=['Journal Name','Title of Article', \
               'Writers of Article', \
               'Date of Publication',\
               'Link to Publication', \
               'Reviewer Name', \
               'Review Word Count', \
               'Reviewing Date', \
               "Reviewer's Title", \
               "Reviewer's Institution", \
               'Link to All Reviews',
               'Link to PDF of Reviewer','Attachments', 'Page Count']
dfa = tot_count[tot_counta]
#%If something/some review clearly wrong, e.g. here it is completely missing:
#dfa=dfa[dfa['Reviewer Name']!='Benjamin D Horn']
#%
dfa.to_csv('BMC2018_all_available_ok_tikka12620.csv',index=False)
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
