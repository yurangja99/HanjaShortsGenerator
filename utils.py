import openai
import time
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
    print("ChatGPT initialized with:")
    print("Model:", self.model)
    print("Temp:", self.temperature)

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
