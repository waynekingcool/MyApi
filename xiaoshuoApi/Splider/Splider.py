from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re
from xiaoshuoApi.Splider.WBTool import WBTool
# 爬虫类
class SpliderPY:

    # 类方法
    @classmethod
    def SoupSplider(cls,baseUrl):
        url = "http://m.biqukan.com"

        html = urlopen(baseUrl)
        # 需要以html5lib进行解析,但是速度会慢很多
        bsObj = BeautifulSoup(html,"html5lib")
        # 返回的数据 用来拼接json
        data = {}
        dataArray = []

        # print(bsObj.prettify())
        # 解析网页
        # 热门小说
        hotArray = bsObj.find("div",{"class":"hot"}).findAll("div",{"class":"item"})
        hot = []
        # print(hotArray)
        for i in range(len(hotArray)):
            # 封面
            bookImageUrl = hotArray[i].find("div",{"class":"image"}).find("a").find("img").get("src")
            # 作者
            bookAuthor = hotArray[i].find("span").get_text();
            # 标题
            bookTitle = hotArray[i].find("dt").find("a").get_text();
            # 链接
            tempUrl = hotArray[i].find("dt").find("a").get("href")
            bookUrl = "http://m.biqukan.com" + tempUrl
            # 描述
            bookDesc = hotArray[i].find("dd").get_text();
            # print(bookImageUrl,bookAuthor,bookTitle,bookUrl)
            temp = {"imageUrl":bookImageUrl,"author":bookAuthor,"title":bookTitle,"bookurl":bookUrl,"bookDesc":bookDesc}
            hot.append(temp)
        # data["hot"] = hot
        dataArray.append({"hot":hot})


        # 小说分类
        category = bsObj.findAll("div",{"class":"block"})
        # print(category)
        # 数组用来保存分类
        for i in range(len(category)):
            # 分类标题
            categoryTitle = category[i].find("h2").get_text();
            liArray = category[i].find("ul").findAll("li")

            tempArray = []
            for j in range(len(liArray)):
                liItem = liArray[j]
                # 小说分类
                bookType = liItem.find("span", {"class": "s1"}).get_text();
                # 小说名称
                bookTitle = liItem.find("span", {"class": "s2"}).find("a").get_text();
                # 小说链接
                tempUrl = liItem.find("span", {"class": "s2"}).find("a").get("href")
                bookUrl = url + tempUrl
                # 小说作者
                bookAuthor = liItem.find("span", {"class": "s3"}).get_text();
                # print(categoryTitle, bookType, bookTitle, bookAuthor, bookUrl)
                tempDic = {"categoryTitle":categoryTitle,"bookType":bookType,"title":bookTitle,"author":bookAuthor,"bookurl":bookUrl}
                tempArray.append(tempDic)
            # 不同的分类放到不同的数组中
            # data[categoryTitle] = tempArray
            dataArray.append({categoryTitle:tempArray})

        # 拼接json
        responseJson = json.dumps(dataArray,ensure_ascii=False)
        # print(responseJson)
        return responseJson

    # 小说详情页
    @classmethod
    def bookInfoSplider(cls,pathurl):
        baseUrl = "http://www.biqukan.com"
        url = baseUrl + '/' +pathurl
        html = urlopen(url)
        soup = BeautifulSoup(html,"html5lib")
        # 小说信息
        info = soup.find("div",{"class":"info"})
        # 封面
        cover = info.find("div",{"class":"cover"}).find("img").get("src")
        coverUrl = baseUrl + cover
        # 名称
        title = info.find("h2").get_text()

        # 小说详情
        small = info.find("div",{"class":"small"}).findAll("span")
        author = ""
        category = ""
        state = ""
        wordCount = ""
        updateTime = ""
        for i in range(len(small)):
            span = small[i]
            text = span.get_text()
            if i == 0:
                author = text.replace("作者：","")
            elif i == 1:
                category = text.replace('分类：','')
            elif i == 2:
                state = text.replace('状态：','')
            elif i == 3:
                wordCount = text.replace('字数：','')
            elif i == 4:
                updateTime = text.replace('更新时间：','')

        # 小说介绍
        desctemp = info.find("div",{"class":"intro"}).get_text()
        desc = desctemp.replace("简介：","")

        # 章节
        listmain = soup.find("div",{"class":"listmain"}).find("dl")
        # print(listmain.contents)
        isEnd = -1

        lastChap = []
        allChap = []

        # 控制章节 有些坑爹的小说,一章分成好几章..所以设置一个变量,用来控制chapId
        chapAllId = -1
        chapLastId = -1

        for child in listmain.contents:
            # print(child.name)
            if child.name is None:
                # 如果是换行符什么的,直接跳过
                continue

            if child.name == "dt":
                # 第一次遇到dt
                if isEnd == -1:
                    isEnd = 0
                elif isEnd == 0 :
                    isEnd = 1
                continue



            # 最新章节
            if isEnd == 0:
                chapUrl = baseUrl + child.find("a").get("href")
                chapTitle = child.find("a").get_text()
                if chapLastId == -1 :
                    chapLastId = WBTool.cn2dig(chapTitle) - 1
                else:
                    chapLastId += 1
                lastChap.append({"chapUrl":chapUrl,"chapTitle":chapTitle,"chapId":chapLastId})
                # print("last",chapUrl,chapTitle)

            elif isEnd == 1:
                chapUrl = baseUrl + child.find("a").get("href")
                chapTitle = child.find("a").get_text()
                if chapAllId == -1 :
                    chapAllId = WBTool.cn2dig(chapTitle) - 1
                else:
                    chapAllId += 1

                allChap.append({"chapUrl":chapUrl,"chapTitle":chapTitle,"chapId":chapAllId})
                # print("all", chapUrl, chapTitle)


        # 拼成JSON
        dic = dict()
        dic["bookInfo"] = {"title":title,"author":author,"category":category,"state":state,"wordCount":wordCount,"updateTime":updateTime,"desc":desc,"coverUrl":coverUrl}
        dic["lastChap"] = lastChap
        dic["allChap"] = allChap

        responseJson = json.dumps(dic, ensure_ascii=False)
        return responseJson

        # print(title,author,category,state,wordCount,updateTime,desc)

    # 小说内容
    @classmethod
    def ChapContent(cls,url):
        baseUrl = "http://www.biqukan.com"
        # url = baseUrl + '/' + pathurl
        html = urlopen(url)
        soup = BeautifulSoup(html,"html5lib")
        # 章节名称
        title = soup.find("div",{"class":"content"}).find("h1").get_text()

        # 章节内容
        content = soup.find("div",{"id":"content"}).get_text()
        # 添加换行符
        out = re.sub(r"\s{2,}", "\n  ", content)

        pageChapArray = soup.find("div",{"class":"page_chapter"}).findAll("li")
        # 上一章
        prevChap = baseUrl + pageChapArray[0].find("a").get("href")
        if prevChap.find("html") == -1:
            prevChap = "已经是第一章"
        # 下一章
        nextChap = pageChapArray[2].find("a").get("href")
        # 如果不是以.html结尾,则为最后一章
        if nextChap.find("html") == -1 :
            nextChap = "最后一章"

        dic = dict()
        dic["chapTitle"] = title
        dic["pre"] = prevChap
        dic["next"] = nextChap
        dic["chapContent"] = out
        # print(out)
        responseJson = json.dumps(dic,ensure_ascii=False)
        return responseJson


    @classmethod
    def SeleniumSplider(cls,baseUrl):
        driver = webdriver.Chrome()
        driver.get(baseUrl)
        elem = driver.find_elements_by_class_name("hot")
        print(elem)

    @classmethod
    def testRe(cls):
        testStr = "第六章 升级纸张，还是内容？"
        # matchObj = re.match(r'^第.章|回$',testStr)
        matchObj = re.match(r'^第[一二三四五六七八九零千百十]*',testStr)
        temp = matchObj.group()
        mystr = re.sub(r'第','',temp)
        print(mystr)



# Splider.SoupSplider("http://m.biqukan.com/")
# SpliderPY.SeleniumSplider("http://m.biqukan.com/")
# SpliderPY.bookInfoSplider("0_790/")
# SpliderPY.ChapContent("http://www.biqukan.com/0_790/20088431.html")
SpliderPY.testRe()