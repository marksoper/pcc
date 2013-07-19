
import sys
import markdown
import json
import codecs
from BeautifulSoup import BeautifulSoup

srcdir = sys.argv[1].rstrip("/")
targetdir = sys.argv[2].rstrip("/")

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



articlesHtml = []
for article in articles:
    mdfile = codecs.open(srcdir + "/" + article, mode="r", encoding="utf-8")
    md = mdfile.read()
    mdfile.close()
    html = markdown.markdown(md)
    htmlStyled = addStyling(html)
    articlesHtml.append(htmlStyled)

delim = "\n\n\n<br>\n\n\n"
html = delim.join(articlesHtml)

htmlFile = codecs.open(srcdir + "/" + srcdir + ".html",
	"w",
	encoding="utf-8", 
    errors="xmlcharrefreplace"
)

htmlFile.write(html)
htmlFile.close()

