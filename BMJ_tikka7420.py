# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:16:40 2020

@author: pauli
"""
# Task 1.

# Extract the following journal peer review data for each (available) article from 
# BMJ, PLOS Medicine, and BMC between January 15 2020 and January 14 2020, and use also google searches: 

#(1) The quality of preventive care for pre-school aged children in Australian general practice
#(2) Louise K. Willes
#(3) 6.12.2020
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
#%%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
#%PLOS is missing quite many peer reviews (only 27 in 2020, so we need)
#jan='https://journals.plos.org/plosmedicine/issue?id=10.1371/issue.pmed.v16.i01#Research_Article'

#%Let's try to get the first pdf automatically for BMJ, or use the below?, use the below if you can:
#utest='https://www.bmj.com/archive/online/2020'
#I need a list of the kind:
u1='https://www.bmj.com/archive/online/2020/'
#%% Rist I ghought to enter some of the link data manually:
#lista=['01-01','01-08','01-15','01-22',
#       '01-29','02-05','02-12','02-19',
#       '02-26','03-05','03-12','03-19',
#       
#       '03-26','04-02','04-09','04-16','04-23',
#       '04-30','05-07','05-14','05-21',
#       '05-28','06-04','06-11','06-18',
#       
#       '06-25','07-02','07-09','07-16','07-23',
#       '07-30','08-06','08-13','08-20',
#       '08-27','09-09','09-16','09-23','09-30',
#       
#       '10-07','10-14','10-21','10-28',
#       '11-04','11-11','11-18','11-25',
#       '12-02','12-09','12-16','12-23']
#%%Or more easily with..
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
utot=[]
for i in range(len(ax)):
    utot.append(u1+ax[i])
#%Should ax have less values than needed:
#https://stackoverflow.com/questions/21939652/insert-at-first-position-of-a-list-in-python
#utot.insert(0,'https://www.bmj.com/archive/online/2020/12-31')    
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
utot2=np.delete(utot, popia).tolist()
#%For saving and loading:
utot22=pd.DataFrame(utot2)
utot22.to_csv('weekly_bmj2020_links_tikka7420.csv')
#utot2=pd.read_csv("weekly_bmj2020_links_tikka7420.csv")
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
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
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
alle=date2(utot2)        
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
total=[]
for i in range(len(tot)):    
    total.append([x for x in tot[i] if str(x) != 'nan'])    
#%For saving and loading
dates=pd.DataFrame(alle)
dates.to_csv('all_dates_2020_27420.csv')
#%Should you need to load:
#dates=pd.read_csv("all_dates_2020_27420.csv")
#dates=list(dates.ix[:,1]) #or see above
#%For saving and loading:
linksa=pd.DataFrame(links)
linksa.to_csv('all_links_2020_27420.csv')
#%Should you need to load:
#links=pd.read_csv("all_links_2020_27420.csv")
#links=list(links.ix[:,1]) #or see above
#%Saving
namesa=pd.DataFrame(names)
namesa.to_csv('all_names_2020_27420.csv')
#namesa=pd.read_csv("all_names_2020_27420.csv")
#names=list(namesa.ix[:,1]) #or see above
#%The names of the articles:
totali=pd.DataFrame(total)
totali.to_csv('all_total_BMJ_links_2020_24420.csv')
#%Should you need to load:
#total=[]
#total=pd.read_csv("all_total_BMJ_links_2020_24420.csv")
##%You need to do this, if you want to load as a list again:
#total=total.ix[:,1:]
#total=total.values.tolist()
#taxi=[]
#for i in range(len(total)): 
#    taxi.append([x for x in total[i] if x == x])
#total=taxi 
#%I am guess that I need similarly 'too loops' to get this solved.
#The first:
def peer_loop(total):
    #%
    n=0
    spana3=[]
    spana3=total
#    all_spans4=[]
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
            if 'Peer review' in text.ix[i,0]:
                a.append(i)
            if 'Abstract' in text.ix[i,0]:
               b.append(i)
        cur=text.ix[a[0]:b[0],0]
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
    #    elif nop==[]:
    #        cura=cura[0:noo[0]]
        else:
            cura=cura[0:-1]
            
        for i in range(len(cura)):
            if len(cura[i].split(', '))>1:
                cura[i]=cura[i].split(', ')[1]
        cura=cura[::2]
        pura.append(cura)
    #%
    return pura
#%Peer loop for the peer pdf:
def peer_loop2(total):
    #%
    n=0
    spana3=[]
    ok=[]
    spana3=total
    for n in range(len(spana3)):
        ag2=[]
        driver.get(spana3[n])         
        if driver.find_elements_by_xpath("//a[@title='Article Tab - Peer review']")[0].text=='Peer review'\
            or driver.find_elements_by_xpath("//a[@title='Article Tab - Peer review']")=='Peer review':
            
            ag2=spana3[n]+'/peer-review'
            driver.get(ag2) 
            #%
            if driver.find_elements_by_xpath("//div[@class='pane-content']/div[@id='no-peer-review']")==[]:
            #This is not completely intuitive..:
                if len(driver.find_elements_by_xpath("//div[@class='peer-list']/ul"))>=3:
                else:
                    ok.append([])
            else:
                ok.append([])
        else:
            ok.append([])
            #%this is the peer review pdf..
    return ok
#%test..
#nix=[]
#for i in range(0,4):
#    nix.append(peer_loop2(total[i]))     
#%
#%tn and tn1 for the writer names and peer review links:  
tn=[]
i=0
for i in range(len(total)):
    tn.append(peer_loop(total[i]))
#%tn
ttn=[]
for i in range(len(tn)): 
    for j in range(len(tn[i])):
        tn[i][j]=', '.join(tn[i][j])
 #%   
#tna=pd.DataFrame(tn)
#tna.to_csv('writers_BMJ_2020_24420.csv')
#%Should you need to load:
#tn=[]
#tn=pd.read_csv("writers_BMJ_2020_24420.csv")
##%You need to do this, if you want to load as a list again:
#tn=tn.ix[:,1:]
#tn=tn.values.tolist()
#taxi=[]
#for i in range(len(tn)): 
#    taxi.append([x for x in tn[i] if x == x])
#tn=taxi 
    #%
tn1=[]
i=0
for i in range(len(total)):
    tn1.append(peer_loop2(total[i])) #if you go just numberw, while loop is also possible
#%Again for loading and saving:
#tnn=pd.DataFrame(tn1)
#tnn.to_csv('all_total_names_20320_v2.csv')
#tn2=pd.DataFrame(tn1)
#tn2.to_csv('all_total_pdf_links_2020_28220.csv')  
#%
#%tn1=pd.read_csv("all_total_pdf_links_2020_28220.csv")
#tn1=list(tn1.ix[:,1]) #or see above
#%Now I need to gather the data for each article (one row):
part_list=[]
#%Some info:
#https://martin-thoma.com/scraping-with-selenium/ #This should be good
#https://www.reddit.com/r/learnpython/comments/6bt8g2/how_can_i_essentially_click_a_button_on_a_webpage/
#https://stackoverflow.com/questions/54862426/python-selenium-get-href-value/54862612

#%And the part list (for all weeks):
for i in range(len(total)):
    part_list.append([tn[i], alle[i], names[i], total[i], tn1[i]])
#https://www.journaldev.com/23674/python-remove-character-from-string
#%And then all the weeks would be something like: for loading and saving:
tnx=pd.DataFrame(part_list)
tnx.to_csv('all_categores_2020_29420_v1.csv')
#%%https://stackoverflow.com/questions/26666919/add-column-in-dataframe-from-list/38490727       
dt=pd.concat([pd.DataFrame(part_list[i][0], columns=['Writers of Article']) for i in range(17)], ignore_index=True)
#%dt=dt.drop([3, 4]) #if something is not ok
#dt=dt.reset_index(drop=True)
#%Part list may require [] brackests if it is just one string variable
dt1=pd.concat([pd.DataFrame(part_list[i][1], columns=['Date of Publication'])\
               for i in range(17)], ignore_index=True)
#%
dt2=pd.concat([pd.DataFrame(part_list[i][2], columns=['Title of Article'])\
               for i in range(17)], ignore_index=True)
    #%
dt3=pd.concat([pd.DataFrame(part_list[i][3], columns=['Link to Publication']) for i in range(17)], ignore_index=True)
#%
for i in range(len(part_list)):
    for j in range(len(part_list[i][4])):        
        if part_list[i][4][j]==[]:
            part_list[i][4][j]=0
            #%
dt4=pd.concat([pd.DataFrame(part_list[i][4], columns=['Link to PDF of Review']) for i in range(17)], ignore_index=True)
    #%%Check the range
tot_list = pd.DataFrame(index=range(0,len(dt)),columns = ['Writers of Article', 'Date of Publication', \
                        'Title of Article', 'Link to Publication', 'Link to PDF of Review'])  
tot_list['Writers of Article'] = dt
tot_list['Date of Publication'] = dt1
tot_list['Title of Article'] = dt2
tot_list['Link to Publication'] = dt3
tot_list['Link to PDF of Review'] = dt4
final_matrix=tot_list
#%For saving and loading:
tnp=pd.DataFrame(tot_list)
tnp.to_csv('all_for_bmj_review2020_20320tikka.csv')
##%%
#final_matrix=[]
#final_matrix=pd.read_csv("all_for_bmj_review2020_20320tikka.csv")
#final_matrix=final_matrix.ix[:,1:]

#%%Here is how you get the data from pdf:
#https://stackoverflow.com/questions/45470964/python-extracting-text-from-webpage-pdf
#% This is how you import the pdfs from links:
#https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
#https://www.geeksforgeeks.org/how-to-get-rows-index-names-in-pandas-dataframe/    
import urllib.request
url=[]
x=[]
xa=[]
for i in range(len(final_matrix)):
    if final_matrix['Link to PDF of Review'][i] !=0:
        url=str(final_matrix['Link to PDF of Review'][i])
        x=str(list(final_matrix.index)[i])
        xa.append(x)
        urllib.request.urlretrieve(url, filename='C:\\python\\BMJ2020\\'+x+'peer.pdf') #check..
    else:
        pass
#Then convert the files to word e.g. with WPS PDF to Word program
#%%Now I need to do I loop for all files, and save the results
directory="C:\python\BMJ2020\*.docx"
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
#%
#df2=totis(x=all_files2[2])
#%
df_tot=[]
for i in range(len(all_files2)):
    df_tot.append(totis(x=all_files2[i]))

#%With this you get the extra columns away by joining the cells that do that
x=0
for x in range(len(df_tot)):
    for i in range(len(df_tot[x])):
        if df_tot[x].ix[i].shape >(1,):
            ax=[]
            bx=[]
            for j in range(len(df_tot[x].ix[i])):
                if df_tot[x].ix[i][j] != None:
                    ax.append(df_tot[x].ix[i][j])
                elif df_tot[x].ix[i][j] == None:
                    ax.append(str(' '))
            bx=' '.join(ax) #this syntax is better tget right
            #https://stackoverflow.com/questions/10880813/typeerror-sequence-item-0-expected-string-int-found
            df_tot[x].ix[i,0]=bx
#%Now you just need the first column from every dataframe
dtok=[]            
for i in range(len(df_tot)):
    dtok.append(df_tot[i].loc[:,0])          
#%For saving and loading:
dtok2=pd.DataFrame(dtok)
dtok2.to_csv('essential_for_bmj_2020_review_25320tikka.csv')
#%
#dtok=[]
#dtok=pd.read_csv("essential_for_bmj_2020_review_25320tikka.csv")
#dtok=dtok.ix[:,1:]  
#%Make the list of list a list of panda dataframes:
#total=dtok.ix[:,1:]
#total=total.values.tolist()
#taxi=[]
#for i in range(len(total)): 
#    taxi.append([x for x in total[i] if x == x])
#    #%
#maxi=[]
#for i in range(len(taxi)):
#    maxi.append(pd.DataFrame(taxi[i]))
#mazi=[]
#for i in range(len(taxi)):
#    mazi.append(maxi[i][0])
#dtok=mazi
#%%Once you have the dataframe well extracted, the below function it should work:
def words2(dx=dtok[0],xx=int(desig[0][1])): #the first zero in 'desig[0][0]' is the variable
    #%
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
    ss=[]
    ssa=[]
    ssn=[]
    Article=[]
#    dx=dtok[112]
    for i in range(0, len(dx)):
        stra = str(dx.iloc[i])
        match1 = bool(re.search(r'Reviewer: ', stra)) #I need to change these values..
        match2 = bool(re.search(r'Reviewer ', stra))
        match2n= bool(re.search(r' Comments:', stra))
        #I need to change these values..
        match2a = bool(re.search(r'Detailed comments', stra)) #I need to change these values..
        match2b = bool(re.search(r'Our statistician made the following comments:', stra))  
        
        match3  = bool(re.search(r'Additional Questions:', stra))
        match4  = bool(re.search(r'Please enter your name:', stra))
        mx4a   = bool(re.search(r'Institution: ', stra))
        match5 = bool(re.search(r'Information for submitting a revision', stra))
        
        if match1==True:
            start.append(i)

        elif match2n==True:
            start.append(i)

        elif match2==True:
            if 'Patient Reviewer' in stra:
                pass
            elif 'Patient Reviewer' not in stra:
                start.append(i)
      
        elif match2a==True:
            start.append(i)
        elif match2b==True:
            start.append(i)

        if match3==True:
            end.append(i)
        elif match4==True:
            end.append(i)
        elif mx4a==True:
            end.append(i)
        elif match5==True:
            end.append(i)

        if match4:
            sup.append(i)
            supa.append([dx[i].split(": ")[1].split(" Job Title")[0],i])
            
        if 'Job Title' in stra:
            ss.append(i)
            a=dx[i].split("Job Title: ")[1] ==['']
            b=dx[i].split("Job Title: ")[1] !=['']
            c=dx[i].split("Job Title")[0] !=['']
            if a:
                s4.append([dx[i+1].split(" Institution")[0],i])
            elif b or c:
                s4.append([dx[i].split("Job Title: ")[1].split(" Institution")[0],i])
                
        if 'Institution' in stra:
            ssa.append([dx[i],i])
        if 'Thank you for sending us your paper. We read it with interest but I am sorry to say that' in stra:
            start.append(0)
            end.append(int(len(dx)*0.95))
        if 'entitled "' in stra:
            if i<int(len(dx)*0.2):
                Article.append((dx[i].split('entitled "')[1]).split('"')[0])
           

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
    if end==[]:
        end=start[1:]
        end.append(int(len(dx)*0.98))
   
    #%
    i=0
    at=[]
    for i in range(len(start)):
        if abs(start[i]-start[i-1])<5:
            at.append(i)
            #%
    start = [j for i, j in enumerate(start) if i not in at]
#    https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index    
#%here are the exceptions
     #%
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
#%
    end=test(end)
    #%
    if len(start)>len(end):
        if end[0]==start[1] or end[0]+1==start[1] or end[0]-1==start[1] or end[0]+2==start[1] or end[0]-2==start[1]:
            start.pop(1)
    #%
    if len(end)<len(start):
        ex=[]
        ex=start[1]
        end.insert(0, ex)
        if end[-1]==len(dx):
            end.pop(-1)
            if sup!=[]:
                if max(sup)<len(dx):
                    end.append(max(sup))
                elif max(sup)==len(dx):
                    end.append(int(len(dx)*0.95))
                    
            elif sup==[]:
                end.append(int(len(dx)*0.95))
        if len(end)<len(start):
            enda=[]
            enda=end[-1]
            e2=[]
            e2=start[1:]
            e2.append(enda)
            end=e2

    aux2=[]
    a3=[]
    i=0
    if len(start)<len(end):
        for i in range(len(end)):
            if end[i]-end[i-1]<4 and end[i]-end[i-1]>0:
                aux2.append(i-1)
    a3.append(end[0])
    i=0

    for i in range(len(aux2)):
        if aux2[i]-aux2[i-1]>1:
            a3.append(end[aux2[i]])
    
    if len(start)<len(end):
        if len(start)>1:
            a3.insert(0, start[1])
            end=a3
        elif len(start)==1:
            a3.insert(0, start[0])
            end=[a3[1]]
        elif len(start)==0:
            end.append(int(len(dx)*0.95))
            start.append(int(len(dx)*0.05))
#%
    if len(end)!=len(start):
        enda=[]
        enda=end[-1]
        end=start[1:]
        if sup!=[]:
            if max(sup)<len(dx):
                end.append(max(sup))
        elif sup==[]:
            end.append(int(len(dx)*0.95))
        elif enda<int(len(dx)*0.99):
            end.append(enda)
        elif enda>int(len(dx)*0.9):
            end.append(int(len(dx)*0.95))
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
                #%
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
        for i in range(len(no)):
            endax1.append(end.index(no[i]))
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
    Institution=   names(supass, xt='Journal Institution') 
    #%
    Title=   names(s4, xt='Journal Reviewer Title')
    #%
    Reviewer=   names(supa, xt='Journal Reviewer')
    Article2 = []
    Article2 = Article * len(Reviewer)
    Designation=[]
    Designation = [xx] * len(Reviewer)
#%
    for i in range(len(start)):
        res=[]
        io2=list(tuple(range(start[i], end[i])))
    #https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/     
    #https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
    #%'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
        for i in io2:
            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[i])))))

        tot.append(np.sum(res))
        
    if tot==[]:
        tot.append(0)
 #%
    return tot, Reviewer, Title, Institution, Article2, Designation  
#%%Test:
#Words, Reviewer, Title, Institution, Article2, Designation=words2(dx=dtok[15],xx=int(desig[15][1]))
    #%Got it, the amount of words in peer reviews about ok:
test_short=[]   
for i in range(len(dtok)): 
    test_short.append(words2(dx=dtok[i],xx=int(desig[i][1])))
    #got some value, but checking.. now about
    #%ok..
test_short2=[]
test_short2=test_short  
#% 
tnan=pd.DataFrame(test_short2)
tnan.to_csv('half of the info_BMJ_2020_24420.csv')
#%Should you need to load:
#tnan=[]
#tnan=pd.read_csv("test_short2_BMJ_2020_24420.csv")
#%You need to do this, if you want to load as a list again:
#tnan=tn.ix[:,1:]
#tnan=tn.values.tolist()
#taxi=[]
#for i in range(len(tnan)): 
#    taxi.append([x for x in tnan[i] if x == x])
#tnan=taxi
#test_short2=tnan 
#%It was tuple list, so now I convert it to list of lists:
#https://stackoverflow.com/questions/16730339/python-add-item-to-the-tuple
tt=[]
for i in range(len(test_short2)):
    tt.append(list(test_short2[i]))
#%
ttax=pd.DataFrame(tt)
ttax.to_csv('half of the infoos_BMJ_2020_24420.csv')    
#%   
def panda(a):   
    panda1=[]
    panda1=pd.DataFrame(a, index=['Review Word Count', 'Reviewer Name', "Reviewer's Title", "Reviewer's Institution", 'Article Name','Designation'])
    panda1=panda1.T
    return panda1

totaali=[]
for i in range(len(tt)):
    totaali.append(panda(tt[i]))

result = pd.concat(totaali)
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html 
result.fillna(value=pd.np.nan, inplace=True)
#%Replacing empty lists with nans:
result=result.mask(result.applymap(str).eq('[]'))
#https://stackoverflow.com/questions/43788826/replace-empty-list-values-in-pandas-dataframe-with-nan?rq=1
#%Let's do the other way around i.e. add final_matrix to result, here are nan columns:
result['Writers of Article'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Date of Publication'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Title of Article'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Link to Publication'] = pd.DataFrame(index=range(len(result)),columns=range(1))
result['Link to PDF of Review'] = pd.DataFrame(index=range(len(result)),columns=range(1))
#%Zeroing the indeces:
result=result.reset_index()
result=result.drop(columns=['index'])
result=result.replace('YYY', 'nan')
#%You may need to curate your data:
#https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-in-a-certain-column-is-nan
#result=result.iloc[0:675,:]
result = result[result['Designation'].notna()]
#huh, now I got the designation correct in result, now need to match that to the final matrix designation
#%%There must be faster ways to do this, than below, e.g. with maps or libraries etc.:
#result.applymap(lambda y: [result.applymap(lambda x: x == [])]=='nan')
#final_matrix=final_matrix.drop(columns=['Reviewer'])
for i in range(len(final_matrix)):
    for j in range(len(result)):
        if final_matrix.index.tolist()[i] ==int(result['Designation'].iloc[j]):
            result['Title of Article'].iloc[j]=final_matrix['Title of Article'].iloc[i]
for i in range(len(final_matrix)):
    for j in range(len(result)):
        if final_matrix.index.tolist()[i] ==result['Designation'].iloc[j]:
#            result['Title of Article'].iloc[j]=final_matrix['Title of Article'].iloc[i]
            result['Writers of Article'].iloc[j]=final_matrix['Writers of Article'].iloc[i]
            result['Date of Publication'].iloc[j]=final_matrix['Date of Publication'].iloc[i]
            result['Link to Publication'].iloc[j]=final_matrix['Link to Publication'].iloc[i]
#%%This xa maybe excessive..
for i in range(len(xa)):
    for j in range(len(result)):
        if int(xa[i]) ==result['Designation'].iloc[j]:
            result['Link to PDF of Review'].iloc[j]=final_matrix['Link to PDF of Review'].iloc[int(xa[i])]
            #this should come from 
            #%
#1) It seems that link to pdf is not giving all the data, the articles etc. metadata are not refering to right review..   
#%Let me first check the designation..:
result=result.drop(columns=['Designation', 'Title of Article'])           
result.rename(columns={'Article Name':'Title of Article'}, inplace=True) 
result["Journal Name"]='BMJ' #if something is not available, mark it with 'nan'
result["Reviewing Date"]='nan' #if something is not available..
result["Link to All Reviews"]='nan'
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
               'Link to PDF of Review']
df = result[resulta]        
#%%If something too much or little, you man need to have more here..
#df=df.iloc[0:493,:]
            #%
dtokz=pd.DataFrame(df)
dtokz.to_csv('bmj_reviews2020_29420tikka.csv',index=False)
