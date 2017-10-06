import requests
import re
import os
from lxml import html


headers = {
    'Host':'www.luoo.net',
    'Referer':'http://www.luoo.net/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/61.0.3163.100 Safari/537.36'
}
pictures = []
names = []
positions = []
# 获取期刊第一页
def getJournal():
    url = 'http://www.luoo.net/music/'
    response = requests.get(url, headers).content
    con = html.fromstring(response)
    for i in range(10):
        baseUrl = '//div[@class="vol-list"]/div[{}]'.format(str(i + 1))
        # 获取图片地址
        picture = con.xpath(baseUrl + '/a/img/@src')[0]
        pictures.append(picture)
        # 获取标题
        name = con.xpath(baseUrl + '/div/a/text()')[0]
        names.append(name)
        # 获取具体歌单地址
        position = con.xpath(baseUrl + '/a/@href')[0]
        positions.append(position)
    return pictures, names, positions

songNAmes = []
songUrls = []
albumNums = []
# 获取具体歌曲信息
def getSongIfo(urls):
    # 获取专辑的数字
    ii = 0
    for name in names:
        albumNum = re.findall(r'\d+', name)[0]
        albumNums.append(albumNum)
    for i in urls:
        response = requests.get(i, headers).content
        songCon = html.fromstring(response)
        # 获取歌曲名称
        s = songCon.xpath('//div[@class="vol-tracklist"]/ul/li/div/a[1]/text()')[0]
        songNAmes.append(s)
        # 获取歌曲链接
        for s in range(9):
            url = 'http://mp3-cdn2.luoo.net/low/luoo/radio{}/0{}.mp3'.format(str(albumNums[ii]),str(s + 1))
            songUrls.append(url)
        ii += 1

# 创建文件夹并下载音乐
def makeDir():
    for name in names:
        if not os.path.exists('E:\luowangmusic\{}'.format(name)):
            os.makedirs('E:\luowangmusic\{}'.format(name))
        os.chdir('E:\luowangmusic\{}'.format(name))
        ss = os.getcwd()
        print(ss)
        for j, k in zip(songNAmes, songUrls):
            res = requests.get(k)
            with open(ss + '\{}.mp3'.format(j), 'wb') as songFile:
                songFile.write(res.content)







if __name__ == '__main__':
    getJournal()
    getSongIfo(positions)
    makeDir()




