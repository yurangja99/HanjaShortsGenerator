import argparse
from keys import openai_api_key, pixabay_api_key, pexels_api_key
from utils import ChatGPT
from crawler.crawler import Crawler
from author.author import Author
from splitter.splitter import Splitter
from tts.tts import TTS
from image.imager import Imager
from editor.editor import Editor

parser = argparse.ArgumentParser()
parser.add_argument("keyword", type=str, help="사자성어 혹은 고사성어")
parser.add_argument("--gpt-model", type=str, choices=["gpt-3.5-turbo"], default="gpt-3.5-turbo", help="ChatGPT 모델")
parser.add_argument("--gpt-temp", type=float, default=0.7, help="ChatGPT 모델 창의성 (0.0 ~ 1.0)")
parser.add_argument("--sd-model", type=str, choices=["CompVis/stable-diffusion-v1-4"], default="CompVis/stable-diffusion-v1-4", help="Stable Diffusion 모델")
parser.add_argument("--sd-seed", type=int, default=42, help="Stable Diffusion seed값")
parser.add_argument("--width", type=int, default=450, help="영상의 가로 길이")
parser.add_argument("--height", type=int, default=800, help="영상의 세로 길이")
parser.add_argument("--chalkboard", type=str, default="background.png", help="사자성어 소개 장면 배경. default 값 그대로 쓰는 것을 추천.")
parser.add_argument("--font", type=str, default="NanumGothicExtraBold.ttf", help="자막 폰트 파일 위치")
parser.add_argument("--text-chinese-size", type=int, default=127, help="사자성어 소개 장면 한자 크기")
parser.add_argument("--text-korean-size", type=int, default=36, help="사자성어 소개 장면 훈음 크기")
parser.add_argument("--text-chinese-color", type=str, default="black", help="사자성어 소개 장면 한자 색")
parser.add_argument("--fps", type=int, default=10, help="영상의 FPS")
parser.add_argument("--text-size", type=int, default=14, help="자막 크기")
parser.add_argument("--text-color", type=str, default="black", help="자막 색깔")
args = parser.parse_args()

if __name__ == "__main__":
  # ChatGPT model
  gpt = ChatGPT(
    openai_api_key=openai_api_key,
    model=args.gpt_model,
    temperature=args.gpt_temp
  )
  
  # crawl data about the keyword
  crawler = Crawler()
  data = crawler.crawl(args.keyword)
  
  # generate script for video
  author = Author(gpt)
  script = author.write_script(data)
  
  # split script
  splitter = Splitter()
  speakers, scenes = splitter.split(script)

  # generate audio using TTS
  tts = TTS(speakers)
  scenes = tts.read_script(scenes, data["keyword"])
  
  # parse or generate images or videos
  imager = Imager(
    gpt_model=gpt,
    pexels_api_key=pexels_api_key,
    pixabay_api_key=pixabay_api_key,
    target_resolution=(args.width, args.height),
    chalkboard=args.chalkboard,
    font=args.font,
    text_chinese_size=args.text_chinese_size,
    text_korean_size=args.text_korean_size,
    text_chinese_color=args.text_chinese_color,
    sd_model=args.sd_model
  )
  scenes = imager.image(
    data=data,
    speakers=speakers,
    scenes=scenes,
    seed=args.sd_seed
  )
  
  # generate final video
  editor = Editor(
    target_resolution=(args.width, args.height), 
    background_image=args.chalkboard, 
    fps=args.fps, 
    text_size=args.text_size, 
    text_color=args.text_color
  )
  video_name = editor.edit_video(scenes, args.keyword)
