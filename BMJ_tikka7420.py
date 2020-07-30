# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:16:40 2018

@author: pauli
"""
# Task 1.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 20XX and January 14 20(XX+1),

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
import datetime
import time
from selenium import webdriver  # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import string
#%Loading list of lists accumulated from previous codings, especially problematic: 'part_list'
#totala=[]
#totala=pd.read_csv("all_categores_2018_23620_v1.csv") #this you need to load with tnon, see above
##%You need to do this, if you want to load as a list again:
#totala=totala.iloc[:,1:]
#totala=totala.values.tolist()
#taxi=[]
#for i in range(len(totala)): 
#    taxi.append([x for x in totala[i] if x == x])
#dtok=[]
#part_list=taxi 
#%
#Or Check tnon below for loading..
#part_list=[]
#total=pd.read_csv("all_categores_2018_23620_v1.csv")
##dates=list(dates.ix[:,1]) #or see above
##%You need to do this (fore each possibly), 
## if you want to load as a list again, use similar procedure in sim. cases:
##total=[]
#total=total.iloc[:,1:]
#total=total.values.tolist()
#tnon=[[] for i in range(50)]
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
###            https://stackoverflow.com/questions/10037742/replace-part-of-a-string-in-python
###            https://stackoverflow.com/questions/5387208/how-to-convert-a-string-to-a-list-in-python/5387227
###%e.g. important for loading:
#part_list=tnon 
#%More ammends:
#for i in range(len(part_list)):
#    if len(part_list[i][1])<len(part_list[i][0]):
#        part_list[i][1].append(part_list[i][1][0])
#%And even more, new one:
#https://stackoverflow.com/questions/19334374/python-converting-a-string-of-numbers-into-a-list-of-int
#xaa=[int(s) for s in part_list[0][6][0].split(',')]
#for i in range(len(part_list)):
#    part_list[i][6]=([int(s) for s in part_list[i][6][0].split(',')])        
#partlist2=[[] for i in range(49)]
##partlist2=part_list
##%%How to resume the list from list of lists (instead of list of strings)
#for i in range(len(partlist2)):
#    partlist2[i][5]=tn3[i]
#part_list=part_list[0:49]  
#%
#%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
#%Let's try to get the first pdf automatically for BMJ, or use the below?, use the below if you can:
#utest='https://www.bmj.com/archive/online/2018'
#I need a list of the kind:
u1='https://bmj.com/archive/online/2018/'
#%Or more easily with..
soupn1=[]
responsen1=[]
one_a_tagn1=[]
responsen1=requests.get(u1)
soupn1=BeautifulSoup(responsen1.text, 'html.parser')
one_a_tagn1=soupn1.findAll('a') #ok
#%
ax=[]
for i in range(len(one_a_tagn1)):
    if str('href') in str(one_a_tagn1[i]):     
        if '/archive/online/' in str(one_a_tagn1[i]['href']):
            ax.append(one_a_tagn1[i]['href'][-5:])
#%Should the ax have values not ok:
ax=np.delete(ax, [0,1]).tolist()
ax.sort()
#%
utot=[]
for i in range(len(ax)):
    utot.append(u1+ax[i])
#%Should ax have less values than needed:
#https://stackoverflow.com/questions/21939652/insert-at-first-position-of-a-list-in-python
#utot.insert(0,'https://www.bmj.com/archive/online/2018/12-31')    
soupn=[]
responsen=[]
one_a_tagn=[]
for i in range(0,len(utot)):
    responsen.append(requests.get(utot[i]))
    soupn.append(BeautifulSoup(responsen[i].text, 'html.parser'))
    one_a_tagn.append(soupn[i].findAll('a')) #ok
    #%
nn=[]    
nt=[]
for j in range(len(soupn)):
    for i in range(len(soupn[j].findAll('h3'))):
        if soupn[j].findAll("h3")[i].string=='Research':
            nn.append(j)
        elif soupn[j].findAll("h3")[i].string=='News':
            nt.append([j,i])
#          https://stackoverflow.com/questions/22003302/beautiful-soup-just-get-the-value-inside-the-tag
            #%
test_list = list(range(0, 52))    
popia=list(set(test_list).difference(nn))
#%I should find the indeces of the missing four..
#https://stackoverflow.com/questions/497426/deleting-multiple-elements-from-a-list
#utot2=np.delete(utot, popia).tolist()
utot2=list(np.sort(utot)) #2018 required this solution
#%For saving and loading:

utot22=pd.DataFrame(utot2)
utot22.to_csv('weekly_bmj2018_links_tikka23620.csv')
#utot2=pd.DataFrame(utot)
#utot2.to_csv('weekly_bmj2018_links_tikka23620.csv')
#utot2=pd.read_csv("weekly_bmj2018_links_tikka23620.csv")
#utot2=list(utot2.ix[:,1])
#%Ok so far..
##Crucial info:    
##https://sqa.stackexchange.com/questions/35338/fetch-all-the-links-on-a-page-that-are-within-the-same-class    
##https://kite.com/python/answers/how-to-remove-specific-characters-from-a-string-in-python    
#%Part one:
all_urls = []
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
#%Ok, eli tässä on jo melkein kaikki metadata.. dates:
def date(url=utot2[0]):
    driver.get(url)
    all_spans2 = driver.find_elements_by_xpath("//ul[@id='research']/li/div/div/div/\
    span[@class='highwire-cite-metadata-date highwire-cite-metadata']")
    #Crucial info:    
    #https://sqa.stackexchange.com/questions/35338/fetch-all-the-links-on-a-page-that-are-within-the-same-class    
    as2=[]
    for i in range(len(all_spans2)):
        as2.append(all_spans2[i].text)
    as2=as2[1:len(as2):2]
    for i in range(len(as2)):
        a_string = as2[i]
        a_string = a_string.replace("(Published ", "")
        a_string = a_string.replace(")", "")
        as2[i]=a_string
    return as2
#https://kite.com/python/answers/how-to-remove-specific-characters-from-a-string-in-python  
#as21=date(url=utot2[0])
#%It was just two separate functions that I needed:
def date2(utot2):
    tn=[]
    for i in range(len(utot2)):
        tn.append(date(url=utot2[i]))
    return tn
#%This worked, and was relatively fast:
dates=date2(utot2)        
#%Links
def links(url=utot2[0]):
    driver.get(url)
    all_spans = driver.find_elements_by_xpath("//ul[@id='research']/li/div/div")
    spana3=[]
    for span in all_spans:
        spana3.append(span.find_element_by_css_selector('a').get_attribute('href'))     
#%The names of the article:
    all_spans3 = driver.find_elements_by_xpath("//ul[@id='research']/li/div/div")
    as3=[]
    for i in range(len(all_spans3)):
        as3.append(all_spans3[i].text) #here are the names..
    return spana3, as3
#%Test:
#sana, asu=links(url=utot2[0]) 
#%This worked here as well:
def links2(utot2):
    tn=[]
    for i in range(len(utot2)):
        tn.append(links(url=utot2[i]))
    return tn
#%This worked, and was relatiwely fast:
links=links2(utot2)
#%
nam=[]
for i in range(len(links)):
    nam.append(links[i][1])
names=[]
for i in range(len(nam)):    
    names.append([x for x in nam[i] if str(x) != 'nan']) 
#%Now I need to append links' 'spana' to peer-loop.. 
tot=[]
for i in range(len(links)):
    tot.append(links[i][0])
    #%
total=[]
for i in range(len(tot)):    
    total.append([x for x in tot[i] if str(x) != 'nan'])    
#%For saving and loading
datesa=pd.DataFrame(dates)
datesa.to_csv('all_dates_2018_23620.csv')
##%Should you need to load:
#dates=pd.read_csv("all_dates_2018_27420.csv")
#links=pd.read_csv("all_links_2018_27420.csv")
#namesa=pd.read_csv("all_names_2018_27420.csv")
# these files are either at: C:\Users\pauli or C:\python
#%For saving and loading:
linksa=pd.DataFrame(links)
linksa.to_csv('all_links_2018_23620.csv')
#%Should you need to load:
#links=list(links.ix[:,1]) #or see above
#%Saving
namesa=pd.DataFrame(names)
namesa.to_csv('all_names_2018_23620.csv')
#names=list(namesa.ix[:,1]) #or see above
#%The names of the articles:
totali=pd.DataFrame(total)
totali.to_csv('all_total_BMJ_links_2018_23620.csv')
#%I am guess that I need similarly 'too loops' to get this solved.
#The first:
def peer_loop(total):
    #%
    n=0
    spana3=[]
    spana3=total
    pura=[]
    for i in range(len(spana3)):
        res = requests.get(spana3[i])
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True) 
        text=pd.DataFrame(text) #to open text is to kill the kernel
        a=[]
        b=[]
        for i in range(len(text)):
            if 'Peer review' in text.loc[i,0]:
                a.append(i)
            if 'Abstract' in text.loc[i,0]:
               b.append(i)
        if len(a)!=0:
            cur=text.loc[a[0]:b[0],0]
            cura=list(cur)
            ii=[]
            pii=[]
            tii=[]
            noo=[]
            for i in range(len(cura)):
                if 'Peer review' in cura[i]:
                    ii.append(i)
                if '\n' in cura[i]:
                    pii.append(i)
                if len(cura[i])<4:
                    tii.append(i)
            nii=[ii,pii,tii]
            flat_list = [item for sublist in nii for item in sublist]
            flat_list=list(np.unique(flat_list))
            for i in sorted(flat_list, reverse=True):
                del cura[i]
            nop=[]
            for i in range(len(cura)):
                if 'University' in cura[i]:
                    nop.append(i)
                if 'Instit' in cura[i]:
                    nop.append(i)
                if 'Harvard ' in cura[i]:
                    nop.append(i)
                if 'Correspondence' in cura[i]:
                    nop.append(i)
            if nop!=[]:
                cura=cura[0:nop[0]]
            else:
                cura=cura[0:-1]
                
            for i in range(len(cura)):
                if len(cura[i].split(', '))>1:
                    cura[i]=cura[i].split(', ')[1]
            cura=cura[::2]
            pura.append(cura)
        else:
            pass
#            pura('nan')
    #%
    return pura
#%Peer loop for the peer pdf:
#%First the peer links:
#(Why the below procedure changes totol to total2 by-fly as well, not needed?)  
#%
total2=total
#%
total3=total2
for i in range(len(total3)):
    for j in range(len(total3[i])):
        total3[i][j]=total3[i][j]+'/peer-review'  
#%Reset the normal links:
total=[]
for i in range(len(tot)):    
    total.append([x for x in tot[i] if str(x) != 'nan'])    
#%Then the function:
def peer_loop3(total2): 
    #%
    n=0
    spana3=[]
    soupn1=[]
    responsen1=[]
    one_a_tagn1=[]
    spana3=total2
    pdf=[]
    resp=[]
    soup=[]
    link=[]
    for n in range(len(spana3)):
            #                https://docs.python.org/3/tutorial/errors.html
            try:
                resp = urllib.request.urlopen(spana3[n])
                soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
                alepa=[]
                for link in soup.find_all('a', href=True):
                    alepa.append(link['href'])
        
                p=[]
                pe=[]
                pen=[]
                for i in range(len(alepa)):
                    arr = ['First', 'decision']
                    arr2 = ['first', 'decision', 'Letter', 'Letter', 'First', 'Decision']
                    arr3=['Original', 'original', 'Response', 'response', 'Article']
                    str = alepa[i]
                    if all(c in str for c in arr):
                        p.append(i)
                    if any(c in str for c in arr2):
                        pe.append(i)
                    if any(c in str for c in arr3):
                        pen.append(i)
                if pen!=[]:    
                    if p!=[]:
                        pdf.append(alepa[p[0]])
                    elif pe!=[]:
                        pdf.append(alepa[pe[0]])
                    else:
                       pdf.append([])
                else:
                   pdf.append([])
            except:
                pdf.append([])
#                https://docs.python.org/3/tutorial/errors.html
            else:
                pdf.append([])
#https://www.tutorialspoint.com/How-to-check-if-multiple-strings-exist-in-another-string-in-Python
            #%this is the peer review pdf..
    return pdf
#%test..
#%tn and tn1 for the writer names and peer review links:  
tn=[]
i=0
for i in range(len(total)):
    tn.append(peer_loop(total[i]))
#%tn You need to do the transformation below to have correct names for each article in right form (i.e. non-lst):
#But this work only for the tnx data from previous loop
for i in range(len(tn)): 
    for j in range(len(tn[i])):
        tn[i][j]=', '.join(tn[i][j])
 #%
tna=pd.DataFrame(tn)
tna.to_csv('writers_BMJ_2018_23620.csv')

#%Depending what form you get the data saved, you may need something like the above to load it (i.e. tnon)..
#%These loops are relatively time consuming (tn, and tn1, around 15min/each so better save..)
tn1=[]
i=0
for i in range(len(total2)):
    tn1.append(peer_loop3(total2[i])) #if you go just numbers, while loop is also possible
    
#%Again for loading and saving:
tnn=pd.DataFrame(tn1)
tnn.to_csv('all_total_pdf_links_2018_23620.csv')
#%tn2=pd.DataFrame(tn1)
#tn2.to_csv('all_total_pdf_links_2018_23620.csv')   
tn3=[]
for i in range(len(tn1)):
     tn3.append(tn1[i][::2])
for i in range(len(tn3)): 
    for j in range(len(tn3[i])):
        if tn3[i][j]==[]: #this is sometimes just brackets, i.e. [], and sometimes brackets with '', i.e. '[]'
            tn3[i][j]='nan'
#%
#%Again for loading and saving:
tnn=pd.DataFrame(tn3)
tnn.to_csv('all_totalok_pdf_links_2018_23620.csv')    
   #%Calculating the number of pages in the pdf.. needed?
   #Check the ranges, also for the part list
import PyPDF2, io, requests
page_count=[[] for i in range(len(tn3))]
for i in range(len(tn3)):
    for j in range(len(tn3[i])):
        if tn3[i][j]!='nan':
            if 'www.bmj.com/sites/default/files/' in tn3[i][j]:
                response = requests.get(tn3[i][j])
                pdf_file = io.BytesIO(response.content) # response being a requests Response object
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                num_pages = pdf_reader.numPages
                page_count[i].append(num_pages)
            elif 'www.bmj.com/sites/default/files/' not in tn3[i][j]:
                page_count[i].append(0)
        elif tn3[i][j]=='nan':
            page_count[i].append(0)
#%Again for loading and saving:
tnz=pd.DataFrame(page_count)
tnz.to_csv('page_count_2018_23620.csv')
#%Now I need to gather the data for each article (one row):
part_list=[]
#%Some info:
#https://martin-thoma.com/scraping-with-selenium/ #This should be good
#https://www.reddit.com/r/learnpython/comments/6bt8g2/how_can_i_essentially_click_a_button_on_a_webpage/
#https://stackoverflow.com/questions/54862426/python-selenium-get-href-value/54862612
#%And the part list (for all weeks):
for i in range(len(total)):
    part_list.append([tn[i], dates[i], names[i], total[i], total2[i], tn3[i], page_count[i]])
#https://www.journaldev.com/23674/python-remove-character-from-string
#%I/we may need to do a 20 page +if there is a writers name in the review cut of code..(12.5.20)
#%And then all the weeks would be something like: for loading and saving:
tnx=pd.DataFrame(part_list)
tnx.to_csv('all_categores_2018_23620_v1.csv') #ok at the moment (13.5.20)
#%https://stackoverflow.com/questions/26666919/add-column-in-dataframe-from-list/38490727      
#CHECK the RANGE, e.g. 49,50,51, 21? 
dt=[]
dt=pd.concat([pd.DataFrame(part_list[i][0], columns=['Writers of Article']) for i in range(len(total))], ignore_index=True)
#If you load part_list, you need the brackets []
#%dt=dt.drop([3, 4]) #if something is not ok
#dt=dt.reset_index(drop=True)
#%Part list may require [] brackests if it is just one string variable
dt1=[]
dt1=pd.concat([pd.DataFrame(part_list[i][1], columns=['Date of Publication'])\
               for i in range(len(total))], ignore_index=True)
dt2=[]
dt2=pd.concat([pd.DataFrame(part_list[i][2], columns=['Title of Article'])\
               for i in range(len(total))], ignore_index=True)
dt3=[]
dt3=pd.concat([pd.DataFrame(part_list[i][3], columns=['Link to Publication']) for i in range(len(total))], ignore_index=True)
dt33=[]
dt33=pd.concat([pd.DataFrame(part_list[i][4], columns=['Link to All Reviews']) for i in range(len(total))], ignore_index=True)
dt4=[]
dt4=pd.concat([pd.DataFrame(part_list[i][5], columns=['Link to PDF of Review']) for i in range(len(total))], ignore_index=True)
dt5=[]
dt5=pd.concat([pd.DataFrame(part_list[i][6], columns=['Page Count']) for i in range(len(total))], ignore_index=True)

#%Check the range
tot_list=[]
final_matrix=[]
tot_list = pd.DataFrame(index=range(0,len(dt)),columns = ['Writers of Article', 'Date of Publication', \
                        'Title of Article', 'Link to Publication', 'Link to PDF of Review'])  
tot_list['Writers of Article'] = dt
tot_list['Date of Publication'] = dt1
tot_list['Title of Article'] = dt2
tot_list['Link to Publication'] = dt3
tot_list['Link to All Reviews'] = dt33
tot_list['Link to PDF of Review'] = dt4
tot_list['Page Count'] = dt5
final_matrix=tot_list
#%Convert empty list to string:
final_matrix=final_matrix[final_matrix['Link to PDF of Review'] != 'nan']
#%If there are some bougus links take them out with this or other way:
final_matrix=final_matrix[final_matrix['Page Count'] !=0]
#final_matrix=final_matrix[final_matrix['Page Count'] < 23]
#https://stackoverflow.com/questions/34162625/remove-rows-with-empty-lists-from-pandas-data-frame
#next find out the NA etc values in final matrix
#final_matrix=final_matrix.reset_index()

#%For saving and loading:
#tnp=pd.DataFrame(final_matrix)
#tnp.to_csv('all_for_bmj_review2018_26520tikka.csv') #one needs to be carefull with these dates when loading
#%For loading:
#final_matrix=[]
#final_matrix=pd.read_csv("all_for_bmj_review2018_25520tikka.csv")
#final_matrix=final_matrix.ix[:,1:]
#final_matrix=final_matrix[final_matrix['Link to PDF of Review'] != 'nan']
#final_matrix=final_matrix[final_matrix['Page Count'] < 23]
#%Here is how you get the data from pdf:
#https://stackoverflow.com/questions/45470964/python-extracting-text-from-webpage-pdf
#% This is how you import the pdfs from links:
#https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
#https://www.geeksforgeeks.org/how-to-get-rows-index-names-in-pandas-dataframe/    
#import urllib.request
#global str
#del str #do not use str as a name of a variable of function
#%https://stackoverflow.com/questions/6039605/typeerror-str-object-is-not-callable-python
#url=[]
x=[]
xa=[]
xu=[]
for i in range(len(final_matrix)):
#    if final_matrix['Link to PDF of Review'][i] !='nan': #If you have removed nans etc., you do not need this
#    url=final_matrix['Link to PDF of Review'][list(final_matrix.index)[i]] #note the index is not i, but list..
    x=list(final_matrix.index)[i]
    xu=str(x)
    xa.append(x)
#    urllib.request.urlretrieve(url, filename='C:\\python\\BMJ2018\\'+xu+'peer.pdf') #check..

#%Now I need to do I loop for all files, and save the results
directory="C:\python\BMJ2018\*.docx"
import glob

dataframes = []
all_files2=(glob.glob(directory))

desig=[]
import re
for i in range(len(all_files2)):
    desig.append(re.findall(r'\d+', all_files2[i])) #these are final_matrix equivalents:
#%Create the list for the DataFrames:
#% This is how I import docx files:
def totis(x=all_files2[22]):    #check the length of all_files2 before giving value to it e.g. [122]
    import docx2txt
    result=[]
#    x=all_files2[122]
    result = docx2txt.process(x)
    #%This worked:
    #https://stackoverflow.com/questions/13169725/how-to-convert-a-string-that-has-newline-characters-in-it-into-a-list-in-python
    r2=[]
    r2=result.splitlines()
    #https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
    list2 =[]
    list2 = [e for e in r2 if e] 
    list2=[x.split("\t") for x in list2]
    list2 = [e for e in list2 if e]
    #% This is how you delete lists:
    #https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/
    for i in range(len(list2)):
        if list2[i][0] == '':
            del list2[i][0]
    for i in range(len(list2)):
        if list2[i][0] == '':
            del list2[i][0]
    #% The pandas are better to handle data (in functions) than list of lists (according to my experience):
    df=pd.DataFrame(list2)
    return df

df_tot=[]
for i in range(len(all_files2)):
    df_tot.append(totis(x=all_files2[i]))
#%You may need to manually delet an index for 2018:
#df_tot.index=..click..[57]
#%
#%With this you get the extra columns away by joining the cells that do that
# #https://stackoverflow.com/questions/10880813/typeerror-sequence-item-0-expected-string-int-found
#%Now you just need the first column from every dataframe
dtok=[]            
for i in range(len(df_tot)):
    dtok.append(df_tot[i].loc[:,0])          
#%For saving and loading:
    #%
#dtok2=pd.DataFrame(dtok)
#dtok2.to_csv('essential_for_bmj_2018_review_23620tikka.csv') #it is better to start here than partlist, 
#if your word count function needs modification due data: 
    #%
#l=[]
#for i in range(len(desig)):
#    if int(desig[i][1])==20:
#        l.append([i,desig[i][1]])
##        #%%
##        Godfrey P. Oakley, Jr. 
#%
#l=[]
#for i in range(len(dtok)):
#    for j in range(len(dtok[i])):
#        if "Monica Bertoia" in dtok[i][j]:
#            l.append(i)
#            print(i)
#%%Once you have the dataframe well extracted, the below function it should work:
#Check the BMJ extras file (25.5.2018) for testing if needed
def words2(dx=dtok[0],xx=int(desig[0][1])): #the first zero in 'desig[0][0]' is the variable
    #%Check the short reviews (Tikka 21520)
    start=[]
    end=[]
    real_start=[] 
    rt2=[]
    real_end=[] 
    re2=[]
    res=[]
    tot=[]
    sup=[]
    supa=[]
    supas=[]
    supass=[]
    s4=[]
    sx=[]
    ssx=[]
    ss=[]
    ssy=[]
    ssa=[]
    ssn=[]
    Article=[]
#    dx=dtok[120]
#    xx=int(desig[120][1])
    nana=[]
    panaa=[]
    separate=[]
#    oh=[]
    email=['Please see the reviewer\'s report', 'Please see the attahcment',\
           'Please see the attachment',\
           'My comments are in a separate file','my report is added as a word document',\
           'See uploaded review comments', 'sent via email']
    for i in range(0, len(dx)):
        stra = str(dx.iloc[i])
        match1 = bool(re.search(r'Reviewer: ', stra)) #I need to change these values..
        match1a = bool(re.search(r'Reviewer:', stra)) #I need to change these values..

        match2 = bool(re.search(r'Recommendation:', stra))
        match2n= bool(re.search(r'Comments:', stra))
        match2na= bool(re.search(r'Comments from Reviewers', stra))
        
        #I need to change these values..
        match2a = bool(re.search(r'Detailed comments from the meeting:', stra)) #I need to change these values..
        match2b = bool(re.search(r'Our statistician made the following comments', stra)) 
        match2c = bool(re.search(r'Reviewer', stra)) #I need to change these values..  
        match3  = bool(re.search(r'Additional Questions:', stra))
        match4  = bool(re.search(r'Please enter your name:', stra))
        mx4a   = bool(re.search(r'Institution: ', stra))
        match5 = bool(re.search(r'Information for submitting a revision', stra))
        match6 = bool(re.search(r'Funds', stra))
        
        if match1==True:
            start.append(i)
        elif match2n==True:
            if start==[]:
                start.append(i)
        elif match2na==True:
            if start==[]:
                start.append(i)
        elif match1a==True:
            if start==[]:
                start.append(i)
        elif match2c==True:
            if start==[]:
                start.append(i)
#            'Reviewer'
        elif match2==True:
            if 'Patient Reviewer' in stra:
                pass
            elif 'Patient Reviewer' not in stra:
                start.append(i)
      
        elif match2a==True:
            if start==[]:
                start.append(i)
        elif match2b==True:
            if start!=[]:
                start.append(i)
        elif 'Comments by Editorial Committee' in stra:
            if start==[]:
                nana.append(i)
        elif 'comments from reviewer' in stra:
            if start==[]:
                nana.append(i)
        elif i<int(len(dx)/10) and len(dx)>290:
            if 'Reviewer: ' in stra:
                start.append(i)
                #%
        if match3==True:
            end.append(i)
        elif match4==True:
            if end!=[]:
                end.append(i)
        elif mx4a==True:
            if end!=[]:
                end.append(i)
        elif match5==True:
            if end!=[]:
                end.append(i)

        elif 'Please enter your name:' in stra:
            if end==[]:
                panaa.append(i)
                end.append(i)
        elif 'Another editor' in stra:
            if end==[]:
                panaa.append(i)
        elif 'Yours sincerely, ' in stra:
            if end==[]:
                panaa.append(i)
                
        if match4:
            sup.append(i)
            supa.append([dx[i].split(": ")[1].split(" Job Title")[0],i])
           
        if 'Job Title:' in stra:
            ss.append(i)
            a=dx[i].split("Job Title: ")[1] ==['']
            b=dx[i].split("Job Title: ")[1] !=['']
            c=dx[i].split("Job Title")[0] !=['']
            if a:
                s4.append([dx[i+1].split(" Institution")[0],i])
            elif b or c:
                s4.append([dx[i].split("Job Title: ")[1].split(" Institution")[0],i])
        if 'Please enter your name: ' in stra:            
            if 'Job Title:' not in stra:
                sx.append(dx[i].split("Please enter your name: ")[1])
            elif 'Job Title:' in stra:
                sx.append(dx[i].split("Please enter your name: ")[1].split("Job Title")[0])
        if  "chair" in stra and i<30 and len(dx)>91 and 'Members of the committee were: ' in \
        dx[i] or "Chair" in stra and i<30 and len(dx)>91 and 'Members of the committee were: ' in dx[i]:
#            oh.append(i)
            sx.append([dx[i].split("Members of the committee were: ")[1]])
        elif "chair" in stra and i<30 and len(dx)>91 or "Chair" in stra and i<30 and len(dx)>91:
            sx.append([dx[i]])
            
#%
        if 'Institution:' in stra:
            ssx.append(dx[i].split('Institution: ')[1]) 
        if 'Job Title:' in stra:
            ssy.append(dx[i].split('Job Title: ')[1])  
        if 'Institution:' in stra:
            ssa.append([dx[i],i])
        if 'Thank you for sending us your paper. We read it with interest but I am sorry to say that' in stra:
            start.append(0)
            end.append(int(len(dx)*0.98))
        if 'entitled "' in stra:
            if i<int(len(dx)*0.2):
                Article.append((dx[i].split('entitled "')[1]).split('"')[0])
                
        for i in range(len(email)):
            if email[i] in stra:
                separate.append('attached')
           

    for i in range(len(ssa)):
        if 'Institution: ' not in ssa[i][0]:
            pass
        elif 'Institution: ' in ssa[i][0]:
            ssn.append(ssa[i])
        elif 'Institution: ' not in stra:
            ssn.append('nan')
            
    for i in range(len(ssn)):  
        if ssn[i][0].split("Institution: ")[1] ==['']:
            supass.append([ssn[i].split(' Reimbursement')[0],ssn[i][1]])
        elif ssn[i][0].split("Institution: ")[1] !=[''] or ssn[i][0].split("Institution: ")[0] !=['']:
            supass.append([ssn[i][0].split("Institution: ")[1].split(' Reimbursement')[0], ssn[i][1]])
        elif ssn[i][0].split("Institution: ")[0] ==['']:
            supass.append(['nan',ssn[i][1]])
            #%
    if len(end)>2 and len(start)>2 and end[0]>start[0] and end[0]>start[1] and abs(start[0]-start[1])>28:
        end.append(start[1])
    end=list(np.sort(end)) 
    #%
    if start==[]:
        if len(nana)!=0:
            start.append(nana[0])
        elif len(nana)==0:
            start.append(0)
    if start==[]:
        start.append(0)
    if end==[]:
#        end=start[1:]
        if len(panaa)!=0:
            if len(end)>0:
                if panaa[0]>end[0]:
                    end.append(panaa[0])
                elif panaa[0]<end[0]:
                    end.append(int(len(dx)*0.98))  
            else:
                pass
            #%
        elif len(panaa)==0:
            end.append(int(len(dx)*0.95)+1) 
            #%
    if end==[]:
        end=start[1:]
        end.append(int(len(dx)*0.98))
   
    #%breaking point for start
    i=0
    at=[]
    for i in range(len(start)):
        if abs(start[i]-start[i-1])<3 or abs(start[i]-start[i-1])<4 and len(start)>5:
            at.append(i)
            #%
    if len(start)>2:
        if at==[1, 2]:
            start=start[2:]
        elif len(at)>2 and at!=[1, 2] or len(at)<2 or len(at)==2:
            start = [j for i, j in enumerate(start) if i not in at]
    #%if end bad good breaking point for end
    i=0
    at=[]
    for i in range(len(end)):
        if len(end)!=len(start)*3:
            if abs(end[i]-end[i-1])<6 and len(end)!=len(start)*2 and abs(end[0]-end[-1])>14 and abs(np.median(end)-end[-1])>8:
                at.append(i)
#        elif len(end)==len(start)*2:
#            if abs(end[i]-end[i-1])<5 and abs(end[0]-end[-1])>14 and abs(np.median(end)-end[-1])>8:
#                at.append(i)
#            
            #%
    if len(end)>2:
        if start[0]==end[1] and (len(end)-2)==len(start) and at[0]==1:
            end=end[2:]
        else:
            end = [j for i, j in enumerate(end) if i not in at]
            #%
    if len(start)>4 and len(start)-1==len(end) and start[1]<end[0] and start[1]<29:
        start=start[1:]
        
        #%
    if len(end)>1 and len(start)>1:
        if end[-1]>160 and start[1]==end[0] and start[-1]==end[-2]:
            end[0]=int(end[0]*0.8)
            end[1]=int(end[1]*0.87)
            for i in range(2,len(end)-1):
                end[i]=int(end[i]*0.90)
        #%
    if len(end)-1==len(start) and len(start)>4 and end[-1]>end[-2] and end[-2]>start[-1]:
        end=end[0:-1]
    if len(end)+1==len(start) and len(start)>3 and start[-1]>start[-2] and start[-1]>end[-2] and abs(start[-1]-start[-2])<4:
        start=start[0:-1]
    if len(start)==len(end) and len(end)==6 and len(dx)>200 and start[1]<end[0] and start[2]<end[1] and start[-1]<end[-2] and abs(end[-1]-end[-2])<9:
        end.insert(0,start[1])
        end.pop(-1)
    #%
    
    if len(end)>3 and len(start)>1 and (len(end)-1)==len(start) and end[-2]<start[-1] and end[-3]<start[-2] and len(dx)<206 and start[0]>23 and end[0]<41:
        at=[]
        for i in range(len(end)):
            if len(end)!=len(start)*3:
                if abs(end[i]-end[i-1])<7 and len(end)!=len(start)*2 and abs(end[0]-end[-1])>14 and abs(np.median(end)-end[-1])>8:
                    at.append(i)
        end = [j for i, j in enumerate(end) if i not in at]
    #%
    if len(end)>2 and len(start)>1 and (len(end)-1)==len(start) and end[-2]<start[-1] and end[-3]<start[-2] and len(dx)>205 and start[0]>23:
        at=[]
        for i in range(len(end)):
            if len(end)!=len(start)*3:
                if abs(end[i]-end[i-1])<7 and len(end)!=len(start)*2 and abs(end[0]-end[-1])>14 and abs(np.median(end)-end[-1])>8:
                    at.append(i)
        end = [j for i, j in enumerate(end) if i not in at]
        
    if len(end)>2 and len(start)>2 and end[0]>start[2] and (len(end)-1)==len(start) and len(dx)>80 and start[0]>16:
        at=[]
        for i in range(len(end)):
            if len(end)!=len(start)*3:
                if abs(end[i]-end[i-1])<7 and len(end)!=len(start)*2 and abs(end[0]-end[-1])>14:
                    at.append(i)
        end = [j for i, j in enumerate(end) if i not in at]
        if len(sx)==len(end) and abs(start[0]-start[2])<11 and start[0]>16 and len(dx)>80 and start[-1]>60 and end[-1]>70:
            start=start[2:]
            #%
            
    if len(end)==len(start) and len(start)>2 and end[0]>start[1] and end[-2]>start[-1] \
    and end[1]>start[2] and abs(end[0]-end[1])>50 and len(dx)>180 and start[0]>10 and abs(start[0]-start[2])<45:
        end.append(start[1]-1)
        end=np.sort(end)
        end=list(end)
        #%
        if len(dx)>180 and abs(end[-1]-end[-2])<10 and end[-2]>start[-1] and abs(end[-1]-len(dx))<34:
            end.pop(-1)


            
#        end.pop(-3)
        
#% ok breaking point
#    https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index    
#%here are the exceptions
    endb=[]
    enda=[]
    endc=[]
    endd=[]
    if len(end)>4 and (len(end)-1)==len(start):
        end=end[0:-1]
        #%
    if len(start)>len(end) and end[-1]>start[-1] and abs(start[-1]-start[-2])<6 and len(end)>2:
        start=start[0:-1]
    at=[]
    if len(start)>3 and len(end)!=len(start):
        for i in range(len(start)):
            if abs(start[i]-start[i-1])<4:
                at.append(i) 
        start = [j for i, j in enumerate(start) if i not in at]
    #%
    if len(end)!=len(start):
        if len(end)==len(start)*3:
            at=[]
            for i in range(len(end)):
                if abs(end[i]-end[i-1])<5 or len(end)>len(start) and len(end)>7 and abs(end[i]-end[i-1])<7:
                    at.append(i)
                        #%
        if len(end)>2:
#            at=[]
            end = [j for i, j in enumerate(end) if i not in at]
                #%
        if len(start)==2:
            if len(end)>2 and len(end)>(len(start)*3-1):
                endc.append(end[0])
                endc.append(end[2])
                end=endc
            elif len(end)<3:
                pass
        if len(start)==4:
            if len(end)>3:
                if len(end)<=len(start)+2:
                    endd.append(end[0])
                    endd.append(end[1])
                    endd.append(end[2])
                    endd.append(end[-1])
                    end=endd
                if len(end)>len(start)+2:
                    pass
            elif len(end)<4:
                pass
            #%
    if len(end)>len(start):
        if len(start)>1 and abs(end[1]-end[0])>7:
            end=end[0:-1]
            if len(enda)>len(start):
                endb.append(enda[0])
                endb.append(enda[-1])
                end=endb
        elif len(start)==1:
            if end!=[]:
                start.append(end[0])
            else:
                start.append(int(len(dx)*0.98))
        
        else:
            pass
            #%
    if len(start)>4:        
        if end[0]-start[0]<4:
            if len(end)!=len(start):
                start=start[1:]
                end=end[1:]
     #%
    if len(end)!=len(start):
        def test(end): 
        #%     
            i=0
            au=[]
            for i in range(len(end)):
                if end[i]-end[i-1]>3:
                    au.append(end[i])
            enda=[]
            enda=end[0]
            au.insert(0,enda)
        #    https://developers.google.com/edu/python/lists
            end=au
            return end
    #% The pandas are better to handle data (in functions) than list of lists (according to my experience):
        if end!=[]:
            end=test(end)
            #%
        if len(start)>len(end) and len(end)>1 and len(start)>2 and start[1]<end[0]:
            end.append(start[1])
        end=np.sort(end)
        end=list(end)
            #%
        if len(start)!=[] and len(end)!=[] and len(end)>0:
            if len(start)>len(end) and abs(int(len(dx)*0.98)-end[-1])>4:
                end.append(int(len(dx)*0.98))
        #%
        if len(start)==5 and len(end)==4 and start[2]<end[1] and end[-1]>110 and start[0]>22:
            end.append(start[2])
        end=np.sort(end)
        end=list(end)
    #%
    if len(start)==len(end) and len(dx)>120 and len(end)>2 and end[-2]>start[-1] and start[0]>20 and abs(start[1]-end[0])<2:
        end.pop(-1)
        end.insert(-2,start[-1])
        end=np.sort(end)
        end=list(end)
        #%
        
        
        
    if len(start)>len(end):
        if len(start)!=[] and len(end)!=[] and len(end)>0 and len(start)>1:
            if end[0]==start[1] or end[0]+1==start[1] or end[0]-1==start[1] or end[0]+2==start[1] or end[0]-2==start[1]:
                start.pop(1)

    end=np.sort(end)
    end=list(end)
    
    if len(end)>5 and len(start)==len(end) and len(dx)>175 and end[0]>start[1] and end[-2]>start[-1] and end[1]>start[2] and end[2]>start[3] and abs(end[-1]-end[-2])<12:
        end.insert(0,start[1])
        end.pop(-1)
        #%
    end=np.sort(end)
    end=list(end)
    
    #%
    if len(start)>1 and len(end)>1:
        if start[1]<end[0] and len(start)>5:
            start[1]=end[0]
            start[0]=int(end[0]-2)
    if len(end)>1 and len(start)>2:
        if end[1]==start[2] and len(start)>5 and abs(start[1]-start[2])<10 and end[0]<start[2]:
            start.pop(1)
            end.pop(1)
    #%
    if len(end)<len(start):
        if len(start)!=[] and len(end)!=[] and len(end)>0 and len(start)>1:
            ex=[]
            ex=start[1]
            end.insert(0, ex)
            if end[-1]==len(dx):
                end.pop(-1)
                if sup!=[]:
                    if max(sup)<len(dx):
                        end.append(max(sup))
                    elif max(sup)==len(dx):
                        end.append(int(len(dx)*0.98))
                        
                elif sup==[]:
                    end.append(int(len(dx)*0.98))
            if len(end)<len(start):
                enda=[]
                enda=end[-1]
                e2=[]
                e2=start[1:]
                e2.append(enda)
                end=e2
                #%relatively good breaking point
    if len(end)>1 and len(start)>2 and end!=[] and start!=[]:
        if abs(end[0]-end[1])>int(end[-1]/2):
            end.append(start[2])
        if len(end)-1==len(start) and len(start)>4 and end[-2]>start[-1] and (start[1]+50)<end[1]:
            end=end[0:-1]
    if end!=[] and len(start)>3:
        if abs(end[1]-end[2])>int(end[-1]/2):
            end.append(start[3])
        if len(end)-1==len(start) and len(start)>4 and end[-2]>start[-1] and (start[1]+50)<end[1]:
            end=end[0:-1]
            #%
    if len(end)>1 and len(start)>1:
        if abs(end[-1]-end[-2])<5:
            end=end[0:-1]

    aux2=[]
    a3=[]
    i=0
    if len(start)<len(end):
        for i in range(len(end)):
            if end[i]-end[i-1]<4 and end[i]-end[i-1]>0:
                aux2.append(i-1)
    if end!=[]:
        a3.append(end[0])
    i=0

    for i in range(len(aux2)):
        if aux2[i]-aux2[i-1]>1:
            a3.append(end[aux2[i]])
    #%
    if len(start)<len(end):
        if len(start)+1==3 and abs(end[1]-end[0])<8:
            if abs(end[1]-end[0])==7:
                aq=[]
                aq.append(end[0])
                aq.append(end[-1]+1)
                end=[]
                end=aq
            else:
                aq=[]
                aq.append(end[0])
                aq.append(end[-1])
                end=[]
                end=aq
        elif len(start)>1 and abs(end[1]-end[0])>7:
            a3.insert(0, start[1])
            end=a3
        elif len(start)==1:
            a3.insert(0, start[0])
            end=[a3[1]]
        elif len(start)==0:
            end.append(int(len(dx)*0.98))
            start.append(int(len(dx)*0.05))
#%
    if len(end)!=len(start):
        if end!=[]:
            enda=[]
            enda=end[-1]
            end=start[1:]
            if sup!=[]:
                if max(sup)<len(dx):
                    end.append(max(sup))
            elif sup==[]:
                end.append(int(len(dx)*0.98))
            elif enda<int(len(dx)*0.98):
                end.append(enda)
            elif enda>int(len(dx)*0.9):
                end.append(int(len(dx)*0.98))
    #%
    peta=[]
    eta=[]
    x=[]
    if len(end)>1:
        for i in range(len(end)):
            if len(dx)>300:
                if end[i]-end[i-1]>int(len(dx)*0.5):
                    peta=i
                    for i in range(len(end)):
                        x.append(end[i]-end[i-1])
        if x!=[]:
            eta=int(np.average([np.median(x),np.max(x)/2])) 
    
            del end[peta]          
            end.insert(peta, eta)
    if len(end)==len(start):
        end=np.sort(end)
    end=list(end)
                #%
    apo=[]
    if len(start)>0:
        for i in range(len(start)):
            apo.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[start[i]])))))
            if apo[i]>3 and 'Reviewer' in dx.iloc[start[i]] and apo[i]<7 or \
            len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[start[i]].split('Reviewer')[0]))))>3:
                start[i]=start[i]+1
                #%
    if end!=[] and start!=[] and len(end)>0 and len(start)>1:
        if len(end)==len(start) and len(start)>6:
            if abs(start[0]-start[1])<3 and abs(start[1]-start[2])<5: 
                if (start[2]-start[1])<-3 and abs(start[0]-start[1])<=2:
                    ok=start[0]
                    start=start[2:]
                    start[0]=ok
#%
                if end[0]==end[1] and abs(end[2]-end[1])>12:
                    end=end[1:-1]
    if len(end)>5 and len(start)>5:
        end=np.unique(end)
        end=np.sort(end)
        end=list(end)
        start=np.unique(start)
        start=np.sort(start)
        start=list(start)
                    #%
    if start==[]:
        start.append(int(len(dx)/10))
    if end==[]:
        end.append(int(len(dx)-3))   
    def names(supass, xt='JOURNAL'):
        #%
        supass2=[]
        for i in range(len(supass)):
            supass2.append(supass[i][1])

        def common_data(list1, list2): 
            result = []  
            # traverse in the 1st list 
            for x in list1:  
                # traverse in the 2nd list 
                for y in list2:    
                    # if one common 
                    if abs(x-y)<3: 
                        result.append(x)
                          
            return result 
        #https://www.geeksforgeeks.org/python-check-two-lists-least-one-element-common/
        sn=[]
        sn=common_data(end, supass2)  
        #%These elements have 'general':
        no=list(set(end) - set(sn)) 
        #https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
        #General:
        endax1=[]
        if no!=[] or len(no)>0 and len(end)>0 or end!=0:
            for i in range(len(no)):
                endax1.append(end.index(no[i]))
                #%
        #The names    
        endax2=[]
        for i in range(len(sn)):
            endax2.append(end.index(sn[i]))
        #%
        supass3=[[]]*len(end)
        for i in range(len(endax1)):
            supass3.insert(endax1[i],xt)
        #%
        for i in range(len(endax2)):
            if len(endax2)==len(supass):
                supass3.insert(endax2[i], supass[i][0])
            elif len(endax2)>len(supass):
                supass3.append(supass[i][0])
            elif len(endax2)<len(supass):
                supass3.append(supass[i][0])
        if len(supass3)>len(end):
            supass3=supass3[0:len(end)]
            #%
        return supass3
#%
    if ssx==[]:
        Institution=   names(supass, xt='Journal Institution') 
    else:
        Institution=ssx
    #%
    if ssy==[]:
        Title=   names(s4, xt='Journal Reviewer Title')
    else:
        Title=ssy
    #%
    if sx==[]:
        Reviewer=names(supa, xt='Journal Reviewer')
    else:
        Reviewer=sx
    Article2 = []
    Article2 = Article * len(Reviewer)
    Designation=[]
    Designation = [xx] * len(Reviewer)
#%
    io2=[]
    tot=[]
    tat=[]
#    tit=[]
#    tut=[]
    ras=[]
    rus=[]
#    ris=[]
    res=[]
    if start==[]:
        start.append(int(len(dx)/10))
    if end==[]:
        end.append(int(len(dx)-3))
        #%
    for i in range(len(start)):
        res=[]
        io2=list(tuple(range(start[i], end[i])))
        #%
    #https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/     
    #https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
    #%'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
        if start[0]!=0 and end[0]<6000 and len(end)==len(start):
            for i in io2:
    #            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[i]))))) # (?<![\"=\w])(?:[^\W_]+)(?![\"=\w])
                res.append(len(dx.iloc[i].split(' ')))
                ras.append(len(re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', str(dx.iloc[i]))))
    #            rus.append(len(re.findall(r'[0-9]+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[i])))))
    #            ris.append(len(re.findall(r'(?=.*?[a-zA-Z].*?[a-zA-Z])', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[i])))))
            tot.append(np.sum(res))
            tat.append(np.sum(ras))
#        tit.append(np.sum(rus))
#        tut.append(np.sum(ris))
        elif start[0]==0 and end[0]>6000:
            tot.append(0)
            tat.append(0)
            #%
        pat=[]
        for i in range(len(tat)-1):
            pat.append(tat[i+1]-tat[i])
        pat.insert(0,tat[0])
        #%
        
        for i in range(len(pat)):
            if pat[i]>199:
                if pat[i]>422:
                    if np.median(pat)*6>int(pat[i]/4):
                        pat[i]=int(pat[i]/2)-np.median(pat)
                    elif np.median(pat)*6<int(pat[i]/4):
                        pat[i]=int(pat[i]/4)-np.median(pat)*5
                elif pat[i]<422 and pat[i]>199:
                    pat[i]=int(pat[i]/4)+np.median(pat)*5+int(np.median(pat)/2)+2
            elif pat[i]<200 and pat[i]>99 and np.max(pat)==pat[i]:
                pat[i]=np.median(pat)
            elif pat[i]<200 and pat[i]>99:
                pat[i]=int(pat[i]/3)
            elif pat[i]<100 and pat[i]>49 and np.max(pat)==pat[i]:
                pat[i]=np.median(pat)
            elif pat[i]<100 and pat[i]>49:
                pat[i]=int(pat[i]/1.5)+np.median(pat)
                #%
        for i in range(len(pat)):
            pat[i]=int(pat[i])
            
        ko=[]
        ko.append(np.median(pat))  
        po=[]
        po.append(np.min(pat))
        no=[]
        no.append(np.max(pat))
        #%
        if len(pat)>1 and len(tot)>1:
            if np.median(pat)<100:
                for i in range(len(pat)):   
                    if pat[i]>po[0]:
                        if pat[i]<no[0] and int(abs(pat[i]-ko[0]))>4:
                            pat[i]=int(pat[i]/1.8)
                        elif int(abs(pat[i]-ko[0]))<5:
                            pass
                        elif len(pat)<3 or len(pat)>6:
                            if pat[i]>365:
                                pat[i]=ko*6
    for i in range(len(pat)):
        pat[i]=int(pat[i])
            #%
#    if pat!=[] and len(pat)==len(tot):
#        for i in range(len(tot)):
#            tot[i]=tot[i]+pat[i]
            #%
    if len(Reviewer)-1==len(tot) and len(start)==len(tot):
        Reviewer=Reviewer[1:]
    elif len(Reviewer)+1==len(tot) and len(start)==len(tot):
        Reviewer.insert(0,'Members of the committee')
        
    separate2=[]
    if tot==[]:
        tot.append('rev')
    if separate!=[]:
        separate2=['no']* len(Reviewer)
        for i in range(len(Reviewer)):
            if tot[i]<21:
                for j in range(len(separate)):
                    separate2[i]=separate[j]
    elif separate==[]:
        separate=['no']* len(Reviewer)
        separate2=separate
        #%
    for i in range(len(tot)):
        tot[i]=int(tot[i])
        if pat[i]>4 and tot[i]>49 and tot[i]<3500 and pat!=[] and len(pat)==len(tot):
            if pat[i]<26:
                tot[i]=tot[i]+int(pat[i]/1.6)
            elif pat[i]>25:
                tot[i]=tot[i]+int(pat[i]/60)+18
        elif pat[i]<4 and tot[i]>39:
            tot[i]=tot[i]+pat[i]
                #%
#    for i in range(len(tot)):
#        tot[i]=int(tot[i])
#        if tot[i]>=950:
#            tot[i]=tot[i]-int(0.02*tot[i])-10
#        tot[i]>=2500 and tot[i]<3300:
#            if tot[i]==2542:
#                tot[i]=tot[i]-int(int((tot[i]/2435-1)*tot[i]))+4
#            elif tot[i]!=2542:
#                tot[i]=tot[i]-int(0.044*tot[i])+40
#        elif tot[i]>=1525 and tot[i]!=2435 and tot[i]<2500:
#            tot[i]=tot[i]-int(0.045*tot[0])+10
#        elif tot[i]>=1330 and tot[i]<1525:
#            tot[i]=tot[i]-int(0.02*tot[0])-10
#        elif tot[i]>=950 and tot[i]<1330:
#            tot[i]=tot[i]-int(0.025*tot[0])
#        elif tot[i]>3229 and tot[i]<4000:
#            tot[i]=tot[i]-int(0.03*tot[i])
            #% Members of the committee

        
        #%
    return tot, Reviewer, Title, Institution, Article2, Designation, separate2 
#%Test:
#Words, Reviewer, Title, Institution, Article2, Designation, separate=words2(dx=dtok[15],xx=int(desig[15][1]))
#%Got it, the amount of words in peer reviews about ok:
#len(dtok)
test_short=[]   
for i in range(len(dtok)): 
    test_short.append(words2(dx=dtok[i],xx=int(desig[i][1])))
    #%got some value, but checking.. now about
test_short2=[]
test_short2=test_short  
#%It was tuple list, so now I convert it to list of lists:
#https://stackoverflow.com/questions/16730339/python-add-item-to-the-tuple
tt=[]
for i in range(len(test_short2)):
    tt.append(list(test_short2[i]))
ttax=pd.DataFrame(tt)
ttax.to_csv('half of the infoos_BMJ_2018_23620_v3.csv')  
def panda(a):   
    panda1=[]
    panda1=pd.DataFrame(a, index=['Review Word Count', 'Reviewer Name', "Reviewer's Title", \
 "Reviewer's Institution", 'Article Name','Designation', 'Attachments'])
    panda1=panda1.T
    return panda1
totaali=[]
for i in range(len(tt)):
    totaali.append(panda(tt[i]))
result = pd.concat(totaali)
#%https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html 
result.fillna(value=pd.np.nan, inplace=True)
#%Replacing empty lists with nans:
result=result.mask(result.applymap(str).eq('[]'))
#%
#https://stackoverflow.com/questions/43788826/replace-empty-list-values-in-pandas-dataframe-with-nan?rq=1
#%Let's do the other way around i.e. add final_matrix to result, here are nan columns:
result['Writers of Article'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Date of Publication'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Title of Article'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Link to Publication'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Link to PDF of Review'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Link to All Reviews'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Page Count'] = pd.DataFrame(index=range(len(result)),columns=range(1))
#result['Attachments'] = pd.DataFrame(index=range(len(result)),columns=range(1))
#%Zeroing the indeces:
result=result.reset_index()
result=result.drop(columns=['index'])
result=result.replace('YYY', 'nan')
#%You may need to curate your data:
#https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-in-a-certain-column-is-nan
#%result=result.iloc[0:675,:]
result = result[result['Designation'].notna()]
#huh, now I got the designation correct in result, now need to match that to the final matrix designation
#%There must be faster ways to do this, than below, e.g. with maps or libraries etc.:
#result.applymap(lambda y: [result.applymap(lambda x: x == [])]=='nan')
#final_matrix=final_matrix.drop(columns=['Reviewer'])
for i in range(len(final_matrix)):
    for j in range(len(result)):
        if final_matrix.index.tolist()[i]==int(result['Designation'].iloc[j]):
            result['Title of Article'].iloc[j]=final_matrix['Title of Article'].iloc[i]
            result['Page Count'].iloc[j]=final_matrix['Page Count'].iloc[i]
#            result['Attachments'].iloc[j]=final_matrix['Attachments'].iloc[i]
for i in range(len(final_matrix)):
    for j in range(len(result)):
        if final_matrix.index.tolist()[i] ==result['Designation'].iloc[j]:
#            result['Title of Article'].iloc[j]=final_matrix['Title of Article'].iloc[i]
            result['Writers of Article'].iloc[j]=final_matrix['Writers of Article'].iloc[i]
            result['Date of Publication'].iloc[j]=final_matrix['Date of Publication'].iloc[i]
            result['Link to Publication'].iloc[j]=final_matrix['Link to Publication'].iloc[i]
            result['Link to All Reviews'].iloc[j]=final_matrix['Link to All Reviews'].iloc[i]
            
#%This xa maybe excessive..
for i in range(len(xa)):
    for j in range(len(result)):
        if int(xa[i]) == int(result['Designation'].iloc[j]):
            result['Link to PDF of Review'].iloc[j]=final_matrix['Link to PDF of Review'].loc[int(xa[i])]
            #note the loc in the final matrix of previous row!
            #this should come from 
#1) It seems that link to pdf is not giving all the data, the articles etc. metadata are not refering to right review..   
#%Let me first check the designation..:
result=result.drop(columns=['Designation', 'Article Name'])           
#result.rename(columns={'Article Name':'Title of Article'}, inplace=True) 
result["Journal Name"]='BMJ' #if something is not available, mark it with 'nan'
result["Reviewing Date"]='nan' #if something is not available..
#%result["Link to All Reviews"]='nan'
resulta=[]
resulta=['Journal Name','Title of Article', \
               'Writers of Article', \
               'Date of Publication',\
               'Link to Publication', \
               'Reviewer Name', \
               'Review Word Count', \
               'Reviewing Date', \
               "Reviewer's Title", \
               "Reviewer's Institution", \
               'Link to All Reviews',
               'Link to PDF of Review',\
               'Page Count',\
               'Attachments']
#%
df=[]
df = result[resulta]  
df=df.replace('x', 'nan') 
df=df.replace('n/a', 'nan')   
df=df.replace('N/A', 'nan')  
df=df.replace('-', 'nan')      
df=df.replace('not applicable', 'nan')     
df=df.replace('xx', 'nan')   
df=df.replace('z', 'nan')  
df=df.replace('', 'nan') 
df=df.replace('NA', 'nan') 
df=df.replace('nan', 'nan')   
df=df.replace('None', 'nan')   
df=df.replace('none', 'nan')   
#In some columns you need to change the type from int/else to string so that when you
#are saving it as excel file, the 'nan' values do not dissapear (in excel)
#https://stackoverflow.com/questions/22005911/convert-columns-to-string-in-pandas
df['Reviewer\'s Title'] = df['Reviewer\'s Title'].astype(str) 
df["Reviewer's Institution"] = df["Reviewer's Institution"].astype(str)   
df["Review Word Count"] = df["Review Word Count"].astype(str)   
df=df.loc[df['Review Word Count']!='nan'] 
df["Review Word Count"] = df["Review Word Count"].astype(float) 
df["Reviewer Name"] = df["Reviewer Name"].astype(str)   
df=df.loc[df['Reviewer Name']!='nan']  
df["Link to PDF of Review"] = df["Link to PDF of Review"].astype(str)   
df=df.loc[df['Link to PDF of Review']!='nan'] 
df=df.loc[df["Reviewer Name"].drop_duplicates().index]
#from itertools import groupby 
#res = [i[0] for i in groupby(np.sort(df["Reviewer Name"]))] 
#%IF some values are gray, convert them to string manually by clicking the table (with mouse)
for i in range(len(df)):
    if ';' in df['Title of Article'].iloc[i]:
        df['Title of Article'].iloc[i]=df['Title of Article'].iloc[i].split(';')[0] 
for i in range(len(df)):
    if 'BMJ 2018' in df['Title of Article'].iloc[i]:
        df['Title of Article'].iloc[i]=df['Title of Article'].iloc[i].split('BMJ 2018')[0] 
#%If something too much or little, you man need to have more here..
#df=df.iloc[:,'Review Word Count']!='nan'
#%Should you need to remove clearly wron values:
        #%
#df=df.loc[df.index!=244]
        #%
dtokz=pd.DataFrame(df)
dtokz.to_csv('bmj_reviews2018_tikka16720_v1.csv',index=False)
dtokz.to_excel("bmj_reviews2018_tikka16720_v1.xlsx") 
#%
#np.mean(dtokz['Review Word Count'])
dfa2=dtokz
aa=dfa2['Review Word Count']<26
bb=dfa2['Attachments']=='attached'
cc= aa & bb
dd= ~cc
#https://stackoverflow.com/questions/15998188/how-can-i-obtain-the-element-wise-logical-not-of-a-pandas-series
#%if dfa2['Attachments']=='attached' or dfa2['Review Word Count']<5
dfa2=dfa2[dd]
#dfa2=dfa2[dfa2['Review Word Count']!=0]
#dfa2=dfa2[dfa2['Review Word Count']!=1]
dfa2=dfa2[dfa2['Reviewer Name']!='Members of the committee']
#%
nn=[]
for i in dfa2.index:
    if "['" in dfa2['Reviewer Name'][i]:
        nn.append(i)
def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
#  https://www.geeksforgeeks.org/python-difference-two-lists/
# Driver Code 
li1 = dfa2.index
li2 = nn
ok=Diff(li1, li2)
dfa2=dfa2.loc[ok]
#%%
import pandas as pd
f =  pd.read_csv('2018aa.txt', header=None)
#https://stackoverflow.com/questions/21546739/load-data-from-txt-with-pandas
#https://www.quora.com/How-do-I-open-a-URL-in-Google-Chrome-in-new-tab-using-Python
import webbrowser
for i in range(len(f)):
    url = f.iloc[i][0]
    webbrowser.open_new_tab(url)
#%%
dfa2.to_csv('bmj_reviews2018_tikka16720_v2.csv',index=False)
