import os
from tts.speaker import Speaker

class TTS(object):
  def __init__(self, speakers: list):
    """
    Initialize TTS with given speakers.
    
    Args:
        speakers (list): list of speakers. 
    """
    # set host as female, and most of the speakers as male. (heuristic, so can be changed)
    names = ["B", "C", "D", "A"]
    
    assert len(speakers) <= len(names)
    
    # initialize Speaker instances for each speaker
    self.speakers = [Speaker(names[i]) for i in range(len(speakers))]
  
  def read_script(self, scenes: list, dirpath: str):
    """
    Synthesize audio for given scenes, and return it with additional info: audio file name and duration. 

    Args:
        scenes (list): scenes which is returned by Splitter
        dirpath (str): path to save audio.
        
    Return:
        return (list): input itself with audio name and duration. 
    """
    # read each line and get audio name and duration
    read_scenes = []
    for scene_idx, scene in enumerate(scenes):
      read_scene = []
      for line_idx, line in enumerate(scene):
        audio_name, duration = self.speakers[line["speaker"]].read(text=line["content"], audio_name=os.path.join(dirpath, f"audio-{scene_idx}-{line_idx}"))
        read_scene.append({
          "speaker": line["speaker"], 
          "content": line["content"], 
          "audio_name": audio_name, 
          "duration": duration
        })
      read_scenes.append(read_scene)
    
    # print results
    print("TTS Result:")
    for idx, read_scene in enumerate(read_scenes):
      print("Scene", idx + 1)
      for line in read_scene:
        print(line)
    
    return read_scenes
