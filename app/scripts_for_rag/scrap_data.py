from requests_html import HTMLSession 


class extract_web_data:
    def __init__(self):
        
        self.web_service=HTMLSession()


    def get_articles_search(self,topic:str):
        url_base='https://www.popularmechanics.com/search/?q='
        url=url_base+topic
        web_response=self.web_service.get(url)
        urls=[]
        titles=[]
        data_urls=web_response.html.find("a.ee4ms352.css-1objo0p.e1c1bym14")
        data_titles=web_response.html.find("span.css-huxaxc.e10ip9lg5")
        for link in data_urls:
            urls.append(link.attrs["data-vars-ga-outbound-link"])
        
        for title in data_titles:
            titles.append(title.text)    
        return urls,titles

        
        
    def get_text_article(self,url):
            
        web_response=self.web_service.get(url)
        text=web_response.html.find("p[data-node-id]")
        hl=web_response.html.find("p")[0]
        return text,hl
    def get_title_article(self,url):
        web_response=self.web_service.get(url)
        data=web_response.html.find('h1.css-1uosn6.e1f1sunr8', first=True)
        
        return data.text
    def get_article_images(self,url):
        web_response=self.web_service.get(url)
        data=web_response.html.find('img.css-0.e1g79fud0')
        return data
    def get_article(self,url):
        article=dict()
        images=[]
        paraphs,hl=self.get_text_article(url)
        article["title"]=self.get_title_article(url)
        article["highlight"]=hl.text
        imgs=self.get_article_images(url)
        text=""     
        for paraph in paraphs:
            text+=f"{paraph.text}\n"
        article["content"]=text
        for image in imgs:
            images.append(image.attrs["src"])
        article["images"]=images    
        return article
    


obj=extract_web_data()
urls,titles=obj.get_articles_search("ai")
print(urls[0],titles[0]) 

