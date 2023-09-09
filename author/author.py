import openai
import random
from author.prompts import instruction, few_shot_samples

class Author(object):
  def __init__(self, openai_api_key: str):
    """
    Initialize author that generates script. 
    It uses ChatGPT, so needs openai api key. 

    Args:
        openai_api_key (str): openai api key
    """
    # authentication
    openai.api_key = openai_api_key
  
  def write_script(self, info: dict, model: str="gpt-3.5-turbo", temperature: float=0.7):
    """
    Write script for given information. 

    Args:
        info (dict): dict consists of "keyword", "hanja", "mean", "story". 
        model (str): gpt model name (default: gpt-3.5-turbo)
        temperature (float): creativity of gpt model (default: 0.7)
        
    Return:
        return (str): script for given information. 
    """
    # verify info
    assert info["keyword"] is not None
    assert info["hanja"] is not None
    assert info["mean"] is not None
    assert info["story"] is not None
    
    # due to the input length constraint, get one-shot sample
    one_shot_sample = random.sample(few_shot_samples, 1)[0]
    messages = [
      {"role": "system", "content": instruction}, 
      {"role": "system", "name": "example_user", "content": one_shot_sample["prompt"]}, 
      {"role": "system", "name": "example_assistant", "content": one_shot_sample["completion"]}, 
      {"role": "user", "content": f"사자성어: {info['keyword']}\n\n한자: {info['hanja']}\n\n의미: {info['mean']}\n\n유래: {info['story']}"}
    ]
  
    # get response from chatgpt api
    response = openai.ChatCompletion.create(
      model=model,  
      messages=messages, 
      temperature=temperature
    )
    
    # print result
    print("Author Result:")
    print("Model:", response["model"])
    print("Temp:", temperature)
    print("Input Tokens:", response["usage"]["prompt_tokens"])
    print("Output Tokens:", response["usage"]["completion_tokens"])
    print("Script:")
    print(response["choices"][0]["message"]["content"])
    
    return response["choices"][0]["message"]["content"]
