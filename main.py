import argparse
import os
from datetime import datetime
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
parser.add_argument("--start-from", type=str, choices=["keyword", "data", "scripts", "scenes", "audios", "clips"], default="keyword", help="영상 제작 시작 지점. (keyword: 처음부터, data: 크롤링 데이터부터, scripts: 작성된 대본부터, scenes: 장면별로 구분된 대본부터, audios: 대본, 오디오부터, clips: 대본, 오디오, 비디오부터)")
parser.add_argument("--gpt-model", type=str, choices=["gpt-3.5-turbo"], default="gpt-3.5-turbo", help="ChatGPT 모델")
parser.add_argument("--gpt-temp", type=float, default=0.7, help="ChatGPT 모델 창의성 (0.0 ~ 1.0)")
parser.add_argument("--sd-model", type=str, choices=["CompVis/stable-diffusion-v1-4", "runwayml/stable-diffusion-v1-5", "stabilityai/stable-diffusion-2-1"], default="CompVis/stable-diffusion-v1-4", help="Stable Diffusion 모델")
#parser.add_argument("--sd-model", type=str, choices=["stabilityai/stable-diffusion-xl-base-1.0"], default="stabilityai/stable-diffusion-xl-base-1.0", help="Stable Diffusion 모델")
parser.add_argument("--sd-seed", type=int, default=-1, help="Stable Diffusion seed값 (-1일 경우 random seed)")
parser.add_argument("--width", type=int, default=900, help="영상의 가로 길이")
parser.add_argument("--height", type=int, default=1600, help="영상의 세로 길이")
parser.add_argument("--chalkboard", type=str, default="background.png", help="사자성어 소개 장면 배경. default 값 그대로 쓰는 것을 추천.")
parser.add_argument("--font", type=str, default="NanumGothicExtraBold.ttf", help="자막 폰트 파일 위치")
parser.add_argument("--text-chinese-size", type=int, default=254, help="사자성어 소개 장면 한자 크기")
parser.add_argument("--text-korean-size", type=int, default=72, help="사자성어 소개 장면 훈음 크기")
parser.add_argument("--text-chinese-color", type=str, default="black", help="사자성어 소개 장면 한자 색")
parser.add_argument("--fps", type=int, default=30, help="영상의 FPS")
parser.add_argument("--text-size", type=int, default=72, help="자막 크기")
parser.add_argument("--text-color", type=str, default="white", help="자막 색깔")
parser.add_argument("--text-stroke-width", type=int, default=2, help="자막 가장자리 두께")
parser.add_argument("--text-stroke-color", type=str, default="black", help="자막 가장자리 색깔")
parser.add_argument("--bgm", type=str, default="bgm.mp3", help="영상 배경음악")
parser.add_argument("--bgm-vol", type=float, default=0.2, help="영상 배경음악 볼륨 조절 (0.0 ~ 1.0)")
args = parser.parse_args()

if __name__ == "__main__":
  # make output directory
  dirpath = os.path.join("video_outputs", args.keyword)
  os.makedirs(dirpath, exist_ok=True)

  # ChatGPT model
  gpt = ChatGPT(
    openai_api_key=openai_api_key,
    model=args.gpt_model,
    temperature=args.gpt_temp
  )
  
  if args.start_from in ["keyword"]:
    # crawl data about the keyword
    crawler = Crawler()
    data = crawler.crawl(args.keyword)
    save(dirpath, data, None, None, None)
  else:
    data, _, _, _ = load(dirpath)
  
  if args.start_from in ["keyword", "data"]:
    # generate script for video
    author = Author(gpt)
    scripts = author.write_script(data)
    save(dirpath, data, scripts, None, None)
  else:
    data, scripts, _, _ = load(dirpath)

  if args.start_from in ["keyword", "data", "scripts"]:
    # split script
    splitter = Splitter()
    speakers, scenes = splitter.split(scripts)
    save(dirpath, data, scripts, speakers, scenes)
  else:
    data, scripts, speakers, scenes = load(dirpath)

  if args.start_from in ["keyword", "data", "scripts", "scenes"]:
    # generate audio using TTS
    tts = TTS(speakers)
    scenes = tts.read_script(scenes, dirpath)
    save(dirpath, data, scripts, speakers, scenes)
  else:
    data, scripts, speakers, scenes = load(dirpath)
  
  if args.start_from in ["keyword", "data", "scripts", "scenes", "audios"]:
    # if seed is -1, random seed
    seed = args.sd_seed if args.sd_seed > -1 else int(datetime.now().timestamp())
    print("Stable Diffusion seed:", seed)
    
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
      seed=seed,
      dirpath=dirpath
    )
    save(dirpath, data, scripts, speakers, scenes)
  else:
    data, scripts, speakers, scenes = load(dirpath)
  
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
