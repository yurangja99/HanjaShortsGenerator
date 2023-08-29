import argparse
from keys import openai_api_key
from crawler.crawler import Crawler
from author.chatgpt import Author
from splitter.splitter import Splitter

parser = argparse.ArgumentParser()
parser.add_argument("keyword", type=str, help="사자성어 혹은 고사성어")
parser.add_argument("--author-model", type=str, choices=["gpt-3.5-turbo"], default="gpt-3.5-turbo", help="대본 작성 AI 모델")
parser.add_argument("--author-temp", type=float, default=0.7, help="대본 작성 AI의 창의성 (0.0 ~ 1.0)")
args = parser.parse_args()

if __name__ == "__main__":
  # crawl data about the keyword
  crawler = Crawler()
  data = crawler.crawl(args.keyword)
  
  # generate script for video
  author = Author(openai_api_key)
  script = author.write_script(data, model=args.author_model, temperature=args.author_temp)
  
  # split script
  splitter = Splitter()
  splitted_script = splitter.split(script)
