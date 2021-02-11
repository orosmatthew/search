import requests
from urllib.parse import urlparse
from html.parser import HTMLParser
import keyboard
import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

init_url = "google.com"

url_queue = []

url_list = []

urls_txt = open(os.path.join(__location__, 'urls.txt'), "r", encoding="utf-8")
done_urls_txt = open(os.path.join(__location__, 'done_urls.txt'), "r", encoding="utf-8")

url_lines = urls_txt.read().split("\n")
done_urls_lines = done_urls_txt.read().split("\n")

urls_txt.close()
done_urls_txt.close()

for u in url_lines:
    if u not in done_urls_lines:
        url_queue.append(u)
    url_list.append(u)


class MyHTMLParser(HTMLParser):

    def error(self, message):
        print("Parse Error!: " + message)

    def __init__(self):
        super().__init__()
        self.tag_data = []
        self.save_tags = ['h1', 'h2', 'h3', 'title', 'meta', 'a']
        self.heading_tags = ['h1', 'h2', 'h3']
        self.curr_tag = ""
        self.curr_attrs = ""
        self.curr_data = ""

        self.links = []
        self.word_list = []
        self.title = ""
        self.og_title = ""
        self.meta_title = ""
        self.description = ""

    @staticmethod
    def _clean_url(u):
        return u.replace("www.", "")

    @staticmethod
    def _make_keywords(s):
        w_list = []
        s_list = re.split("[ \n]", s)
        for d in s_list:
            if re.match("^[A-Za-z0-9'\\\_-]*$", d):
                if d not in w_list:
                    w_list.append(d.lower())
        return w_list

    @staticmethod
    def _make_alphanumerical(s):
        s = re.sub(r'[^a-zA-Z0-9_ |+-=]', '', s)
        return s

    def process_tag_data(self):
        for t in self.tag_data:
            tag = t[0]
            attrs = t[1]
            data = t[2]
            if tag == "title":
                self.title = self._make_alphanumerical(data)
                for w in self._make_keywords(data):
                    if not w in self.word_list:
                        self.word_list.append(w)
            if tag == "meta":
                if len(attrs) >= 2:
                    if attrs[0][1] == "description":
                        for a in attrs:
                            if a[0] == "content":
                                self.description = self._make_alphanumerical(a[1])
                                for w in self._make_keywords(self.description):
                                    if not w in self.word_list:
                                        self.word_list.append(w)
                    if attrs[0][1] == "og:site_name":
                        for a in attrs:
                            if a[0] == "content":
                                self.og_title = self._make_alphanumerical(a[1])
                                for w in self._make_keywords(self.og_title):
                                    if not w in self.word_list:
                                        self.word_list.append(w)
                    if attrs[0][1] == "og:title":
                        for a in attrs:
                            if a[0] == "content":
                                self.meta_title = self._make_alphanumerical(a[1])
                                for w in self._make_keywords(self.meta_title):
                                    if not w in self.word_list:
                                        self.word_list.append(w)
            if tag in self.heading_tags:
                for w in self._make_keywords(self._make_alphanumerical(data)):
                    if not w in self.word_list:
                        self.word_list.append(w)
            if tag == "a":
                for a in attrs:
                    if a[0] == "href":
                        url = urlparse(a[1]).hostname
                        if url != None:
                            url = self._clean_url(url)
                            if not url in self.links:
                                self.links.append(url)

    def handle_starttag(self, tag, attrs):
        self.curr_tag = tag
        self.curr_attrs = attrs
        self.curr_data = ""

    def handle_endtag(self, tag):
        if tag == self.curr_tag:
            if self.curr_tag in self.save_tags:
                self.tag_data.append([self.curr_tag, self.curr_attrs, self.curr_data])

    def handle_data(self, data):
        self.curr_data = data


urls_txt = open(os.path.join(__location__, 'urls.txt'), "a", encoding="utf-8")
done_urls_txt = open(os.path.join(__location__, 'done_urls.txt'), "a", encoding="utf-8")
data_txt = open(os.path.join(__location__, 'data.txt'), "a", encoding="utf-8")
dis_txt = open(os.path.join(__location__, 'dis.txt'), "a", encoding="utf-8")
connections_txt = open(os.path.join(__location__, 'connections.txt'), "a", encoding="utf-8")


def add_escapes(s):
    s = s.replace("\\", "\\\\")
    s = s.replace("%", "\\%")
    s = s.replace("_", "\\_")
    s = s.replace("'", "\\'")
    s = s.replace("\"", "\\\"")
    s = s.replace("\n", "")
    s = s.replace("\t", "")
    return s


if len(url_queue) == 0:
    url_queue.append(init_url)
    url_list.append(init_url)
    urls_txt.write(init_url + "\n")

while len(url_queue) != 0:

    urls_txt.close()
    done_urls_txt.close()
    data_txt.close()
    dis_txt.close()
    connections_txt.close()

    urls_txt = open(os.path.join(__location__, 'urls.txt'), "a", encoding="utf-8")
    done_urls_txt = open(os.path.join(__location__, 'done_urls.txt'), "a", encoding="utf-8")
    data_txt = open(os.path.join(__location__, 'data.txt'), "a", encoding="utf-8")
    dis_txt = open(os.path.join(__location__, 'dis.txt'), "a", encoding="utf-8")
    connections_txt = open(os.path.join(__location__, 'connections.txt'), "a", encoding="utf-8")

    if keyboard.is_pressed('q'):
        break

    url = url_queue[0]

    done_urls_txt.write(url + "\n")


    print("Total URLs: " + str(len(url_list)))
    print("Done URLs: " + str(len(url_list)-len(url_queue)))
    print("Queue List: " + str(len(url_queue)))

    print("Requesting: " + url + "\n")

    url_queue.pop(0)

    try:
        response = requests.get("http://" + url)
    except:
        print("Cannot reach site")
        dis_txt.write(url + "\n")
        continue

    try:
        parser = MyHTMLParser()
        parser.feed(response.text)
        parser.process_tag_data()


        for l in parser.links:
            conn = (add_escapes(str(url)).strip() + " " + add_escapes(str(l)).strip())
            connections_txt.write(conn + "\n")
            if not l in url_list:
                url_queue.append(l)
                url_list.append(l)
                urls_txt.write(l + "\n")



        if parser.og_title != "":
            title = parser.og_title
        elif parser.meta_title != "":
            title = parser.meta_title
        elif parser.title != "":
            title = parser.title
        else:
            title = str(url)

        keywords = ""
        for w in parser.word_list:
            keywords += w + " "

        command = (add_escapes(str(url)).strip() + "#" +
                   add_escapes(str(title)).strip() + "#" +
                   add_escapes(str(keywords)).strip())
        data_txt.write(command + "\n")
    except:
        print("cannot decode")
        dis_txt.write(url + "\n")
        continue

urls_txt.close()
done_urls_txt.close()
data_txt.close()
dis_txt.close()
connections_txt.close()
