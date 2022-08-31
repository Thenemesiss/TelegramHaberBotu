
from time import sleep
from threading import Thread
from requests import post, get
from json import loads
from xmltodict import parse



class getLastNews(object):
    def __init__(self, url: str, news_address: str) -> None:
        self.url = url
        self.newsAddress = news_address

    def read_json_config(self):
        return loads(open("config.json", "r", encoding="utf-8").read())

        
    def sendPhotoFromTg(self ,chat: str, photo: str, caption: str, token: str):
        payload = {
            "chat_id": chat ,
            "photo": photo,
            "caption": caption

        }

        post(f"https://api.telegram.org/bot{token}/sendPhoto", data=payload)

    def getLastContent(self ,url: str, image: str, image_url:str, caption: str, title:str) -> str: 
        json_content = get(url=url)
        if json_content.status_code == 200:
            parse_json = parse(json_content.text)
            getLastTopic = parse_json["rss"]["channel"]["item"][0]
            getLastTitle = getLastTopic[title]
            getLastImage = getLastTopic[image][image_url]
            getLastContent = getLastTopic[caption][0:300]
            return getLastContent, getLastTitle, getLastImage

    def News(self) -> str:
        channelId = self.read_json_config()["channel_id"]
        bot_token = self.read_json_config()["token"]


        last = None
        while True:
            try:
                lastContent, lastTitle, ImageUrl = self.getLastContent(url=self.url, title="title", caption="description", image="media:content", image_url="@url")
                if lastContent is not None and  lastTitle is not None and ImageUrl is not None:
                    send_content = f"----{lastTitle}----\n\n{lastContent}\n\nKaynak : | {self.newsAddress} |"
                    if lastTitle != last:
                        last = lastTitle
                        self.sendPhotoFromTg(token=bot_token, chat=channelId, caption=send_content, photo=ImageUrl)
                        sleep(10)

                

            except: continue

lastContentHaberler = getLastNews(url="https://rss.haberler.com/rss.asp", news_address="Haberler.com")
lastContentSondakika = getLastNews(url="http://rss.sondakika.com/rss.asp", news_address="Sondakika.com")

if __name__ == "__main__":
    Thread(target=lastContentSondakika.News, args=()).start()
    Thread(target=lastContentHaberler.News, args=()).start()

