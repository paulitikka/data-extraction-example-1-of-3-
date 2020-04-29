# -*- coding: utf-8 -*-
"""
Created on Wed 4 29 13:00

@author: pauli
"""
# Task 1.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 2019 and January 14 2020, and use also google searches: 

#(1) The quality of preventive care for pre-school aged children in Australian general practice
#(2) Louise K. Willes
#(3) 6.12.2019
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
#%%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
#For 2020..   (check th number of these..) 
urln_all='https://bmcmedicine.biomedcentral.com/articles?query=&volume=18&searchType=&tab=keyword'
urln_all2='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=18&page=2'
#urln_all3='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=18&page=3'
#urln_all4='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=18&page=4'
#urln_all5='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=18&page=5'
#urln_all6='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=13&page=6'
#urln_all7='https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=13&page=7'
#%Here all combined..
utot=[urln_all, urln_all2]#, urln_all3, urln_all4, urln_all5]#, urln_all6, urln_all7]
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
        print(i-2)  #this is ok    
thelistn=pd.DataFrame(mylistn)
thelistn=thelistn.ix[inda]    
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
        print(i)  #this is ok
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
        print(i)  #this is ok
download_url=download_url.drop(download_url.index[inda],axis=0) 
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
download_url=download_url.drop_duplicates() #the number is 227, while yesterday it was 226...
#%
all_urls = []
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
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
        all_spans2 =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
        date=all_spans2[0].text
    else:
        date.append([i])
    if driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")!=[]:
        au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
        authors=au.text
    elif driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")==[]:
        authors.append([i])
    elif len(driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']"))>1:
        au =driver.find_element_by_xpath("//ul[@class='c-author-list js-etal-collapsed']")
        authors=au[0].text
    else:
        authors.append([i])
    
    if driver.find_element_by_xpath("//h1[@class='c-article-title u-h1']")!=[]:
        tita =driver.find_element_by_xpath("//h1[@class='c-article-title u-h1']")
        title=tita.text
    elif driver.find_element_by_xpath("//h1[@class='c-article-title u-h1']")==[]:
        title.append([i])
    elif len(driver.find_element_by_xpath("//h1[@class='c-article-title u-h1']"))>1:
        tita =driver.find_element_by_xpath("//h1[@class='c-article-title u-h1']")
        title=tita[0].text
    else:
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
#dat=pd.DataFrame(datee_aut2)
#dat.to_csv('dates_authors_titles_BMC2014_tikka27420.csv') #you can use this as datee_aut2 in future  
#datee_aut2=[]
#datee_aut2=pd.read_csv("dates_authors_titles_BMC2018_tikka22420.csv")
#datee_aut2=da_au.iloc[:,1:4] #there was an extrac column   
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
#da_au.to_csv('dates and authors_BMC2019_tikka15420.csv')
##%% Loading:
#da_au=[]
#da_au=pd.read_csv("dates and authors_BMC2019_tikka15420.csv")
#da_au=da_au.iloc[:,1:4] #there was an extrac column
#%This loop seem to be working below (24.1.2020), This takes 10 min, before enter, check if you already have what you need
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
        match = re.search(r'Report_V', str)#in year 2014 this changes to V1 (or V0?), 2006 this changes to V2
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
#linkaase.to_csv('links_BMC2019_tikka17420.csv')   
#indaase=pd.DataFrame(indaas)
#indaase.to_csv('indeces_BMC2019_tikka17420.csv')
#linkaas=[]
#linkaas=pd.read_csv("links_BMC2019_tikka17420.csv")
#indaas=[]
#indaas=pd.read_csv("indeces_BMC2019_tikka17420.csv") 
##%% Loading:
#da_au=[]
#da_au=pd.read_csv("dates and authors_BMC2019_tikka15420.csv")
#da_au=da_au.iloc[:,1:4] #there was an extrac column 
#% This is why I like to be an engineer:
#%Let's take all the correct links first:
correct=[]
for i in range(len(linkaas)):
    correct.append(linkaas[i].ix[indaas[i],0])  
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
naps_tot=naps00+naps11
#%This is one of the time consuming internet extraction steps that needs to be done separately:
#One needs to get the right order of pdfs/words already here, 
# note the way the pdfs have been named:
#o=[]
#i=0
#for i in range(len(naps_tot)):
#    o.append(np.str(naps_tot[i][1]))
#    urllib.request.urlretrieve(naps_tot[i][0], \
#                               filename='C:\\python\\BMC2020\\' +o[i]+' '+naps_tot[i][0][-37:])  
#https://www.digitalocean.com/community/tutorials/how-to-convert-data-types-in-python-3  
#%There are two ways to do this. Either converge all the files as one, or import them separately as a big pands frame.
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
directory="C:\python\BMC2020\*.docx"
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
def words2(df):
    #%
#    df2=df[143]
    io=[]
    xx=[]
    
    for i in range(0, len(df)):
        str = (df.iloc[i])
        match1 = re.search(r'Reviewer\'s report:', str)
        match2 = re.search(r'Are the methods appropriate and well described?', str)
        match3 = re.search(r'https://', str)
        match4 = re.search(r'Does the work include the necessary controls?', str)
        match5 = re.search(r'Are the conclusions drawn adequately supported by the data shown?', str)
        match6 = re.search(r'Are you able to assess any statistics in the \
                      manuscript or would you recommend an additional statistical review?', str)
        match7 = re.search(r'I am able to assess the statistics', str)
        match8 = re.search(r'Quality of written English', str)
        match8b = re.search(r'Acceptable', str)
        match9 = re.search(r'Declaration of competing interests', str)
        match10 = re.search(r'I declare that I have no competing interests.', str)  
        if match1:
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
        elif match9:
            io.append(i)
        elif match10:
            io.append(i)
    io.append(len(df))
            #%
    for i in range(0,len(io)):
        if io[i]>100000:
            io[i]=io[i]/100000
    dx= [0]
    if len(io)<2:
        io.insert(0,1)
#    https://stackoverflow.com/questions/3525953/check-if-all-values-of-iterable-are-zero
    #%
    for i in range(0,len(io)):
        if isinstance(io[i], float):
           dx.append(io[i])
           #%
    io3=[]
    for i in range(len(io)):
        if not isinstance(io[i], float):
           io3.append(io[i])
     #%
    io2=[] 
    io2=list(tuple(range(io3[0]+1, io3[1])))
#%https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/    
    res=[]
#https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
#'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
    for i in io2:
        res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', df.iloc[i]))))
#%
    return  np.sum(res)

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
          
df=[]
for i in range(len(list4)):
    df.append(pd.DataFrame(list4[i])) 
#%
for i in range(len(df)):
    df[i]=df[i].ix[:,0]  
        #%
count=[]
ff=[]
count1=[]
count2=[]
count3=[]
counta=[]  
for i in range(len(df)):
    count.append(words2(df[i])) #Yes!! Got it!!
    count1.append(df[i][1])
    count2.append(df[i][2])
    count3.append(df[i][3])
    counta.append(df[i][1:5])
#%Because of these dependencies, you need to do these phases one-by-one
#Title, name, date:
date=[]
name=[]
i=0
j=0
for i in range(len(counta)):
    for j in range(0,len(counta[i])):#check indeces..
        if 'Version:' in counta[i].iloc[j]:
            if len(counta[i].iloc[j].split("Date:"))>1:
                date.append(counta[i].iloc[j].split("Date:")[1].split(" Reviewer:")[0])
            elif len(counta[i].iloc[j].split("Date:"))==1:
                date.append(counta[i].iloc[j].split("Date:"))
            else:
                date.append([])                    
        else:
            pass
        if 'Reviewer:' in counta[i].iloc[j]:
            if len(counta[i].iloc[j].split("Reviewer:"))>1:
                name.append(counta[i].iloc[j].split("Reviewer:")[1])
            elif len(counta[i].iloc[j].split("Reviewer:"))==1:
                name.append(counta[i].iloc[j].split("Reviewer:"))
            else:
                name.append([])
        else:
            pass
for i in range(len(name)):
    if " Reviewer" in name[i]: #huomaa heittomerkki
        name[i]=name[i].split(" Reviewer")[0]
title_ok=[]
for i in range(len(count)):
    if "Title:" in count1[i]: #huomaa heittomerkki
        title_ok.append(count1[i].split("Title:")[1])
    else:
        title_ok.append('nan')        
#Dropping extra lines
tok2=[]
for i in range(len(title_ok)):
    tok2.append(title_ok[i][1:(len(title_ok[i])-1)])
    #%
name2=[]
for i in range(len(name)):
    name2.append(name[i][1:(len(name[i])-1)])
    #%
date2=[]
for i in range(len(date)):
    date2.append(date[i][1:(len(date[i]))])
#%There could be better solution suggestion than this indexing:
#https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
#%To get the right columns one has to exercise a bit:
ana=[]
for i in range(len(nn2)):
    for j in range(len(auxif2)): 
        if nn2[i]==auxif2.index[j]: 
            #designation is in the first column
            ana.append(auxif2.iloc[j,:])
pana=pd.DataFrame(ana)
panax=pana.reset_index(drop=True)
#% Finally save the data:
tot_count=[]
count_ok=pd.DataFrame(count) 
title_ok2=pd.DataFrame(tok2)     
date_ok=pd.DataFrame(date2)
name_ok=pd.DataFrame(name2)         
#%Muutetaan naps_tot dataframeks:
frames = [count_ok, title_ok2, name_ok, date_ok, panax]
tot_count = pd.concat(frames, axis=1) #note the axis! and drop indeces..
#%it worked, yei!! :)
tot_count.columns = ['Review Word Count', "Article's Title", \
   'Reviewer Name', 'Reviewing Date', \
   'Date of Publication','Writers of Article','Title of Article', \
   'Link to All Reviews', 'Link to Publication']# 'Link to PDFs']
tot_count['Journal Name']='BMC Medicine'
#%IF indeces too small or litte, you may need to do...
#tot_count=tot_count.iloc[0:329,:]
#%The form of pdfs are like..
#tot_count['Link to PDFs']=ntg.iloc[xxx,0]
#xxx=ntg.iloc[[22,44,...],0]
ntg=pd.DataFrame(naps_tot) 
ntg2=ntg
ntg2.index=ntg.iloc[:,1]
ntg2=ntg2[0]
ntg2=ntg2.sort_index()
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
        ltt=pd.DataFrame([ltt]) #note all the brackets..
        new.append(ltt)
        
    #%
#https://www.afternerd.com/blog/python-sort-list/
ntg4=pd.concat(new, axis=0)
#%
tot_count.index=nn2
ntg4.index=nn2
ntg4=pd.DataFrame(ntg4[0])
tot_count['Link to PDF of Reviewer']=ntg4
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
               'Link to PDF of Reviewer']
df = tot_count[tot_counta]
#%
df.to_csv('BMC2020_all_available_ok_tikka28420.csv',index=False)
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
