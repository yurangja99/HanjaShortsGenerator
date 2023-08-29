class Splitter(object):
  def __init__(self):
    pass
  
  def split(self, script: str):
    """
    Split given script in four parts. 
    1. introduction part (one or more images)
    2. explanation part (one image)
    3. story part (one or more images)
    4. lesson part (one or more images)

    Args:
        script (str): script returned by Author class. 
                      It must contain "장면 1" to "장면 4", and each line should starts with "NAME: ". 
    
    Return:
        return (tuple(list, list)): (list of speakers, list of scenes)
                                    each scene is a list whose elements are dict("speaker", "content"). 
    """
    # initialize speakers: 호스트 is always contained
    speakers = ["호스트"]
    
    # initialize scenes: length-4 list
    scenes = [[], [], [], []]
    
    # read script line by line
    scene_idx = None
    for line in map(str.strip, script.strip().split("\n")):
      if not line:
        # empty line: continue
        continue
      elif line.startswith("장면 "):
        # new scene starts
        if line == "장면 1":
          scene_idx = 0
        elif line == "장면 2":
          scene_idx = 1
        elif line == "장면 3":
          scene_idx = 2
        elif line == "장면 4":
          scene_idx = 3
        else:
          raise ValueError(line)
      else:
        # scene must be started
        assert scene_idx is not None
        
        # line: add to scenes.
        speaker, content = map(str.strip, line.split(":"))
        if speaker not in speakers:
          speakers.append(speaker)
        scenes[scene_idx].append({"speaker": speakers.index(speaker), "content": content})
    
    # print results
    print("Splitting Result:")
    print("Speakers:", speakers)
    for idx, scene in enumerate(scenes):
      print("Scene", idx + 1)
      for line in scene:
        print(line)
    
    return speakers, scenes
