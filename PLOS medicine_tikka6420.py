 -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:16:40 2020

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium import webdriver  # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium.webdriver.common.by import By
import random
import string
#%%
#%https://developers.google.com/edu/python/regular-expressions
#https://docs.python.org/3/library/urllib.request.html
#https://bmcmedicine.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDateAscending&volume=17&page=1
#%PLOS is missing quite many peer reviews (only 27 in 2019, so we need)
#jan='https://journals.plos.org/plosmedicine/issue?id=10.1371/issue.pmed.v16.i01#Research_Article'
#%Let's try to get the first pdf automatically for BMJ, or use the below?, use the below if you can:
#utest='https://www.bmj.com/archive/online/2019'
#I need a list of the kind:
#u1='https://journals.plos.org/plosmedicine/volume#2019'
#%For 2019:
orig='https://journals.plos.org/plosmedicine/issue?id=10.1371/issue.pmed.v16.i'
#a='https://journals.plos.org/plosmedicine/issue?id=10.1371/issue.pmed.v16.i01'
#b='https://journals.plos.org/plosmedicine/issue?id=10.1371/issue.pmed.v16.i02'


lista=[]
aux=[]
for i in range(0,12):
    if i<9:
        aux.append(str(0)+str(i+1))
    else:
        aux.append(str(i+1))
    lista.append(orig+aux[i]) #this is my utot now..(28.3.20)        
#%%    
##https://stackoverflow.com/questions/21939652/insert-at-first-position-of-a-list-in-python             
#%The below takes too long time... 
all_urls = []
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
#%Ok, eli tässä on jo kaikki metadata..
def get_months(aa):
    #%
#    aa=lista[9]
    driver.get(aa)
    ax=[]
    
    login_form = driver.find_elements_by_xpath("//div[@class='section']")

    for i in range(len(login_form)):
        stra = str(login_form[i].text)
        if 'Research Articles\n' in stra:
            ax=login_form[i].text 

    if len(ax)==[]:
        ax.append('nan\n')
    oo=[]
    oo=ax.split("\n")
    #%
    ntt=[]
    for i in range(len(oo)):
        stra = str(oo[i])
        if 'Research Articles' in stra:
            ntt.append(i)
        if 'Related Articles' in stra:  
            ntt.append(i)
            ntt.append(i+1)
    #%You may consider also flattening the previous if list o flists:
    #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    #flatList = [ item for elem in ntt for item in elem]
    ona=oo
    for index in sorted(ntt, reverse=True):
        del ona[index]
    #%I need the dates and links separated, and connect the data of one article to one list element:
    date=[]
    link=[]
    for i in range(len(ona)):
        stra = str(ona[i])
        if 'published ' in stra:
            date.append(ona[i].split('published ')[1].split('| ')[0])
            link.append(ona[i].split('| ')[1])
    #%Selecting every third element
    #        https://stackoverflow.com/questions/1403674/pythonic-way-to-return-list-of-every-nth-item-in-a-larger-list
    article=ona[::3]
    #%
    writer=ona[1:][::3]
    #%This works
    all_in_month=[]
    for i in range(len(link)):
        all_in_month.append([article[i], writer[i], date[i], link[i]])
        #%
    return all_in_month    
#%The work of the day is here: 
#excalib=[]
#excalib=get_months(lista[9])
#%%2020 was not in archive form:
#2020:https://www.ncbi.nlm.nih.gov/pmc/journals/277/ ??
start = []
options = Options()
#options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
o1='https://journals.plos.org/plosmedicine/search?filterJournals=PLoSMedicine&filterStartDate=2020-03-25&filterEndDate=2020-04-24&q=publication_date%3A%5B2020-01-01T00%3A00%3A00Z+TO%202020-04-24T23%3A59%3A59Z%5D&sortOrder=DATE_NEWEST_FIRST&page=1'
#    https://journals.plos.org/plosmedicine/search?filterJournals=PLoSMedicine&filterStartDate=2020-03-25&filterEndDate=2020-04-24&q=publication_date%3A%5B2020-01-01T00%3A00%3A00Z+TO%202020-04-24T23%3A59%3A59Z%5D&sortOrder=DATE_NEWEST_FIRST&page=2
o2='https://journals.plos.org/plosmedicine/search?filterJournals=PLoSMedicine&filterStartDate=2020-03-25&filterEndDate=2020-04-24&q=publication_date%3A%5B2020-01-01T00%3A00%3A00Z+TO%202020-04-24T23%3A59%3A59Z%5D&sortOrder=DATE_NEWEST_FIRST&page=2' 
o_tot=[o1,o2] 
#%%
def get_months2(aa):
    #%
