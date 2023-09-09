import openai
import random
from author.prompts import instruction, few_shot_samples
from utils import ChatGPT

class Author(object):
  def __init__(self, gpt_model: ChatGPT):
    """
    Initialize author that generates script. 
    It uses ChatGPT, so needs openai api key. 

    Args:
        gpt_model (ChatGPT): gpt model
    """
    # authentication
    self.gpt_model = gpt_model
  
  def write_script(self, info: dict):
    """
    Write script for given information. 

    Args:
        info (dict): dict consists of "keyword", "hanja", "mean", "story". 
        
    Return:
        return (str): script for given information. 
    """
    # verify info
    assert info["keyword"] is not None
    assert info["chinese"] is not None
    assert info["hanja"] is not None
    assert info["mean"] is not None
    assert info["story"] is not None
    
    # due to the input length constraint, get one-shot sample
    one_shot_sample = random.sample(few_shot_samples, 1)[0]
    messages = [
      {"role": "system", "content": instruction}, 
      {"role": "system", "name": "example_user", "content": one_shot_sample["prompt"]}, 
      {"role": "system", "name": "example_assistant", "content": one_shot_sample["completion"]}, 
      {"role": "user", "content": f"사자성어: {info['keyword']}\n\n한자: {info['chinese']}\n\n훈음: {info['hanja']}\n\n의미: {info['mean']}\n\n유래: {info['story']}"}
    ]
  
    # get response from chatgpt api
    response = self.gpt_model.ask(messages)
    
    # print result
    print("Author Result:")
    print("Model:", response["model"])
    print("Input Tokens:", response["usage"]["prompt_tokens"])
    print("Output Tokens:", response["usage"]["completion_tokens"])
    print("Script:")
    print(response["choices"][0]["message"]["content"])
    
    return response["choices"][0]["message"]["content"]
