from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from django.http import response
import requests
from opencc import OpenCC #字體轉換
 
 
# 抽象類別
class Search(ABC):
    def __init__(self, area):
        self.area = area  # 地區
 
    @abstractmethod
    def scrape(self):
        pass
 
class IFoodie(Search):
    def scrape(self):
        response = requests.get(
        "https://ifoodie.tw/explore/"+self.area+"/list?sortby=popular&opening=true")
 
        soup = BeautifulSoup(response.content, "html.parser")
 
        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div',class_='jsx-3440511973 restaurant-info', limit=3)
 
        content = ""
        for card in cards:
            title = card.find(  # 餐廳名稱
            "a",class_="jsx-3440511973 title-text").getText()
            stars = card.find(  # 餐廳評價
            "div",class_="jsx-1207467136 text").getText()
            address = card.find(  # 餐廳地址
            "div",class_="jsx-3440511973 address-row").getText()
 
            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title}\n{stars}顆星\n{address} \n\n"
 
        return content
class Dict(Search):
    def scrape(self):
        siml_words = []
        response = requests.get(
        "http://dict.youdao.com/w/eng/"+self.area+"/#keyfrom=dict2.index")
    
        soup = BeautifulSoup(response.content, "html.parser")
        content = ""
        try :            
            #標題
            content+=self.area+'\n'
            try : #kk音標
                kk = soup.find(class_='phonetic').get_text()
                content+="   英"+kk
            except AttributeError:#kk音標找到空
                pass
            #本身翻譯
            s = soup.find(class_='trans-container')('ul')[0]('li')
            #print(s)
            for item in s:
                if item.text:
                    content+=item.text+"\n"
            content+="--------------------------------------\n"
        except IndexError: #index_error:cccccc #沒本身翻譯->使用網路翻譯
            #網路翻譯
            for ex in soup.find_all(class_="wt-container"):  #EX:CCCCCC
                a = 0
                for net_ext in ex.find_all(class_="title",limit=3):
                    a+=1
                    content+=str(int(a))+"."+net_ext.getText().lstrip()
            content+="--------------------------------------\n"
        except TypeError: #type_error:dtreccc(有錯誤修正),yyyyyrtyr(沒有) #搜尋不到
            try:
                #print("error!!!")
                simliar_words = soup.find_all(class_="title",limit=2)
                if(soup.find(class_="error-typo").getText()==""):
                    pass
                else:
                    for sw_s in soup.find_all(class_="error-typo"):    
                        for s_w in simliar_words:
                            #print(s_w.getText()+"!")
                            siml_words.append(s_w.getText())
                    #print("搜尋不到")
                    content = "搜尋不到"
                    return content,siml_words
                #print(siml_words[0])
                #print(soup.find(class_="error-typo").getText())

            except AttributeError:#yyyyyrtyr(沒有)
                print("no result~")
                content = "查無資料~"
                return content,siml_words 

        examples = soup.find_all(id='bilingual',limit=3)
        #print(examples)
        if examples == []:#切換檢索字典例句
            examples = soup.find_all(id='originalSound',limits=3)
            if examples == []:
                examples = soup.find_all(id='authority',limit=3)#fuck
                if examples == []:
                    content+="No examples!" #eggg
                else:
                    content = example_output(examples,content)                 
            else :
                content = example_output(examples,content)
        else:#雙語例句
            for example in examples:
                a = 0
                for p in example.find_all("p",class_=""):
                    a+=1
                    if(a%2!=0):
                        content+=str(int(a/2+1))+"."+p.getText().strip('\n')
                    else : 
                        content+='\n'+p.getText()
        cc = OpenCC('s2twp') #簡體轉繁體
        content = cc.convert(content)
        return content,siml_words
        
def example_output(examples,content):
    for example in examples:
        a = 0
        for p in example.find_all("p",class_=""):
            a+=1
            content+=str(int(a))+"."+p.getText().rstrip()+'\n'
    return content