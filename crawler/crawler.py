import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawler(object):
  def __init__(self):
    # Selenium chrome driver
    self.driver = webdriver.Chrome()
    
    # URL of NAVER hanja dictionary
    self.url = "https://hanja.dict.naver.com/#/search?query="

  def crawl(self, keyword: str):
    """
    Find hanja, mean, and story about the given keyword. 

    Args:
        keyword (str): sa-ja-sung-eo
    
    Return:
        return (dict): consists of hanja, mean, and story. 
    """
    # search keyword
    self.driver.get(self.url + keyword)
    time.sleep(3)
    
    # select first page and load
    self.driver.find_element(By.CLASS_NAME, "origin").find_element(By.TAG_NAME, "a").click()
    time.sleep(3)
    
    # get hanja, mean, and story
    chinese = self.driver.find_element(By.CLASS_NAME, "u_word_dic")
    hanja = self.driver.find_element(By.CLASS_NAME, "hanja_mean")
    mean = self.driver.find_element(By.CLASS_NAME, "mean_list")
    story = self.driver.find_element(By.CLASS_NAME, "se_wrap")
    
    # print results
    print("Crawling Result:")
    print("Keyword:", keyword)
    print("Chinese:", chinese.text)
    print("Hanja:", hanja.text)
    print("Mean:", mean.text)
    print("Story:", story.text)
    
    self.driver.quit()
    
    return dict([("keyword", keyword), ("chinese", chinese.text), ("hanja", hanja.text), ("mean", mean.text), ("story", story.text)])
  