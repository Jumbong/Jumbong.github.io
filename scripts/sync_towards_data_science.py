import argparse
import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree

import yaml


AUTHOR_URL = "https://towardsdatascience.com/author/jumbongjunior1999/"
FEED_URL = AUTHOR_URL + "feed/"


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


def read_feed(feed_path):
    if feed_path.suffix == ".json":
        feed_data = json.loads(feed_path.read_text(encoding="utf-8"))
        feed = feed_data.get("feed", {})
        if feed_data.get("status") != "ok" or feed.get("url") != FEED_URL or feed.get("link") != AUTHOR_URL:
            raise ValueError("RSS2JSON did not return the expected author feed.")
        return [
            {
                "link": item["link"],
                "title": item["title"],
                "date": datetime.fromisoformat(item["pubDate"]),
                "topic": next(iter(item.get("categories", [])), ""),
                "description": item.get("description", ""),
            }
            for item in feed_data["items"]
        ]

    channel = ElementTree.parse(feed_path).find("channel")
    if channel is None or channel.findtext("link", "").strip() != AUTHOR_URL:
        raise ValueError("The RSS feed does not belong to the expected author.")
    return [
        {
            "link": item.findtext("link", ""),
            "title": item.findtext("title", ""),
            "date": parsedate_to_datetime(item.findtext("pubDate", "")),
            "topic": item.findtext("category", ""),
            "description": item.findtext("description", ""),
        }
        for item in channel.findall("item")
    ]


def sync_publications(feed_path, catalog_path):
    catalog_text = catalog_path.read_text(encoding="utf-8")
    catalog = yaml.safe_load(catalog_text)
    known_links = {article_url(article["href"]) for article in catalog}
    new_articles = []

    for item in read_feed(feed_path):
        link = article_url(item["link"])
        if link in known_links:
            continue
        title = " ".join(unescape(item["title"]).split())
        if not title:
            raise ValueError(f"The RSS entry has no title: {link}")

        excerpt = ArticleExcerpt()
        excerpt.feed(item["description"])
        excerpt.close()
        new_articles.append({
            "title": title,
            "published": item["date"].date().isoformat(),
            "topic": item["topic"].strip() or "Towards Data Science",
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
