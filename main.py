import argparse
from crawler.crawler import Crawler

parser = argparse.ArgumentParser()
parser.add_argument("keyword", type=str, help="사자성어 혹은 고사성어")
args = parser.parse_args()

if __name__ == "__main__":
  # crawl data about the keyword
  crawler = Crawler()
  data = crawler.crawl(args.keyword)
  