#    aa=o_tot[0]
    driver.get(aa)
    #%sometimes loading takes more time than few second, so some wait is needed:
    time.sleep(20)
    artcilees = driver.find_elements_by_xpath("//dt/a[@href]")
    #%
    namees= driver.find_elements_by_xpath("//dd/p[@class='search-results-authors']")
    datees= driver.find_elements_by_xpath("//dd/p/span[2]")
    linkiis= driver.find_elements_by_xpath("//dd/p[@class='search-results-doi']")
    #%
    article=[] 
    writer=[] 
    date=[] 
    link=[]
    for i in range(len(artcilees)):
        article.append(artcilees[i].text)  
        writer.append(namees[i].text) 
        date.append(datees[i].text) 
        link.append(linkiis[i].text) 
    date2=[]
    for i in range(len(date)):
        stra = str(date[i])
        if 'published ' in stra:
            date2.append(date[i].split('published ')[1].split('| ')[0])
        #%This works
    all_in_month=[]
    for i in range(len(article)):
        all_in_month.append([article[i], writer[i], date2[i], link[i]])
        #%
    return all_in_month 
#%%get_months for 2019 and get_months2 for 2020    
#tot=[]
#for i in range(len(lista)):    
#    tot.append(get_months(lista[i]))
tot=[]
for i in range(len(o_tot)):    
    tot.append(get_months2(o_tot[i])) #It seemst that it worked..
#%%Peer loop for the peer pdf:
#def peer_loop2(total):
tot2=[]
tot2=tot   
for i in range(len(tot2)):
    for j in range(len(tot2[i])):
        driver.get(tot2[i][j][3])  
        if driver.find_elements_by_xpath("//ul/li/a[@class='article-tab-6']")!=[]:
            ana=[]
            ana=driver.find_elements_by_xpath("//ul/li/a[@class='article-tab-6']")
            if ana[0].text=='Peer Review':
                start='https://journals.plos.org/plosmedicine/article/peerReview?id='
                end=tot2[i][j][3][-28:len(tot2[i][j][3])] 
                #One needs to be careful to insert is and js instead of test numbers e.g. 11 and 0.       
#        https://journals.plos.org/plosmedicine/article/peerReview?id= 10.1371/journal.pmed.1002980
                ag2=[]
                ag2=start+end
                tot2[i][j].append(ag2)
        else:
            tot2[i][j].append('nan')
#%Ok, now tot2 has all the main peer-review links, but the actual review links, I need to apply 
#%I need total list 'utot2' or similar solution, which I need to implement here  
#%Maybe getting all the text is faster with soup
#%%Actually, this is already start of new word count function   
sync=[]
sync2=[]
i=0
j=0
for i in range(len(tot2)):
    for j in range(len(tot2[i])):
        if tot2[i][j][4]!='nan':
            sync2.append([i,j])
            #%
i=0
syna=[]        
for i in range(len(sync2)):
    syna.append(tot2[sync2[i][0]][sync2[i][1]][4])
#%%For saving and loading:
df=pd.DataFrame(syna)
df.to_csv("plos_review_links_2020ok_24420tikka.csv", sep=',',index=False)
#%% This would seem to be working, but something is not right..
#If the extraction works, then all the rest goes clearly:
#options = Options()
##options.add_argument("--headless")
#prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
#options.add_experimental_option("prefs", prefs)
#driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
#%
i=0
j=0
nanat=[]
#%
n3=[]
#%
options = Options()
options.add_argument("--headless")
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
#for some reason sometimes the button.clikc does not always work, and need to redo for some places?
for i in range(len(syna)):

        options = Options()
        options.add_argument("--headless")
        prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path='C:/Users/Pauli/Downloads/chromedriver.exe',options=options)
        driver.get(syna[i])
        python_button=[]
        python_button = driver.find_element_by_xpath("//a[@class='peer-review-accordion-expander']")
        python_button.click()
        ax=[]
        ax=driver.find_elements_by_xpath("//div[@class='letter__body']/p")
        anax=[]
        for i in range(len(ax)):
            anax.append(ax[i].text)
        n3.append(anax)
        time.sleep(5) #If you have other extraction work with webdriver in additional spyder window, this may not work
        driver.quit()
        #%%I need to modi my counter due the extraction difficulties, but I have the data now:
