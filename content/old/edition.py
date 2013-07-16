
import sys
import markdown
import json
import codecs
from BeautifulSoup import BeautifulSoup

dirname = sys.argv[1].rstrip("/")

articleNamesFile = open(dirname + "/edition.json", "r")
articles = json.loads(articleNamesFile.read())
articleNamesFile.close()

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
    #mdfile = open(dirname + "/" + article, "r")
    mdfile = codecs.open(dirname + "/" + article, mode="r", encoding="utf-8")
    #md = unicode(mdfile.read(), errors="replace")
    md = mdfile.read()
    mdfile.close()
    html = markdown.markdown(md)
    htmlStyled = addStyling(html)
    articlesHtml.append(htmlStyled)

delim = "\n\n\n<br>\n\n\n"
html = delim.join(articlesHtml)

#htmlFile = open(dirname + "/" + dirname + ".html", "w")

htmlFile = codecs.open(dirname + "/" + dirname + ".html",
	"w",
	encoding="utf-8", 
    errors="xmlcharrefreplace"
)

htmlFile.write(html)
htmlFile.close()

