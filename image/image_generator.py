import torch
import openai
import random
import json
from torch import autocast
from diffusers import StableDiffusionPipeline
from image.prompts import generator_instruction, generator_few_shot_samples, generator_positive_prompt, generator_negative_prompt

class ImageGenerator(object):
  def __init__(self, openai_api_key: str, sd_model: str="CompVis/stable-diffusion-v1-4"):
    """
    Initialize image generator with Stable Diffusion model.

    Args:
        openai_api_key (str): open api key. 
        sd_model (str, optional): name of Stable Diffusion model. Defaults to "CompVis/stable-diffusion-v1-4".
    """
    openai.api_key = openai_api_key
    if torch.cuda.is_available():
      print("Image Generator in CUDA!")
      self.device = "cuda"
    else:
      print("Image Generator in CPU!")
      self.device = "cpu"
    self.pipeline = StableDiffusionPipeline.from_pretrained(sd_model, torch_dtype=torch.float16).to(self.device)
  
  def __depict_images(self, scripts: list, model: str, temperature: float):
    """
    With given list of dialogues, get over-all summary and instructions for each dialogue from chat-gpt. 

    Args:
        scripts (list): list of {"speaker": "content"}
        model (str): chat-gpt model
        temperature (float): creativity of chat-gpt model

    Returns:
        dict: {"summary": "", "instructions": [""]}
    """
    # few-shot learning: three-shot
    three_shot_samples = random.sample(generator_few_shot_samples, 3)
    messages = [{"role": "system", "content": generator_instruction}]
    for sample in three_shot_samples:
      messages += [
        {"role": "system", "name": "example_user", "content": sample["prompt"]},
        {"role": "system", "name": "example_assistant", "content": sample["completion"]}
      ]
    messages += [{"role": "user", "content": "\n".join(scripts)}]
    
    # get explanation: JSON form
    response = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=temperature
    )
    
    # verify result
    result = json.loads(response["choices"][0]["message"]["content"])
    
    assert "summary" in result
    assert "instructions" in result
    assert isinstance(result["summary"], str)
    assert isinstance(result["instructions"], list)
    #assert len(result["instructions"]) == len(scripts)
    
    return result
  
  def __generate_images(self, story: dict, image_name: str, seed: int):
    """
    Generate images from over-all summary and instructions. 

    Args:
        story (dict): story returned by __depict_images()
        image_name (str): image name to be saved
        seed (int): random seed for Stable Diffusion model

    Returns:
        list: list of saved image names
    """
    # verify story
    assert "summary" in story
    assert "instructions" in story
    assert isinstance(story["summary"], str)
    assert isinstance(story["instructions"], list)
    
    # generate images using summary and instructions of the story
    with autocast(self.device):
      images = [
        self.pipeline(
          #prompt=", ".join(generator_positive_prompt + ["Tale about " +  story["summary"], instruction]),
          prompt=", ".join(generator_positive_prompt + [instruction]),
          negative_prompt=", ".join(generator_negative_prompt),
          generator=torch.Generator(self.device).manual_seed(seed)
        ).images[0]
        for instruction in story["instructions"]
      ]
    
    # save images
    image_names = []
    for idx, image in enumerate(images):
      name = f"{image_name}-{idx}.png"
      image.save(name)
      image_names.append(name)
    
    return image_names
  
  def generate_image(
    self, 
    scripts: list, 
    image_name: str,
    gpt_model: str="gpt-3.5-turbo", 
    temperature: float=0.7, 
    seed: int=42
  ):
    # depict images using chat-gpt
    story = self.__depict_images(scripts, gpt_model, temperature)
    print("Image Generator Story:")
    print(story)
    
    # generate and save images using stable diffusion
    print("Image Generating with seed ", seed)
    image_names = self.__generate_images(story, image_name, seed)
    print("Image Generated and saved:", image_names)
    
    return image_names