nanat[18]=n3[0]
nanat[19]=n3[1]
nanat[20]=n3[2]
#%I need to figure out the connection between nana, nanat, and n3..., for words, I need nana... perhaps n3 is ok
        #%%
df2=pd.DataFrame(n3)
df2.to_csv("plos_med_basic_2020_tikka24420.csv", sep=',',index=False)
#%%This file needs to be converted:
#nana = pd.read_csv('plos_med_basic_2020_tikka24420.csv')
#%This is how you get your list of lists (one level, not necessarilyt two.. back):
tx=pd.read_csv('plos_med_basic_2020_tikka24420.csv')
tx=tx.ix[:,1:]
tx=tx.values.tolist()
tax=[]
for i in range(len(tx)): 
    tax.append([x for x in tx[i] if x == x])
nana=tax
#%%However, this splitting does not work..
#reala=[]
#for i in range(len(n3)):
#    reala.append(n3[i].splitlines( ))
#%% I guess I can use the previous fuction now, see around 400 line down 'words3' function:
    #https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/     
    #https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
    #%'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
#%Ok, . dates:    
#    #https://sqa.stackexchange.com/questions/35338/fetch-all-the-links-on-a-page-that-are-within-the-same-class    
##https://kite.com/python/answers/how-to-remove-specific-characters-from-a-string-in-python  
##%%Some info:
##https://martin-thoma.com/scraping-with-selenium/ #This should be good
##https://www.reddit.com/r/learnpython/comments/6bt8g2/how_can_i_essentially_click_a_button_on_a_webpage/
##https://stackoverflow.com/questions/54862426/python-selenium-get-href-value/54862612
#https://stackoverflow.com/questions/26666919/add-column-in-dataframe-from-list/38490727       
#%Here is how you get the data from pdf:
#https://stackoverflow.com/questions/45470964/python-extracting-text-from-webpage-pdf
#https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
#https://www.geeksforgeeks.org/how-to-get-rows-index-names-in-pandas-dataframe/    
#    #https://stackoverflow.com/questions/13169725/how-to-convert-a-string-that-has-newline-characters-in-it-into-a-list-in-python
#    #https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
#    #https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/
#%%Once you have the dataframe well extracted, the below function it should work:
def words3(dx=pd.DataFrame(nana[0])): #the first zero in 'desig[0][0]' is the variable
    #%
    start=[]
    end=[]
    res=[]
    tot=[]

    for i in range(0, len(dx)):
        stra = str(dx.iloc[i])
        match1 = bool(re.search(r'Requests from the editors:', stra)) #I need to change these values..
        match2 = bool(re.search(r'Reviewer #', stra))
        if match1==True:
            start.append(i)
    
        elif match2==True:
            start.append(i)
        if 'Any attachments provided with reviews can be' in stra:
            end.append(i)

    if end==[]:
        end=start[1:]
        end.append(int(len(dx)*0.98))
        
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

    end=test(end)
    i=0
    at=[]
    for i in range(len(start)):
        if abs(start[i]-start[i-1])<3:
            at.append(i)
    start = [j for i, j in enumerate(start) if i not in at]
#    https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index        
#%here are the exceptions
    if len(end)<len(start):
        ex=[]
        ex=start[1]
        end.insert(0, ex)
        if end[-1]==len(dx):
            end.pop(-1)
#            if len(end)<len(start):
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
            if end[i]-end[i-1]<3 and end[i]-end[i-1]>0:
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
    peta=[]
    eta=[]
    x=[]
    if len(end)>1:
        for i in range(len(end)):
            if len(dx)>300:
                if end[i]-end[i-1]>int(len(dx)*0.5):
                    peta=i #need to delete too high values
                    for i in range(len(end)):
                        x.append(end[i]-end[i-1])
        if x!=[]:
            eta=int(np.average([np.median(x),np.max(x)/2])) 
    
            del end[peta]          #need to delete too high values
            end.insert(peta, eta)
             
    for i in range(len(start)):
        res=[]
        io2=list(tuple(range(start[i], end[i])))
    #https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/     
    #https://stackoverflow.com/questions/44284297/python-regex-keep-alphanumeric-but-remove-numeric
    #%'https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7992 https://onlinelibrary.wiley.com/doi/full/10.1002/sim.7993'
        for i in io2:
            res.append(len(re.findall(r'\w+', re.sub(r'\b[0-9]+\b', '', str(dx.iloc[i])))))

        tot.append(np.sum(res))
        #%
    if tot==[]:
        tot.append(0)
        #%
    return tot  
