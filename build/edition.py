
import sys
import markdown
import json
import codecs
from BeautifulSoup import BeautifulSoup
import pystache
from datetime import datetime

srcdir = sys.argv[1].rstrip("/")
targetdir = sys.argv[2].rstrip("/")

# templates
tmpldir = "./templates/"
emailArticleTemplate = open(tmpldir + "emailArticle.html").read()

editionFile = open(srcdir + "/edition.json", "r")
edition = json.loads(editionFile.read())
editionFile.close()


def urlify(s):
    t = '-'.join(s.split())
    u = ''.join([c for c in t if c.isalnum() or c=='-'])
    u = u + ".html"
    return u

def generateEditionUrl(edition):
    pub = datetime.strptime(edition["pubDate"], "%B %d, %Y")
    url = "/" + datetime.strftime(pub, "%Y") + "/" + datetime.strftime(pub, "%m") + "/" + datetime.strftime(pub, "%d")
    url = url + "/" + "newsletter" + "/" + urlify(edition["subject"])

edition["url"] = generateEditionUrl(edition)

def addEmailStyling(html):
    soup = BeautifulSoup(html)
    # style images
    imgstyle = "float: right; width: 200px; margin: 0 20px"
    imgs = soup.findAll("img")
    for img in imgs:
        img.attrs.append(("style", imgstyle))
    # style h2 tags
    h2style = "clear:both; font-size: 18px; margin-top: 15px"
    h2s = soup.findAll("h2")
    for h2 in h2s:
        h2.attrs.append(("style", h2style))
    htmlStyled = str(soup).decode("UTF-8", "replace")
    return htmlStyled

def writeArticlePage(articleObj):
    pass


def parseModifiedArticleMarkdown(mmd):
    endJson = mmd.find("}")
    if endJson > 0:
        jsonStr = mmd[0:(endJson+1)].lstrip()
        articleObj = json.loads(jsonStr)
        articleObj["markdown"] = mmd[endJson+1:].lstrip().rstrip()
        return articleObj
    print "WARNING: Article not handled: " + mmd
    return None


def renderEmailArticle(articleObj):
    articleObj["content"] = markdown.markdown(articleObj["markdown"])
    unstyledHtml = pystache.render(emailArticleTemplate, articleObj)
    articleObj["emailHtml"] = addEmailStyling(unstyledHtml)
    return articleObj["emailHtml"]

articleNames = edition["articles"]
articlesHtml = []
for articleName in articleNames:
    articleName = articleName.rstrip(".md") + ".md"
    mdfile = codecs.open(srcdir + "/" + articleName, mode="r", encoding="utf-8")
    mmd = mdfile.read()
    mdfile.close()
    articleObj = parseModifiedArticleMarkdown(mmd)
    if articleObj is None:
        continue
    articleHtml = renderEmailArticle(articleObj)
    articlesHtml.append(articleHtml)
    writeArticlePage(articleObj)

delim = "\n\n\n<br>\n\n\n"
edition["emailHtml"] = delim.join(articlesHtml)

editionEmailFile = codecs.open(targetdir + "/" + edition["url"],
	"w",
	encoding="utf-8", 
    errors="xmlcharrefreplace"
)

editionEmailFile.write(edition["emailHtml"])
editionEmailFile.close()

def writeEditionPage(edition):
    pass

#writeEditionPage(edition)

