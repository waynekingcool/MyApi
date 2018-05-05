from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import json

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
                lastChap.append({"chapUrl":chapUrl,"chapTitle":chapTitle})
                # print("last",chapUrl,chapTitle)
            elif isEnd == 1:
                chapUrl = baseUrl + child.find("a").get("href")
                chapTitle = child.find("a").get_text()
                allChap.append({"chapUrl":chapUrl,"chapTitle":chapTitle})
                # print("all", chapUrl, chapTitle)


        # 拼成JSON
        dic = dict()
        dic["bookInfo"] = {"title":title,"author":author,"category":category,"state":state,"wordCount":wordCount,"updateTime":updateTime,"desc":desc,"coverUrl":coverUrl}
        dic["lastChap"] = lastChap
        dic["allChap"] = allChap

        responseJson = json.dumps(dic, ensure_ascii=False)
        return responseJson

        # print(title,author,category,state,wordCount,updateTime,desc)




    @classmethod
    def SeleniumSplider(cls,baseUrl):
        driver = webdriver.Chrome()
        driver.get(baseUrl)
        elem = driver.find_elements_by_class_name("hot")
        print(elem)



# Splider.SoupSplider("http://m.biqukan.com/")
# SpliderPY.SeleniumSplider("http://m.biqukan.com/")
SpliderPY.bookInfoSplider("0_790/")