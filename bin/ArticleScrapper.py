#-*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def htmlScape(text):
	dictionary = {
		'á' : 	'&aacute',
		'é' :	'&eacute',
		'í' :	'&iacute',
		'ó' :	'&oacute',
		'ú' :	'&uacute',
		'Á'	:	'&Aacute',
		'É'	:	'&Eacute',
		'Í'	:	'&Iacute',
		'Ó'	:	'&Oacute',
		'Ú'	:	'&Uacute',
		'â'	:	'&acirc',
		'ê'	:	'&ecirc',
		'î'	:	'&icirc',
		'ô'	:	'&ocirc',
		'û'	:	'&ucirc',
		'Â'	:	'&Acirc',
		'Ê'	:	'&Ecirc',
		'Î'	:	'&Icirc',
		'Ô'	:	'&Ocirc',
		'Û'	:	'&Ucirc',
		'ã'	:	'&atilde',
		'õ'	:	'&otilde',
		'Ã'	:	'&Atilde',
		'Õ'	:	'&Otilde',
		'Ç'	:	'&Ccedil',
		'ç'	:	'&ccedil'

	}
	for key, value in dictionary.iteritems():
		text = text.replace(key, value)
	return text


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

	def loadFullArticlesData(self):
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
			
				print title[0]
				title = htmlScape(title[0].encode('utf-8'))
				newspaper = htmlScape(article_data[0].encode('utf-8'))
				date = htmlScape(article_data[1].encode('utf-8'))

				self.fullArticles.append({	'title' : unicode(title, 'utf-8'), 
											'date' : unicode(date, 'utf-8'), 
											'newspaper' : unicode(newspaper, 'utf-8'), 
											'text' : html_article
										})

	def generateArticlesFile(self):
		self.loadFullArticlesData()
		templateEngine = TemplateEngine()
		templateEngine.generateHTMLFile(self.fullArticles)


	def printAllData(self):
		self.getFullArticlesData()
		for article in self.fullArticles:
			print article['title']
			print article['date']
			print article['newspaper']
			print '\n\n'


class TemplateEngine:

	def generateHTMLFile(self, data):
		template = self.getTemplate()
		ouput = template.render(articles=data)
		with open("../template/pre-kindle-ouput.html", "w") as htmlFile:
			htmlFile.write(ouput.encode('utf-8'))

	def getTemplate(self):
		environment = Environment(loader=FileSystemLoader("../template"))
		return environment.get_template("skeleton.html")



if __name__ == '__main__':
	a = ArticleScrapper()
	a.generateArticlesFile()

