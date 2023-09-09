import json
from image.image_parser import ImageParser
from image.image_constructor import ImageConstructor
from image.image_generator import ImageGenerator

class Imager(object):
  def __init__(
    self,
    openai_api_key: str,
    pexels_api_key: str | None,
    pixabay_api_key: str | None,
    target_resolution: tuple,
    chalkboard: str,
    font: str,
    text_chinese_size: int,
    text_korean_size: int,
    text_chinese_color: str,
    sd_model: str
  ):
    """
    Class for parse, construct, or generate images or videos for shorts video. 

    Args:
        openai_api_key (str): openai api key
        pexels_api_key (str | None): pexels api key
        pixabay_api_key (str | None): pixabay api key
        target_resolution (tuple): target resolution as (width, height)
        chalkboard (str): background image for constructor
        font (str): font of hanja and korean in constructor
        text_chinese_size (int): size of chinese char in constructor
        text_korean_size (int): size of korean char in constructor
        text_chinese_color (str): color of chinese char in constructor
        sd_model (str): Stable Diffusion model for generator
    """
    # image parser
    self.image_parser = ImageParser(
      openai_api_key=openai_api_key,
      pexels_api_key=pexels_api_key,
      pixabay_api_key=pixabay_api_key
    )
    
    # image constructor
    self.image_constructor = ImageConstructor(
      target_resolution=target_resolution,
      background_image=chalkboard,
      font=font,
      text_chinese_size=text_chinese_size,
      text_korean_size=text_korean_size,
      text_color=text_chinese_color
    )
    
    # image generator
    self.image_generator = ImageGenerator(
      openai_api_key=openai_api_key,
      sd_model=sd_model
    )
  
  def image(self, data: dict, speakers: list, scenes: list, model: str, temperature: float, seed: int):
    """
    Parse, Construct, and Generate images for given script. 
    - parse images for scene 1 and 4. 
    - construct an image for scene 2. 
    - generate images for scene 3. 

    Args:
        data (dict): data returned by crawler. 
        speakers (list): speakers returned by splitter. 
        scenes (list): scenes returned by splitter, or tts. 
        model (str): chat-gpt model
        temperature (float): creativity of chat-gpt model
        seed (int): random seed for generator

    Returns:
        list: scenes itself, with name of image files for each line. 
    """
    # verify data
    assert "hanja" in data
    assert "keyword" in data
    
    # scene 1, 4: parse image
    for idx, line in enumerate(scenes[0]):
      scenes[0][idx]["image_name"] = self.image_parser.parse_image(
        script=line["content"],
        image_name=f"{data['keyword']}-intro-{idx}",
        model=model,
        temperature=temperature
      )
    for idx, line in enumerate(scenes[3]):
      scenes[3][idx]["image_name"] = self.image_parser.parse_image(
        script=line["content"],
        image_name=f"{data['keyword']}-outro-{idx}",
        model=model,
        temperature=temperature
      )
    
    # scene 2: construct image
    constructed_image_name = self.image_constructor.construct_image(
      hanja=data["hanja"],
      image_name=f"{data['keyword']}-hanja"
    )
    for idx, line in enumerate(scenes[1]):
      scenes[1][idx]["image_name"] = constructed_image_name
    
    # scene 3: generate image
    generated_image_names = self.image_generator.generate_image(
      scripts=[speakers[line["speaker"]] + ": " + line["content"] for line in scenes[2]],
      image_name=f"{data['keyword']}-story",
      gpt_model=model,
      temperature=temperature,
      seed=seed
    )
    #assert len(generated_image_names) == len(scenes[3])
    for idx, line in enumerate(scenes[2]):
      scenes[2][idx]["image_name"] = generated_image_names[round((len(generated_image_names) - 1) / (len(scenes[2]) - 1) * idx)]
      
    print("Imager Result:")
    print(json.dumps(scenes, indent=2, ensure_ascii=False))
    return scenes
