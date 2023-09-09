import argparse
from keys import openai_api_key, pixabay_api_key, pexels_api_key
from crawler.crawler import Crawler
from author.author import Author
from splitter.splitter import Splitter
from tts.tts import TTS
from image.imager import Imager

parser = argparse.ArgumentParser()
parser.add_argument("keyword", type=str, help="사자성어 혹은 고사성어")
parser.add_argument("--author-model", type=str, choices=["gpt-3.5-turbo"], default="gpt-3.5-turbo", help="대본 작성 AI 모델")
parser.add_argument("--author-temp", type=float, default=0.7, help="대본 작성 AI의 창의성 (0.0 ~ 1.0)")
parser.add_argument("--width", type=int, default=450, help="영상의 가로 길이")
parser.add_argument("--height", type=int, default=800, help="영상의 세로 길이")
parser.add_argument("--chalkboard", type=str, default="background.png", help="사자성어 소개 장면 배경. default 값 그대로 쓰는 것을 추천.")
parser.add_argument("--font", type=str, default="NanumGothicExtraBold.ttf", help="자막 폰트 파일 위치")
parser.add_argument("--text-chinese-size", type=int, default=127, help="사자성어 소개 장면 한자 크기")
parser.add_argument("--text-korean-size", type=int, default=36, help="사자성어 소개 장면 훈음 크기")
parser.add_argument("--text-chinese-color", type=str, default="black", help="사자성어 소개 장면 한자 색")
parser.add_argument("--generator-model", type=str, choices=["CompVis/stable-diffusion-v1-4"], default="CompVis/stable-diffusion-v1-4", help="이미지 생성 Stable Diffusion 모델")
parser.add_argument("--generator-seed", type=int, default=42, help="이미지 생성 Stable Diffusion seed값")
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
  speakers, scenes = splitter.split(script)

  # generate audio using TTS
  tts = TTS(speakers)
  scenes = tts.read_script(scenes)
  
  # parse or generate images or videos
  imager = Imager(
    openai_api_key=openai_api_key,
    pexels_api_key=pexels_api_key,
    pixabay_api_key=pixabay_api_key,
    target_resolution=(args.width, args.height),
    chalkboard=args.chalkboard,
    font=args.font,
    text_chinese_size=args.text_chinese_size,
    text_korean_size=args.text_korean_size,
    text_chinese_color=args.text_chinese_color,
    sd_model=args.generator_model
  )
  scenes = imager.image(
    data=data,
    speakers=speakers,
    scenes=scenes,
    model=args.author_model,
    temperature=args.author_temp,
    seed=args.generator_seed
  )
