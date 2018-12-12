import requests
from bs4 import BeautifulSoup
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
import time


def GetSearchResult(url, choice):  # getsearchurls
    """docstring here
        :param url: 
        :param choice: 
    """
    try:
        print('获取搜索结果中')
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        demo = r.text
        soup = BeautifulSoup(demo, 'html.parser')
        x = soup.find('a', href=re.compile('F' + choice))
        Urls = x.attrs['href']
        print('获取搜索结果正常')
        return Urls
    except:
        print('获取搜索结果链接时发生错误')
        return -1


def GetComments(url, choice):  # 获取评论,并储存在本地
    print('获取评论中')
    with open('Comments.txt', 'w+', encoding='utf-8') as myfile:
        if choice == 'movie':
            try:
                for i in range(1, 11):
                    Curl = url + 'comments?start=' + str(
                        i *
                        20) + '&limit=20&sort=new_score&status=P&percent_type='
                    r = requests.get(Curl, timeout=30)
                    r.raise_for_status()
                    r.encoding = 'utf-8'
                    demo = r.text
                    soup = BeautifulSoup(demo, 'html.parser')
                    for x in soup.find_all('span', class_='short'):
                        if x.string:
                            print(x.string)
                            myfile.write(x.string)
                    print('获取第' + str(i + 1) + '页评论完成')
                    # time.sleep(5)

            except:
                pass
        else:
            try:
                for i in range(1, 50):
                    Curl = url + 'comments/hot?p=' + str(i + 1)
                    r = requests.get(Curl, timeout=30)
                    r.raise_for_status()
                    r.encoding = 'utf-8'
                    demo = r.text
                    soup = BeautifulSoup(demo, 'html.parser')
                    for x in soup.find_all('p', class_='comment-content'):
                        if x.string:
                            myfile.write(x.string)
                    print('获取第' + str(i + 1) + '页评论完成')
                    # time.sleep(5)
            except:
                pass
    print('获取评论完成')


def DealComments():
    print('处理评论中')
    Comments = {}
    with open('Comments.txt', 'r', encoding='utf-8') as myfile:
        words = ''.join(myfile.readlines())
        Words = str(words)
        pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 清洗标准，只保留中文字符
        filterdata = re.findall(pattern, Words)  # 将清洗后的文本生成一个列表
        CleanedWords = ''.join(filterdata)  # 将列表组合成一个字符串
        segment = jieba.lcut(CleanedWords)  # 分词
        DropedSegment = []  # 储存分词以后的结果
        for n in segment:
            if n not in DropedSegment:
                DropedSegment.append(n)
        with open(
                'stopwords.txt',
                'r',
        ) as stopwordsfile:
            temp = ''.join(stopwordsfile.readlines())
            Lines = temp.replace('\n', '')
            for n in DropedSegment:
                if Lines.find(n) == -1:
                    Comments[n] = 0
            for n in segment:
                for k in Comments.keys():
                    if n == k:
                        Comments[k] = Comments[k] + 1
    print('评论处理完成')
    return Comments


def ShowWithWordCloud(comments):
    print('词云生成中')
    font = r'C:\Windows\Fonts\simfang.ttf'
    backp = imread('00.jpg')
    wordcloud = WordCloud(
        mask=backp,
        background_color='white',
        font_path=font,
        scale=1.5,
        min_font_size=8).fit_words(comments)
    plt.imshow(wordcloud)
    plt.axis("off")
    print('词云生成完成')
    plt.show()
    wordcloud.to_file('词云.jpg')


def main():
    print('请选择想要搜索的种类:\n')
    print('1.电影\n')
    print('2.书籍\n')
    n = input()
    SearchUrl = 'https://www.douban.com/search?q='
    print("请输入想要搜索的目标：")
    item = input()
    choice = {'1': 'movie', '2': 'book'}
    SearchUrl += item
    SearchResultsUrls = GetSearchResult(SearchUrl, choice[n])
    if SearchResultsUrls != -1:
        GetComments(SearchResultsUrls, choice[n])
        Comments = DealComments()
        ShowWithWordCloud(Comments)
    else:
        print('搜索目标不存在')


main()
