import urllib
from bs4 import BeautifulSoup

class ArticleScrapper:
	
	def __init__(self):
		self.address = "http://www.olavodecarvalho.org/"
		self.fullArticles = []

	def getScrapper(self, link):
		url = urllib.urlopen(link)
		return BeautifulSoup(url)

	def getAllArticlesListed(self):
		articles = []
		beautifulSoup = self.getScrapper(self.address + "index.html")
		tables = beautifulSoup.find_all('table')
		articleTable = tables[7]
		allLinks = articleTable.find_all('a', {'class' : 'menulink'})
		for link in allLinks:
			words = link.text.splitlines()
			articleName = " ".join(words)
			articles.append({'name' : articleName.encode('utf-8'), 'link' : link['href']})
		return articles

	def getFullArticlesData(self):
		articles = self.getAllArticlesListed()
		for article in articles:
			beautifulSoup = self.getScrapper(self.address + article['link'])
			table = beautifulSoup.find('table')
			table_tds = table.find_all('td')
			td = table_tds[1]
			paragraphs = td.find_all('p')
			divs = td.find_all('div')

			if len(divs) > 0:
				html_title = paragraphs[1]
				html_date = paragraphs[2]
				html_article = divs[0]
			
				title = html_title.text.split("\n")
				article_data = html_date.text.split("\n")
			
				title = title[0]
				newspaper = article_data[0]
				date = article_data[1]

				self.fullArticles.append({	'title' : unicode(title), 
											'date' : unicode(date), 
											'newspaper' : unicode(newspaper), 
											'text' : unicode(html_article)
										})




	def printAllData(self):
		self.getFullArticlesData()
		for article in self.fullArticles:
			print article['title']
			print article['date']
			print article['newspaper']
			print '\n\n'


if __name__ == '__main__':
	a = ArticleScrapper()
	a.printAllData()

