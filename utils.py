import openai
import time
import json
import os
from openai.error import RateLimitError

class ChatGPT(object):
  def __init__(self, openai_api_key, model: str="gpt-3.5-turbo", temperature: float=0.7):
    """
    Create ChatGPT instance with given model name and temperature

    Args:
        openai_api_key (_type_): openai api key
        model (str, optional): model name. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): creativity of the model. Defaults to 0.7.
    """
    openai.api_key = openai_api_key
    self.model = model
    self.temperature = temperature
    self.sequential_error_cnt = 0

  def ask(self, messages: list):
    """
    Create completion by ChatGPT. Handle RateLimitError by waiting 20s. 

    Args:
        messages (list): list of {"role": "", "content": ""}

    Returns:
        Response: answer of ChatGPT
    """
    try:
      response = openai.ChatCompletion.create(
        model=self.model,
        messages=messages,
        temperature=self.temperature
      )
      self.sequential_error_cnt = 0
      return response
    except RateLimitError:
      self.sequential_error_cnt += 1
      print(f"ChatGPT RateLimitError (occurred {self.sequential_error_cnt} times): try again in 20s.")
      time.sleep(20)
      return self.ask(messages)

def save(dirpath: str, data: dict | None, scripts: str | None, speakers: list | None, scenes: list | None, story: dict | None):
  """
  Save data, scripts, speakers, and scenes in temp.json.

  Args:
      dirpath (str)
      data (dict | None)
      scripts (str | None)
      speakers (list | None)
      scenes (list | None)
      story (list | None)
  """
  # construct object
  obj = {}
  if data is not None:
    obj["data"] = data
  if scripts is not None:
    obj["scripts"] = scripts
  if speakers is not None:
    obj["speakers"] = speakers
  if scenes is not None:
    obj["scenes"] = scenes
  if story is not None:
    obj["story"] = story
  
  # save data
  with open(os.path.join(dirpath, "temp.json"), "w", encoding="utf-8") as f:
    json.dump(obj, f, indent=2, ensure_ascii=False)

def load(dirpath: str):
  """
  Load data, scripts, speakers, and scenes from temp.json
  
  Args:
      dirpath (str)

  Returns:
      tuple(dict, str, list, list): data, scripts, speakers, scenes
  """
  # if no file, return None
  if not os.path.exists(os.path.join(dirpath, "temp.json")):
    return None, None, None, None, None

  # load object
  with open(os.path.join(dirpath, "temp.json"), "r", encoding="utf-8") as f:
    obj = json.load(f)
  
  # return values
  data = obj["data"] if "data" in obj else None
  scripts = obj["scripts"] if "scripts" in obj else None
  speakers = obj["speakers"] if "speakers" in obj else None
  scenes = obj["scenes"] if "scenes" in obj else None
  story = obj["story"] if "story" in obj else None
  return data, scripts, speakers, scenes, story
