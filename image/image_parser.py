import openai
import requests
import random
from image.prompts import parser_instruction, parser_few_shot_samples

class ImageParser(object):
  def __init__(self, openai_api_key: str, pexels_api_key: str, pixabay_api_key: str):
    """
    Initialize image parser. Needs API keys for openai, pexels, and pixabay. 

    Args:
        openai_api_key (str): openai api key
        pexels_api_key (str): pexels api key
        pixabay_api_key (str): pixabay api key
    """
    # openai chatgpt
    openai.api_key = openai_api_key
    
    # pixabay
    self.pixabay_api_key = pixabay_api_key
    self.pixabay_image_endpoint = "https://pixabay.com/api/"
    self.pixabay_video_endpoint = "https://pixabay.com/api/videos/"
    
    # pexels
    self.pexels_headers = {"Authorization": pexels_api_key}
    self.pexels_image_endpoint = "https://api.pexels.com/v1/search/"
    self.pexels_video_endpoint = "https://api.pexels.com/videos/search/"
  
  def __select_keywords(self, script: str, model: str, temperature: float):
    """
    Ask chat-gpt to get two-word prompt for given script. 

    Args:
        script (str): script by the host
        model (str): chat-gpt model name
        temperature (float): chat-gpt's creativity

    Returns:
        str: two-word prompt by chat-gpt
    """
    # few-shot learning: two-shot
    two_shot_samples = random.sample(parser_few_shot_samples, 2)
    messages = [{"role": "system", "content": parser_instruction}]
    for sample in two_shot_samples:
      messages += [
        {"role": "system", "name": "example_user", "content": sample["prompt"]}, 
        {"role": "system", "name": "example_assistant", "content": sample["completion"]}
      ]
    messages += [{"role": "user", "content": f"Script: {script}"}]
    
    # get keywords
    response = openai.ChatCompletion.create(
      model=model, 
      messages=messages, 
      temperature=temperature
    )
    
    return response["choices"][0]["message"]["content"]
  
  def __parse_image_from_pixabay(self, query: str):
    """
    Parse image from pixabay. 

    Args:
        query (str): search query

    Returns:
        dict: image object
    """
    response = requests.get(self.pixabay_image_endpoint, params={"key": self.pixabay_api_key, "q": query, "per_page": 5})
    response = response.json()
    return response["hits"]
  
  def __parse_video_from_pixabay(self, query: str):
    """
    Parse video from pixabay. 

    Args:
        query (str): search query

    Returns:
        dict: video object
    """
    response = requests.get(self.pixabay_video_endpoint, params={"key": self.pixabay_api_key, "q": query, "per_page": 5})
    response = response.json()
    return response["hits"]
  
  def __parse_image_from_pexels(self, query: str):
    """
    Parse image from pexels. 

    Args:
        query (str): search query

    Returns:
        dict: image object
    """
    response = requests.get(self.pexels_image_endpoint, headers=self.pexels_headers, params={"query": query, "per_page": 5})
    response = response.json()
    return response["photos"]
  
  def __parse_video_from_pexels(self, query: str):
    """
    Parse video from pexels. 

    Args:
        query (str): search query

    Returns:
        dict: video object
    """
    response = requests.get(self.pexels_video_endpoint, headers=self.pexels_headers, params={"query": query, "per_page": 5})
    response = response.json()
    return response["videos"]
  
  def __download_image_or_video(self, image: dict, type: int, image_name: str):
    """
    Download image or video to local storage. 

    Args:
        image (dict): object of image or video
        type (int): 0(pixabay image), 1(pixabay video), 2(pexels image), 3(pexels video)
        image_name (str): name of the stored image or video
    """
    # download image or video
    if type == 0:
      # pixabay image
      url = image["largeImageURL"]
    elif type == 1:
      # pixabay video
      url = max(image["videos"].values(), key=lambda x: x["height"])["url"]
    elif type == 2:
      # pexels image
      url = image["src"]["large2x"]
    else:
      # pexels video
      url = max(image["video_files"], key=lambda x: x["height"])["link"]
    
    # find extension
    if "?" in url:
      ext = url.split("?")[-2].split(".")[-1]
    else:
      ext = url.split(".")[-1]
    
    # download image from the url
    response = requests.get(url, stream=True)
    with open(image_name + "." + ext, "wb") as f:
      f.write(response.content)
    
  def parse_image(self, script: str, image_name: str, model: str="gpt-3.5-turbo", temperature: float=0.7):
    """
    Get image from pixabay or pexels. 

    Args:
        script (str): script by the host
        image_name (str): name of the image or video
        model (str, optional): chat-gpt model name. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): chat-gpt creativity. Defaults to 0.7.
    """
    # get two words represent the given script
    query = self.__select_keywords(script, model, temperature)
    
    # parse images and videos from apis
    candidates = [
      self.__parse_image_from_pixabay(query), 
      self.__parse_video_from_pixabay(query), 
      self.__parse_image_from_pexels(query), 
      self.__parse_video_from_pexels(query)
    ]
        
    # choose one randomly
    type = random.choices(range(len(candidates)), map(len, candidates))[0]
    image = random.sample(candidates[type])
    self.__download_image_or_video(image, type, image_name)
