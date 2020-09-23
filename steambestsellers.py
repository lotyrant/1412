from bs4 import BeautifulSoup
import xlwt,os,time,requests

page = 1 #
total_pages = 3 #总页数，爬10页请设定为11
count = 1 #順番に
pool=[] #重ならないように
document = 'Steam_GameTopSellers' #作成したファイル名
wb = xlwt.Workbook() #エクセルを作成する
ws = wb.add_sheet("TopSellers") #エクセルでシートを作る
ws.write(0,0,'番号')#行、列、内容
ws.write(0,1,'タイトル') #B1 ゲームタイトル
ws.write(0,2,'発売日') #C1　発売日
root = os.getcwd() #Pythonルード
date = time.strftime('%Y%m%d',time.localtime(time.time())) #現在の時間

while page<total_pages:
    url = 'https://store.steampowered.com/search/tag=586?supportedlang=japanese&filter=topsellers&page=%s' % str(page)
    r = requests.session()
    res = r.get(url).text
    soup = BeautifulSoup(res,"html.parser")
    game_names = soup.find_all('span',attrs={'class':'title'}) # タイトルを探す
    released_dates = soup.find_all('div',attrs={'class':'col search_released responsive_secondrow'}) #発売日
    for game_name, released_date in zip(game_names,released_dates):
        if game_name.string in pool:
            continue
        else:
            print('%s .GameName：%s Released on：%s' % (count,game_name.string,released_date.string))
            pool.append(game_name.string)
            ws.write(count,0,count)
            ws.write(count,1,game_name.string)
            ws.write(count,2,released_date.string)
            count += 1
    rate = page / (total_pages - 1)
    print('--------------------------第%sページ完成-------------------- %.2f%%' % (str(page),(rate * 100)))
    page += 1
    wb.save('%s%s.xls' % (document,date))
print('--------------------------任務完了--------------------------')
print('データベース：%s\%s%s.xls' % (root,document,date))
