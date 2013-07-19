
import sys
import markdown
import json
import codecs
from BeautifulSoup import BeautifulSoup

srcdir = sys.argv[1].rstrip("/")
targetdir = sys.argv[2].rstrip("/")

# templates
tmpldir = "./templates/"
articleShareLinks = open(templdir + "articleShareLinks.html")

editionFile = open(srcdir + "/edition.json", "r")
edition = json.loads(editionFile.read())
editionFile.close()


def addStyling(html):
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

def writeArticlePage():


def parseModifiedMarkdown(mmd):
    endJson = mmd.index("}")
    jsonStr = mmd[0:(endJson+1)].lstrip()
    articleObj = json.loads(jsonStr)
    articleObj["markdown"] = mmd[endJson+1:].lstrip().rstrip()
    return articleObj


def renderEmailArticle(md):
    html = markdown.markdown(md)
    htmlStyled = addStyling(html)
    return htmlStyled

articleNames = edition["articles"]
editionHtml = []
for articleName in articleNames:
    articleName = articleName.rstrip(".md") + ".md"
    mdfile = codecs.open(srcdir + "/" + articleName, mode="r", encoding="utf-8")
    mmd = mdfile.read()
    mdfile.close()
    articleObj = parseModifiedMarkdown(mmd)
    articleHtml = renderEmailArticle(articleObj)
    editionHtml.append(articleHtml)

delim = "\n\n\n<br>\n\n\n"
html = delim.join(editionHtml)

htmlFile = codecs.open(srcdir + "/" + srcdir + ".html",
	"w",
	encoding="utf-8", 
    errors="xmlcharrefreplace"
)

htmlFile.write(html)
htmlFile.close()

