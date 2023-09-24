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
    
    #assert len(speakers) <= len(names)
    assert speakers is not None
    
    # initialize Speaker instances for each speaker
    self.speakers = [Speaker(names[0])] + [Speaker(names[((i + 2) % 3) + 1]) for i in range(1, len(speakers))]
  
  def read_script(self, scenes: list, dirpath: str):
    """
    Synthesize audio for given scenes, and return it with additional info: audio file name and duration. 

    Args:
        scenes (list): scenes which is returned by Splitter
        dirpath (str): path to save audio.
        
    Return:
        return (list): input itself with audio name and duration. 
    """
    assert scenes is not None
    assert len(scenes) == 4
    assert len(scenes[0]) > 0
    assert "speaker" in scenes[0][0]
    assert "content" in scenes[0][0]
    
    # read each line and get audio name and duration
    total_duration = 0.0
    for scene_idx in range(len(scenes)):
      for line_idx in range(len(scenes[scene_idx])):
        audio_name, duration = self.speakers[scenes[scene_idx][line_idx]["speaker"]].read(text=scenes[scene_idx][line_idx]["content"], audio_name=os.path.join(dirpath, f"audio-{scene_idx}-{line_idx}"))
        scenes[scene_idx][line_idx]["audio_name"] = audio_name
        scenes[scene_idx][line_idx]["duration"] = duration
        total_duration += duration
    
    # print results
    print(f"TTS Result (total {total_duration}s):")
    for idx, read_scene in enumerate(scenes):
      print("Scene", idx + 1)
      for line in read_scene:
        print(line)
    
    return scenes
