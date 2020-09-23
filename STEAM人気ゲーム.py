from bs4 import BeautifulSoup
import csv,requests

def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return ""

def getMostPopularGamesList(steamHTMLText):
    #リストを作成
    gameList = []
    soup=BeautifulSoup(steamHTMLText)
    gameTr=soup.find_all("tr",{"class":"player_count_row"})
    for tr in gameTr:
        singleGameData=[]
        for span in tr.find_all("span",{"class":"currentServers"}):
            singleGameData.append(span.string)
        for a in tr.find_all("a",{"class":"gameLink"}):
            singleGameData.append(a.string)
        gameList.append(singleGameData)
    return gameList

def printList(gameList):
    print("steam人気ランキング")
    print("{1:{0}<4}{2:{0}<8}{3:{0}<10}{4:{0}<10}".format((chr(12288)),"ランキング","現在プレイ中人数","今日最大人数","タイトル"))
    for i in range(num):
        g=gameList[i]
        print("{1:{0}<4}{2:{0}<8}{3:{0}<10}{4:{0}^10}".format((chr(12288)),i+1,g[0],g[1],g[2]))

if __name__ == '__main__':
    url = "https://store.steampowered.com/stats/"
    steamHTMLText = getHTMLText(url)
    gameList = getMostPopularGamesList(steamHTMLText)
    num = len(gameList)
    printList(gameList)