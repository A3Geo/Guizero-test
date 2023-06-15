from guizero import *
from random import choice
from os import listdir
from os.path import isfile, join
import json, unittest
from datetime import datetime

CMS = {'version':'0.3'}
collection = [1,2,3]
MAXID = 0
SELID=0 #ID of selected article
ART={}

#   
def saveArt(pArt):
    f = open('articles/' + str(pArt['ID']) + '.json', 'w') 
    json.dump(pArt,f)
    #f.write(ser)
    f.close()    

def getArtByID(pID):
    global ART
    #print('ShowArt :' + str(id))
    f= open('articles/' + str(pID) + '.json','r')
    ART = json.loads(f.read())
    f.close()
    #return tmp['Content']

#unit tests
def test_getArtByID():  
    getArtByID(1)
    assert ART['ID'] == 1
    assert ART['Title'] == '1st Article'
    assert ART['Content'] == 'Some more random crap\n'


#def showCollection():
#    for i in collection:
#        showArtByID(i)

#show all files in articles folder
def showFiles():
    lstArticles.clear()
    onlyfiles = [f for f in listdir('articles') if isfile(join('articles', f))]
    #print(onlyfiles)
    for i in onlyfiles:
        showFile(i)

#read file, create article from it, update MAXID
def showFile(pFile):
    global MAXID
    f= open('articles/' + str(pFile),'r')
    tmp = json.loads(f.read())
    f.close()
    #Text(app,tmp['Content'])
    lstArticles.append(str(tmp['ID']) + ' : ' +tmp['Title'])
    if int(tmp['ID']) > MAXID :
        MAXID = int(tmp['ID'])

#search the files in the articles folder for the specified string
def searchFiles():
    if len(txtSearch.value) <3:
        if len(txtSearch.value) <1:
            showFiles()
            txtArticle.clear()
        return
    lstArticles.clear()
    onlyfiles = [f for f in listdir('articles') if isfile(join('articles', f))]
    #print(onlyfiles)
    for i in onlyfiles:
        searchFile(i,txtSearch.value)
    if len(lstArticles.items) > 0:   
        lstArticles_click(lstArticles.items[0])    

def searchFile(pFile,pSearch):  
    f= open('articles/' + str(pFile),'r')
    tmp = json.loads(f.read())
    f.close()
    if pSearch in tmp['Content']:
        lstArticles.append(str(tmp['ID']) + ' : ' +tmp['Title'])


def btnNew_Click():
    print(txtInp.value)
    if len(txtInp.value) <3:
        return
    
    newArticle(txtTitle.value,txtInp.value,MAXID+1)
    txtInp.clear() 
    txtTitle.clear()
    showFiles()

def btnEdit_Click():
    ART['Content'] = txtArticle.value
    saveArt(ART)

def newArticle(pTitle,pTxt, pID):
    art = {
    'ID':pID,
    'Title':pTitle,
    'Created':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'Author':'A3',
    'Content':pTxt
    }
    print(art)
    saveArt(art)

# listbox click event
# get article by id, show it in textbox    
def lstArticles_click(pItem):
    global ART
    print(pItem)
    SELID = pItem.split(":")[0].strip()

    txtArticle.clear()
    getArtByID(SELID)
    txtArticle.append(ART['Content'])

def butSearch_click():    
    searchFiles(txtSearch.value)
    
#==========================================================================================================
#     
app = App(title="CMS v" + CMS['version'],width=700,height=800)
app.background_color = "white"
#message = Text(app, text="Welcome to A3CMS (Python version)", grid=[0,0])
#message.text_size = 20

title_box = Box(app, width="fill", align="top", border=True)
Text(title_box,"Welcome to A3CMS (Python version)  ")

#margin
#options_box = Box(app, height="fill", align="bottom", border=False)
#Text(options_box, text="   ")

content_box = Box(app, align="bottom",height="fill", width="600", border=False)
#options2_box = Box(content_box, height="fill", align="right", border=False)
Text(content_box, text="\nEnter titel & text :")

form_box = Box(content_box, layout="grid", width="fill",  border=True)
txtTitle = TextBox(form_box ,grid=[0,0],width="110")
txtInp = TextBox(form_box, grid=[0,1],align="left",width="fill", multiline=True, scrollbar=True, height="5")
button = PushButton(form_box, btnNew_Click, grid=[0,2],text="Save",align="right")

#showCollection()

#articles
artlist_box = Box(content_box, layout="grid", width="600", height="fill", align="bottom", border=False)
Text(artlist_box,grid=[0,0],text="\nARTICLE files : \n",align="left")

SearchBox= Box(artlist_box, layout="grid", width="200", align="right", border=False,grid=[1,0])
txtSearch = TextBox(SearchBox, grid=[0,0],width=30,command=searchFiles)
butSearch = PushButton(SearchBox, butSearch_click, grid=[1,0],text="Search")

lstArticles = ListBox(artlist_box, grid=[0,1],items=["-- Select --"],width=100,height=200, align="top", scrollbar=True,command=lstArticles_click)
txtArticle = TextBox(artlist_box, grid=[1,1],width="64", height="30", multiline=True, scrollbar=True)
button = PushButton(artlist_box, btnEdit_Click, grid=[1,2],text="Update",align="right")
showFiles()
Text(artlist_box,grid=[0,2],text=f"\nMAX id : {MAXID}\n",align="right")

#searchFiles("flippers")

app.display()
