import sys
import urllib.request
import ssl
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_body = False
        self.title_text = ""
        self.body_text = ""
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

        if tag == "body":
            self.in_body = True

        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data.strip()

        if self.in_body:
            text = data.strip()
            if text:
                self.body_text += text + " "


def execute_scraper():
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <URL>")
        return

    url = sys.argv[1]

    if not url.startswith("http"):
        url = "https://" + url

    try:
        context = ssl._create_unverified_context()

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response = urllib.request.urlopen(request, context=context)
        html_content = response.read().decode("utf-8", errors="ignore")

    except Exception:
        print("Error fetching URL")
        return

    parser = MyHTMLParser()
    parser.feed(html_content)

    print(parser.title_text.strip())
    print(parser.body_text.strip())

    for link in parser.links:
        print(link)


if __name__ == "__main__":
    execute_scraper()
