import argparse
import os
from keys import openai_api_key, pixabay_api_key, pexels_api_key
from utils import ChatGPT, save, load
from crawler.crawler import Crawler
from author.author import Author
from splitter.splitter import Splitter
from tts.tts import TTS
from image.imager import Imager
from editor.editor import Editor

parser = argparse.ArgumentParser()
parser.add_argument("keyword", type=str, help="사자성어 혹은 고사성어")
parser.add_argument("--all", action="store_true", help="주어진 사자성어로부터 최종 동영상까지 모든 과정을 수행한다. (--crawler --author --tts --imager --editor 와 같다.)")
parser.add_argument("--crawler", action="store_true", help="Crawler 과정을 수행한다: 사자성어 관련 정보 검색")
parser.add_argument("--author", action="store_true", help="Author 과정을 수행한다: 정보를 보고 대본 작성")
parser.add_argument("--tts", action="store_true", help="TTS 과정을 수행한다: 대본 음성 오디오 생성")
parser.add_argument("--imager", action="store_true", help="Imager 과정을 수행한다: 대본에 맞는 이미지/동영상 검색/제작 (--imager-parser --image-constructor --imager-story --imager-generator와 같다.)")
parser.add_argument("--imager-parser", action="store_true", help="Imager 중 parser 과정을 수행한다: 대본에 맞는 이미지/동영상 검색")
parser.add_argument("--imager-constructor", action="store_true", help="Imager 중 constructor 과정을 수행한다: 대본에 맞는 한자 이미지 생성")
parser.add_argument("--imager-story", action="store_true", help="Imager 중 generator 과정을 위한 사진 설명 생성")
parser.add_argument("--imager-generator", action="store_true", help="Imager 중 generator 과정을 수행한다: 대본에 맞는 이미지 생성")
parser.add_argument("--editor", action="store_true", help="Editor 과정을 수행한다: 동영상 최종 편집")
parser.add_argument("--gpt-model", type=str, choices=["gpt-3.5-turbo"], default="gpt-3.5-turbo", help="ChatGPT 모델")
parser.add_argument("--gpt-temp", type=float, default=0.7, help="ChatGPT 모델 창의성 (0.0 ~ 1.0)")
#parser.add_argument("--sd-model", type=str, choices=["CompVis/stable-diffusion-v1-4", "runwayml/stable-diffusion-v1-5", "stabilityai/stable-diffusion-2-1"], default="CompVis/stable-diffusion-v1-4", help="Stable Diffusion 모델")
parser.add_argument("--sd-model", type=str, choices=["stabilityai/stable-diffusion-xl-base-1.0"], default="stabilityai/stable-diffusion-xl-base-1.0", help="Stable Diffusion 모델")
parser.add_argument("--sd-seed", type=int, default=-1, help="Stable Diffusion seed값 (-1일 경우 random seed)")
parser.add_argument("--width", type=int, default=1080, help="영상의 가로 길이")
parser.add_argument("--height", type=int, default=1920, help="영상의 세로 길이")
parser.add_argument("--chalkboard", type=str, default="background.png", help="사자성어 소개 장면 배경. default 값 그대로 쓰는 것을 추천.")
parser.add_argument("--font", type=str, default="NanumGothicExtraBold.ttf", help="자막 폰트 파일 위치")
parser.add_argument("--text-chinese-size", type=int, default=305, help="사자성어 소개 장면 한자 크기")
parser.add_argument("--text-korean-size", type=int, default=86, help="사자성어 소개 장면 훈음 크기")
parser.add_argument("--text-chinese-color", type=str, default="black", help="사자성어 소개 장면 한자 색")
parser.add_argument("--fps", type=int, default=30, help="영상의 FPS")
parser.add_argument("--text-size", type=int, default=86, help="자막 크기")
parser.add_argument("--text-color", type=str, default="white", help="자막 색깔")
parser.add_argument("--text-stroke-width", type=int, default=5, help="자막 가장자리 두께")
parser.add_argument("--text-stroke-color", type=str, default="black", help="자막 가장자리 색깔")
parser.add_argument("--bgm", type=str, default="bgm.mp3", help="영상 배경음악")
parser.add_argument("--bgm-vol", type=float, default=0.2, help="영상 배경음악 볼륨 조절 (0.0 ~ 1.0)")
args = parser.parse_args()

if __name__ == "__main__":
  # make output directory
  dirpath = os.path.join("video_outputs", args.keyword)
  os.makedirs(dirpath, exist_ok=True)

  # load data
  data, scripts, speakers, scenes, story = load(dirpath)

  # ChatGPT model
  gpt = ChatGPT(
    openai_api_key=openai_api_key,
    model=args.gpt_model,
    temperature=args.gpt_temp
  )
  
  if args.all or args.crawler:
    # crawl data about the keyword
    crawler = Crawler()
    data = crawler.crawl(args.keyword)
    save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.author:
    try:
      # generate script for video
      author = Author(gpt)
      scripts = author.write_script(data)
    except AssertionError:
      print("Can't run Author: Make sure to run: Crawler")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)

    try:
      # split script
      splitter = Splitter()
      speakers, scenes = splitter.split(scripts)
    except AssertionError:
      print("Can't run Splitter: Make sure to run: Crawler, Author")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)

  if args.all or args.tts:
    try:
      # generate audio using TTS
      tts = TTS(speakers)
      scenes = tts.read_script(scenes, dirpath)
    except AssertionError:
      print("Can't run TTS: Make sure to run: Crawler, Author, Splitter")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.imager or args.imager_parser or args.imager_constructor or args.imager_story or args.imager_generator:
    try:
      # instance of Imager
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
    except AssertionError:
      print("Can't run Imager: Make sure to run: Crawler, Author, Splitter")

  if args.all or args.imager or args.imager_parser:
    try:
      # parse images/videos for intro and outro
      scenes = imager.parse(
        scenes=scenes,
        dirpath=dirpath
      )
    except AssertionError:
      print("Can't run Imager-parser: Make sure to run: Crawler, Author, Splitter")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.imager or args.imager_constructor:
    try:
      # construct hanja image
      scenes = imager.construct(
        data=data,
        scenes=scenes,
        dirpath=dirpath
      )
    except AssertionError:
      print("Can't run Imager-constructor: Make sure to run: Crawler, Author, Splitter")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.imager or args.imager_story:
    try:
      # generate story
      story = imager.get_story(
        speakers=speakers,
        scenes=scenes
      )
    except AssertionError:
      print("Can't run Imager-story: Make sure to run: Crawler, Author, Splitter")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.imager or args.imager_generator:
    try:
      # generate images for story
      scenes = imager.generate(
        scenes=scenes,
        story=story,
        dirpath=dirpath,
        seed=args.sd_seed if args.sd_seed > -1 else None
      )
    except AssertionError:
      print("Can't run Imager-generator: Make sure to run: Crawler, Author, Splitter, Imager-story")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
  
  if args.all or args.editor:
    try:
      # generate final video
      editor = Editor(
        target_resolution=(args.width, args.height), 
        fps=args.fps, 
        font=args.font, 
        text_size=args.text_size, 
        text_color=args.text_color, 
        text_stroke_width=args.text_stroke_width, 
        text_stroke_color=args.text_stroke_color
      )
      video_name = editor.edit_video(
        scenes=scenes, 
        dirpath=dirpath,
        bgm=args.bgm,
        bgm_vol=args.bgm_vol
      )
    except AssertionError:
      print("Can't run Editor: Make sure to run: Crawler, Author, Splitter, TTS, Imager")
    finally:
      save(dirpath, data, scripts, speakers, scenes, story)
