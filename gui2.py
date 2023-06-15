from guizero import *
from random import choice
from os import listdir
from os.path import isfile, join
import json

CMS = {'version':'0.2'}
collection = [1,2,3]
MAXID = 0


def saveArt(pArt):
    f = open('articles/' + str(pArt['ID']) + '.json', 'w') 
    json.dump(pArt,f)
    #f.write(ser)
    f.close()    

def getArtByID(pID):
    #print('ShowArt :' + str(id))
    f= open('articles/' + str(pID) + '.json','r')
    tmp = json.loads(f.read())
    f.close()
    return tmp['Content']

#def showCollection():
#    for i in collection:
#        showArtByID(i)

def showFiles():
    lstArticles.clear()
    onlyfiles = [f for f in listdir('articles') if isfile(join('articles', f))]
    print(onlyfiles)
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

def btnClick():
    print(txtInp.value)
    if len(txtInp.value) <3:
        return
    
    newArticle(txtTitle.value,txtInp.value,MAXID+1)
    txtInp.clear() 
    txtTitle.clear()
    showFiles()

def newArticle(pTitle,pTxt, pID):
    art = {
    'ID':pID,
    'Title':pTitle,
    'Created':'14jun23',
    'Author':'A3',
    'Content':pTxt
    }
    print(art)
    saveArt(art)
    
def lstArticles_click(pItem):
    print(pItem)
    id = pItem.split(":")[0].strip()

    txtArticle.clear()
    txtArticle.append(getArtByID(id))
    
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

content_box = Box(app, align="bottom",height="fill", width="600", border=True)
#options2_box = Box(content_box, height="fill", align="right", border=False)
Text(content_box, text="Enter titel & text : \n")

form_box = Box(content_box, layout="grid", width="fill",  border=False)
txtTitle = TextBox(form_box ,grid=[0,0],width="110")
txtInp = TextBox(form_box, grid=[0,1],align="left",width="fill", multiline=True, scrollbar=True, height="5")
button = PushButton(form_box, btnClick, grid=[0,2],text="Save")

#showCollection()

#articles
artlist_box = Box(content_box, layout="grid", width="600", height="fill", align="bottom", border=False)
Text(artlist_box,grid=[0,0],text="\nARTICLE files : \n",align="left")
lstArticles = ListBox(artlist_box, grid=[0,1],items=["-- Select --"],width=100,height=200, align="top", scrollbar=True,command=lstArticles_click)
txtArticle = TextBox(artlist_box, grid=[1,1],width="64", height="30", multiline=True, scrollbar=True)
showFiles()
Text(artlist_box,grid=[1,0],text=f"\nMAX id : {MAXID}\n",align="right")

app.display()


