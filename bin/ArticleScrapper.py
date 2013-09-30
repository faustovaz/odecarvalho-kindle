import urllib
from bs4 import BeautifulSoup

class ArticleScrapper:
	
	def __init__(self):
		self.url = urllib.urlopen("http://www.olavodecarvalho.org/index.html")
		self.beautifulSoup = BeautifulSoup(self.url)
		self.articles = []

	def loadAllArticlesData(self):
		tables = self.beautifulSoup.find_all('table')
		articleTable = tables[7]
		allLinks = articleTable.find_all('a', {'class' : 'menulink'})
		for link in allLinks:
			words = link.text.splitlines()
			articleName = " ".join(words)
			self.articles.append({'name' : articleName, 'link' : link['href']})

	def start(self):
		pass

	def printArticleData(self):
		for article in self.articles:
			print article['name'] , " , " , article['link']


if __name__ == '__main__':
	scrapper = ArticleScrapper()
	scrapper.loadAllArticlesData()
	scrapper.printArticleData()
