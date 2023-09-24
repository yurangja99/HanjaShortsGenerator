import numpy as np
import os
from PIL import ImageFont, ImageDraw, Image
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import concatenate_videoclips, concatenate_audioclips, CompositeVideoClip, CompositeAudioClip, afx
from skimage.filters import gaussian

class Editor(object):
  def __init__(
    self, 
    target_resolution: tuple, 
    fps: int, 
    font: str,
    text_size: int, 
    text_color: str, 
    text_stroke_width: int, 
    text_stroke_color: str
  ):
    """
    Initialize Editor. 

    Args:
        target_resolution (tuple): (width, height) of the editted video. 
        fps (int): fps of the video. 
        font (str): path to the font file. 
        text_size (int): size of the subtitle. 
        text_color (str): color of the subtitle. 
        text_stroke_width (int): width of the stroke of the subtitle. 
        text_stroke_color (str): color of the stroke of the subtitle.
    """
    self.target_resolution = target_resolution
    self.fps = fps
    self.text_size = text_size
    self.text_color = text_color
    self.font = ImageFont.truetype(font, size=text_size)
    self.max_text_cnt = target_resolution[0] // text_size
    self.text_stroke_width = text_stroke_width
    self.text_stroke_color = text_stroke_color
  
  def __is_image(self, image_name: str):
    """
    Determine whether given name is image or video. 

    Args:
        image_name (str): file name
    
    Return:
        return (bool): True if image, False otherwise (of course, video.)
    """
    return image_name.endswith(("bmp", "jpg", "jpeg", "gif", "png", "tif", "wmf", "emf"))
  
  def __fit_image_or_video_in_screen(self, image: ImageClip | VideoFileClip):
    """
    Fit given image or video into target resolution. 
    Ratio will be kept during resizing, and rest of the part would be blurred image. 

    Args:
        image (ImageClip | VideoFileClip): image or video
    
    Return:
        return (VideoFileClip): fitted image or video. 
    """
    # resize given image while keeping ratio
    if image.size[0] / image.size[1] > self.target_resolution[0] / self.target_resolution[1]:
      height = image.size[1] * self.target_resolution[0] / image.size[0]
      height = max(height, self.target_resolution[0])
    else:
      height = self.target_resolution[1]
    image = image.resize(height=height)
      
    # set image position: center
    image = image.set_position(("center", "center"))
    
    # set duration and position of the background
    background = image.resize(self.target_resolution)
    background = background.fl_image(lambda frame: gaussian(frame.astype(float), sigma=8))
    background = background.set_duration(image.duration)
    
    # composite with background image. 
    return CompositeVideoClip([background, image])
    
  def __add_text_to_video(self, image: VideoFileClip, text: str):
    """
    Returns subtitle-adding function for moviepy.fl_image()

    Args:
        image (VideoFileClip): video to add subtitle
        text (str): subtitle
    
    Return:
        return (VideoFileClip): video with subtitle
    """
    def pipeline(subtitle):
      def fun(frame):
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        for idx, line in enumerate(subtitle):
          x = self.target_resolution[0] / 2
          # y = self.target_resolution[1] - self.text_size * (3 + 1.5 * (len(subtitle) - 1 - idx))
          # y = self.target_resolution[1] / 2 + self.text_size * (idx * 1.5 - 0.75)
          y = self.target_resolution[1] * 0.73 + self.text_size * idx * 1.4
          draw.text((x, y), line, self.text_color, self.font, "mm", stroke_width=self.text_stroke_width, stroke_fill=self.text_stroke_color)
        return np.array(frame)
      return fun
    
    # split text to put in the screen
    subtitles = []
    subtitle = ""
    for token in text.split():
      if len(subtitle) + len(token) > self.max_text_cnt:
        # enter: make new line
        subtitles.append(subtitle)
        subtitle = token
      else:
        # add token to current line
        subtitle += f" {token}"
        subtitle = subtitle.strip()
      if token.endswith((".", "!", "?", "\"")):
        # end of the line: make new empty line
        subtitles.append(subtitle)
        subtitle = ""
    if subtitle:
      subtitles.append(subtitle)
    
    # triple subtitles
    subtitles = list(zip(subtitles[::2], subtitles[1::2] + [""]))
    
    # add subtitles for each clips
    sub_clips = []
    get_subtitle_len = lambda l: sum(len(s) + (4 if s.endswith((".", "!", "?", "\"")) else 0) for s in l)
    total_len = sum(map(get_subtitle_len, subtitles))
    start = 0
    end = 0
    for idx, subtitle in enumerate(subtitles):
      if idx == len(subtitles) - 1:
        end = image.duration
      else:
        end = min(start + image.duration * (get_subtitle_len(subtitle) / total_len), image.duration)
      sub_clip = image.subclip(start, end)
      sub_clip = sub_clip.fl_image(pipeline(subtitle))
      sub_clips.append(sub_clip)
      start = end
    
    return concatenate_videoclips(sub_clips)
  
  def __edit_image_or_video_with_audio(self, line: dict, video_name: str):
    """
    Add a video to an audio, then return a video clip.

    Args:
        line (dict): must have audio_name, image_name, and duration.
        video_name (str): name of the video. 
    
    Return:
        return (VideoClip): video clip. 
    """
    # validation
    assert "audio_name" in line
    assert "image_name" in line
    assert "content" in line
    
    # audio clip
    audio = AudioFileClip(line["audio_name"])
    audio = audio.subclip(0, audio.duration - 0.05)
    audio = concatenate_audioclips([audio, AudioClip(lambda _: 0, duration=0.05)])
    
    # get image clip
    if self.__is_image(line["image_name"]):
      # if image, set duration as audio
      image = ImageClip(line["image_name"])
      image = image.set_duration(audio.duration)
    else:
      # if video, remove audio and set duration as audio (loop or cut)
      image = VideoFileClip(line["image_name"])
      image = image.without_audio()
      if image.duration < audio.duration:
        image = image.loop(duration=audio.duration)
      else:
        image = image.set_duration(audio.duration)
    
    # fit video into the screen
    image = self.__fit_image_or_video_in_screen(image)
    
    # add subtitles
    image = self.__add_text_to_video(image, line["content"])
    
    # add audio
    video = image.set_audio(audio)
    video = video.set_fps(self.fps)
    
    return video
  
  def __add_bgm_to_video(self, video: VideoFileClip, bgm: str, bgm_vol: float):
    # bgm
    bgm = AudioFileClip(bgm)
    bgm = bgm.volumex(bgm_vol)
    if bgm.duration < video.duration:
      bgm = afx.audio_loop(bgm, duration=video.duration)
    else:
      bgm = bgm.set_duration(video.duration)
    
    # compose bgm with audio of the video
    audio = CompositeAudioClip([video.audio, bgm])
    
    return video.set_audio(audio)

  def edit_video(self, scenes: list, dirpath: str, bgm: str, bgm_vol: float):
    """
    Edit and save the final video. 

    Args:
        scenes (list): returned value by Image/Video Generator. 
                       each line must have audio_name, video_name, and duration. 
        dirpath (str): path of saved clips and video.
        bgm (str): path to the background music.
        bgm_vol (float): volume of the background music. 
    
    Return:
        return (str): returns video_name if no error occurred. 
    """
    # generate video clips for each lines
    video_clips = []
    for scene_idx, scene in enumerate(scenes):
      for line_idx, line in enumerate(scene):
        video_clips.append(self.__edit_image_or_video_with_audio(line=line, video_name=os.path.join(dirpath, f"clip-{scene_idx}-{line_idx}")))
    
    # make final video
    video = concatenate_videoclips(video_clips)
    video = self.__add_bgm_to_video(video, bgm, bgm_vol)
    video.write_videofile(os.path.join(dirpath, "video.mp4"))
    
    return os.path.join(dirpath, "video.mp4")
