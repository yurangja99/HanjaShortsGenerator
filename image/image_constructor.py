import numpy as np
import re
from PIL import ImageFont, ImageDraw, Image

class ImageConstructor(object):
  def __init__(
    self, 
    target_resolution: tuple, 
    background_image: str, 
    font: str, 
    text_chinese_size: int, 
    text_korean_size: int, 
    text_color: str
  ):
    """
    Initialize Image Constructor. 

    Args:
        target_resolution (tuple): target image resolution
        background_image (str): background image. recommend to use default chalkboard image. 
        font (str): font of characters
        text_chinese_size (int): size of chinese characters
        text_korean_size (int): size of korean hun-eum
        text_color (str): color of characters
    """
    self.target_resolution = target_resolution
    self.background_image = Image.open(background_image).resize(target_resolution)
    self.ext = background_image.split(".")[-1]
    self.text_color = text_color
    self.text_chinese_size = text_chinese_size
    self.text_korean_size = text_korean_size
    self.font_chinese = ImageFont.truetype(font, size=text_chinese_size)
    self.font_korean = ImageFont.truetype(font, size=text_korean_size)
  
  def __parse(self, hanja: str):
    """
    From raw text, parse chinese and korean characters. 

    Args:
        hanja (str): raw text including chinese/korean characters

    Returns:
        tuple(str, str): chinese characters, and list of korean hun-eum
    """
    # get chinese characters: exclude korean
    chinese = re.sub(" +", " ", re.sub("[가-힣 ]", "", hanja))
    
    # get korean: split by chinese characters
    korean = list(map(lambda s: s.strip(), re.split(f"[{chinese}]", hanja)[1:]))
    
    return chinese, korean
  
  def __add_text_to_image_and_save(self, chinese: str, korean: list, image_name: str):
    """
    Add chinese characters and korean hun-eum to the background image. 
    Then, saves the image to the local storage. 

    Args:
        chinese (str): chinese characters
        korean (list): korean hun-eum
        image_name (str): image name to be saved
    """
    draw = ImageDraw.Draw(self.background_image)
    for i in range(4):
      x = self.target_resolution[0] * ((i % 2) * 4 + 3) / 10
      y_chinese = self.target_resolution[1] * ((i // 2) * 10 + 6) / 30
      y_korean = y_chinese + self.text_chinese_size * 0.8
      draw.text((x, y_chinese), chinese[i], self.text_color, self.font_chinese, "mm")
      draw.text((x, y_korean), korean[i], self.text_color, self.font_korean, "mm")
    self.background_image.save(image_name + "." + self.ext, self.ext)
    
    return image_name + "." + self.ext
  
  def construct_image(self, hanja: str, image_name: str):
    """
    Parse, create, and save hanja image. 

    Args:
        hanja (str): raw text including chinese/korean characters
        image_name (str): image name to be saved
    """
    # parse to chinese characters and korean hun-eum
    chinese, korean = self.__parse(hanja)
    
    assert len(chinese) == 4
    assert len(korean) == 4
    
    print("Image Constructor hanja:", chinese)
    print("Image Constructor huneum:", korean)
    
    # print them on the background image
    name = self.__add_text_to_image_and_save(chinese, korean, image_name)
    print("Image Constructor saved image:", name)
    return name
