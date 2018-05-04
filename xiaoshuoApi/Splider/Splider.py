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
            # print(bookImageUrl,bookAuthor,bookTitle,bookUrl)
            temp = {"imageUrl":bookImageUrl,"author":bookAuthor,"title":bookTitle,"bookurl":bookUrl}
            hot.append(temp)
        data["hot"] = hot


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
            data[categoryTitle] = tempArray

        # 拼接json
        responseJson = json.dumps(data,ensure_ascii=False)
        # print(responseJson)
        return responseJson










    @classmethod
    def SeleniumSplider(cls,baseUrl):
        driver = webdriver.Chrome()
        driver.get(baseUrl)
        elem = driver.find_elements_by_class_name("hot")
        print(elem)



# Splider.SoupSplider("http://m.biqukan.com/")
# SpliderPY.SeleniumSplider("http://m.biqukan.com/")