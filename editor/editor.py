from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import concatenate_videoclips, CompositeVideoClip

class Editor(object):
  def __init__(self, target_resolution: tuple, background_image: str, fps: int, text_size: int, text_color: str):
    """
    Initialize Editor. 

    Args:
        target_resolution (tuple): (width, height) of the editted video. 
        background_image (str): background image used to be letter box. 
        fps (int): fps of the video. 
        text_size (int): size of the subtitle. 
        text_color (str): color of the subtitle. 
    """
    self.target_resolution = target_resolution
    self.fps = fps
    self.background_image = ImageClip(background_image).resize(target_resolution)
    self.text_size = text_size
    self.text_color = text_color
  
  def __is_image(self, image_name: str):
    """
    Determine whether given name is image or video. 

    Args:
        image_name (str): file name
    
    Return:
        return (bool): True if image, False otherwise (of course, video.)
    """
    return image_name.split(".")[-1] in ["bmp", "jpg", "jpeg", "gif", "png", "tif", "wmf", "emf"]
  
  def __fit_image_or_video_in_screen(self, image: ImageClip | VideoFileClip):
    """
    Fit given image or video into target resolution. 
    Ratio will be kept during resizing, and rest of the part would be background image. 

    Args:
        image (ImageClip | VideoFileClip): image or video
    
    Return:
        return (VideoFileClip): fitted image or video. 
    """
    # resize given image while keeping ratio
    if image.size[0] / image.size[1] > self.target_resolution[0] / self.target_resolution[1]:
      image = image.resize(width=self.target_resolution[0])
    else:
      image = image.resize(height=self.target_resolution[1])
      
    # set image position: center
    image = image.set_position(("center", "center"))
    
    # set duration and position of the background
    self.background_image = self.background_image.set_duration(image.duration)
    
    # composite with background image. 
    return CompositeVideoClip([self.background_image, image])
    
  def __edit_image_or_video_with_audio(self, line: dict, video_name: str):
    """
    Add a video to an audio, then save the video part. 

    Args:
        line (dict): must have audio_name, image_name, and duration.
        video_name (str): name of the video. 
    
    Return:
        return (str): video name. 
    """
    # validation
    assert line["audio_name"] is not None
    assert line["image_name"] is not None
    assert line["duration"] is not None
    
    # audio clip
    audio = AudioFileClip(line["audio_name"])
    
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
    # To Be Implemented
    
    # add audio
    video = image.set_audio(audio)
    video = video.set_fps(self.fps)
    
    # save editted video
    video.write_videofile(video_name + ".mp4")    
    
    return video_name + ".mp4"
  
  def edit_video(self, scenes: list, video_name: str):
    """
    Edit and save the final video. 

    Args:
        scenes (list): returned value by Image/Video Generator. 
                       each line must have audio_name, video_name, and duration. 
        video_name (str): name of the final video. 
    
    Return:
        return (str): returns video_name if no error occurred. 
    """
    # generate video clips for each lines
    video_clips = []
    for scene_idx, scene in enumerate(scenes):
      for line_idx, line in enumerate(scene):
        video_clip_name = self.__edit_image_or_video_with_audio(line=line, video_name=f"scene{scene_idx}_line{line_idx}")
        video_clips.append(VideoFileClip(video_clip_name))
    
    # make final video
    video = concatenate_videoclips(video_clips)
    video.write_videofile(video_name + ".mp4")
    
    return video_name + ".mp4"