import argparse
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree

import yaml


AUTHOR_URL = "https://towardsdatascience.com/author/jumbongjunior1999/"


class ArticleExcerpt(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_paragraph = False
        self.finished = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "p" and not self.finished:
            self.in_paragraph = True

    def handle_endtag(self, tag):
        if tag == "p" and self.in_paragraph:
            self.in_paragraph = False
            self.finished = True

    def handle_data(self, data):
        if self.in_paragraph:
            self.parts.append(data)


def article_url(link):
    url = urlsplit(link.strip())
    if url.scheme != "https" or url.netloc.lower() != "towardsdatascience.com":
        raise ValueError(f"Unexpected article URL: {link}")
    return urlunsplit(("https", "towardsdatascience.com", url.path.rstrip("/") + "/", "", ""))


def sync_publications(feed_path, catalog_path):
    channel = ElementTree.parse(feed_path).find("channel")
    if channel is None or channel.findtext("link", "").strip() != AUTHOR_URL:
        raise ValueError("The RSS feed does not belong to the expected author.")

    catalog_text = catalog_path.read_text(encoding="utf-8")
    catalog = yaml.safe_load(catalog_text)
    known_links = {article_url(article["href"]) for article in catalog}
    new_articles = []

    for item in channel.findall("item"):
        link = article_url(item.findtext("link", ""))
        if link in known_links:
            continue
        title = " ".join(unescape(item.findtext("title", "")).split())
        if not title:
            raise ValueError(f"The RSS entry has no title: {link}")

        excerpt = ArticleExcerpt()
        excerpt.feed(item.findtext("description", ""))
        excerpt.close()
        new_articles.append({
            "title": title,
            "published": parsedate_to_datetime(item.findtext("pubDate", "")).date().isoformat(),
            "topic": item.findtext("category", "").strip() or "Towards Data Science",
            "summary": " ".join("".join(excerpt.parts).split()),
            "summary-lang": "en",
            "href": link,
        })
        known_links.add(link)

    if new_articles:
        additions = yaml.safe_dump(new_articles, allow_unicode=True, sort_keys=False)
        catalog_path.write_text(catalog_text.rstrip("\n") + "\n" + additions, encoding="utf-8")
    return len(new_articles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("feed", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path("publications.yml"))
    args = parser.parse_args()
    print(f"Added {sync_publications(args.feed, args.catalog)} Towards Data Science publications.")