#%%Test:
Words4=words3(dx=pd.DataFrame(nana[4]))
#%%Got it, the amount of words in peer reviews about ok:
test_short=[]   
for i in range(len(nana)): 
    test_short.append(words3(dx=pd.DataFrame(nana[i])))
    #got some value, but checking.. now about
#%ok..
test_short2=[]
test_short2=test_short   
#%It was tuple list, so now I convert it to list of lists:
#https://stackoverflow.com/questions/16730339/python-add-item-to-the-tuple
tt=[]
for i in range(len(test_short2)):
    tt.append(list(test_short2[i]))
#%I need the word count values tot2..
tot3=tot2    
for i in range(len(tot3)):
    for j in range(len(tot3[i])):
        tot3[i][j].append([])
        #%
for i in range(len(tot3)):
    for j in range(len(tot3[i])):
        if tot3[i][j][5]==[]:
            tot3[i][j][5]=0
                #%
for i in range(len(sync2)):
    tot3[sync2[i][0]][sync2[i][1]][5]=test_short[i]
    #%%
def panda(a):   
    panda1=[]
    panda1=pd.DataFrame(a, index=['Article', 'Names', 'Date', 'Original link', 'Review link','Words'])
    panda1=panda1.T
    return panda1
#%%
#iloa=panda(tot3[0][0])   
    #%
totaali=[]
for i in range(len(tot3)):
    for j in range(len(tot3[i])):
        totaali.append(panda(tot3[i][j]))
    #%%
result = pd.concat(totaali) #this is partly ok..
#%%It would be better to have the numbers in all separate columns
#df = pd.DataFrame(lst)
dipadapa=[]
for i in range(len(result)):
    if result['Words'].iloc[i]!=0:
        dipadapa.append(len(result['Words'].iloc[i]))
#%%
#https://thispointer.com/python-pandas-how-to-add-new-columns-in-a-dataframe-using-or-dataframe-assign/
#result[['Words1','Words2','Words3','Words4']] = pd.DataFrame(index=range(len(result)),columns=range(4))
#https://stackoverflow.com/questions/39050539/adding-multiple-columns-to-pandas-simultaneously
#https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe
#result = result.reset_index(drop=True)
new=[]
new=pd.DataFrame(index=range(np.sum(dipadapa)),columns=range(12))
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
new.columns=tot_counta
#%%nnn
daapa=[]
result = result.reset_index(drop=True)
for i in range(len(result)):
    if result.ix[i,4]=='nan':
        daapa.append(i)
    else:
        pass
result=result.drop(daapa,axis=0)
result = result.reset_index(drop=True)
#%%
cax=[]
for i in range(len(result)):
    cax.append(pd.concat([result.ix[i,0:5]]*dipadapa[i], axis=1).T)
#https://stackoverflow.com/questions/23887881/how-to-repeat-pandas-data-frame
#%
naxi=pd.concat(cax)   
#%
import itertools
b=list(itertools.chain.from_iterable(list(result.ix[:,5])))
c=pd.DataFrame(b)
new['Review Word Count']=c
#%
naxi = naxi.reset_index(drop=True)
new['Title of Article']=naxi.iloc[:,0]
new['Writers of Article']=naxi.iloc[:,1]
new['Date of Publication']=naxi.iloc[:,2]
new['Link to Publication']=naxi.iloc[:,3]
new['Link to All Reviews']=naxi.iloc[:,4]
new['Journal Name']='PLOS Medicine'
#%%
#result=result.fillna(0)  
##For this matrix, these are not necessary:
##https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html 
#result.fillna(value=pd.np.nan, inplace=True)
##%Replacing empty lists with nans:
#result=result.mask(result.applymap(str).eq('[]'))
#%%https://stackoverflow.com/questions/43788826/replace-empty-list-values-in-pandas-dataframe-with-nan?rq=1
##https://stackoverflow.com/questions/45473330/creating-a-pandas-data-frame-of-a-specific-size
dtokz=pd.DataFrame(new)
dtokz.to_csv('plos_reviews_2020_24420tikka.csv', index=False)
