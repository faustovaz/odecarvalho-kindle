#! /usr/bin/env python
#-*- coding: utf-8 -*-

import urllib
import os
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import re


def htmlScape(text):
	dictionary = {
		'á' : 	'&aacute;',
		'é' :	'&eacute;',
		'í' :	'&iacute;',
		'ó' :	'&oacute;',
		'ú' :	'&uacute;',
		'Á'	:	'&Aacute;',
		'É'	:	'&Eacute;',
		'Í'	:	'&Iacute;',
		'Ó'	:	'&Oacute;',
		'Ú'	:	'&Uacute;',
		'â'	:	'&acirc;',
		'ê'	:	'&ecirc;',
		'î'	:	'&icirc;',
		'ô'	:	'&ocirc;',
		'û'	:	'&ucirc;',
		'Â'	:	'&Acirc;',
		'Ê'	:	'&Ecirc;',
		'Î'	:	'&Icirc;',
		'Ô'	:	'&Ocirc;',
		'Û'	:	'&Ucirc;',
		'ã'	:	'&atilde;',
		'õ'	:	'&otilde;',
		'Ã'	:	'&Atilde;',
		'Õ'	:	'&Otilde;',
		'Ç'	:	'&Ccedil;',
		'ç'	:	'&ccedil;',
		'À'	:	'&Agrave;',
		'à'	:	'&agrave;',
		'—'	:	'&#8212;',
		'&ndash;' : '&#8212;'
	}

	for key, value in dictionary.iteritems():
		text = text.replace(key, value)
	return text

def eliminateHTMLBadTags(text):
	soup = BeautifulSoup(text)
	divs = soup.find_all('divs')
	regex = re.compile(r'^[\s\n]*$')
	for div in divs:
		divText = div.get_gext()
		if not divText or regex.match(divText):
			div.replace_with("")
	text = soup.prettify()
	text = re.sub(r'(.?)(&nbsp;)+(.?)', r'\1&nbsp;\3',text)
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
			articles.append({'title' : articleName.encode('utf-8'), 'link' : link['href']})
		return articles

	def loadFullArticlesData(self):
		articles = self.getAllArticlesListed()
		for article in articles:
			beautifulSoup = self.getScrapper(self.address + article['link'])
			table = beautifulSoup.find('table')
			table_tds = table.find_all('td')
			try:
				td = table_tds[1]
				paragraphs = td.find_all('p')
				divs = td.find_all('div')
				if len(divs) > 0:
					html_date = paragraphs[2]
					html_article = divs[0]
					title = unicode(article['title'], 'utf-8')
					title = htmlScape(title.encode('utf-8'))
					print title
					article_data = html_date.text.split("\n")
					newspaper = htmlScape(article_data[0].encode('utf-8'))
					date = htmlScape(article_data[1].encode('utf-8'))
					html_article = eliminateHTMLBadTags(html_article.encode('utf-8'))
					html_article = htmlScape(html_article.encode('utf-8'))
					self.fullArticles.append({	'title' : unicode(title, 'utf-8'), 
												'date' : unicode(date, 'utf-8'), 
												'newspaper' : unicode(newspaper, 'utf-8'), 
												'text' : unicode(html_article, 'utf-8')
											})
					#Due to some strange changes in some html file of some articles,
					#I hardcoded this to get only the articles written by Olavo and available
					#in the "What's new section".
					if (title == "Excesso de democracia"):
						break
			except Exception:
				print "Fail to get article: ", article['title']

	def generateArticlesFile(self):
		self.loadFullArticlesData()
		templateEngine = TemplateEngine()
		templateEngine.generateHTMLFile(self.fullArticles)


class TemplateEngine:

	def generateHTMLFile(self, data):
		template = self.getTemplate()
		ouput = template.render(articles=data)
		with open(self.getPath() + "/template/pre-kindle-output.html", "w") as htmlFile:
			htmlFile.write(ouput.encode('utf-8'))

	def getTemplate(self):
		environment = Environment(loader=FileSystemLoader(self.getPath() + "/template"))
		return environment.get_template("skeleton.html")

	def getPath(self):
		scriptDirPath = os.path.dirname(os.path.realpath(__file__))
		dirPathSplitted = scriptDirPath.split("/")
		dirPathSplitted.pop()
		return "/".join(dirPathSplitted)




if __name__ == '__main__':
	a = ArticleScrapper()
	a.generateArticlesFile()

