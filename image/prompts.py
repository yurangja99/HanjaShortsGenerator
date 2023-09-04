parser_instruction = "You are an youtuber who makes youtube shorts videos. For given Korean script, give me two words in English to find stock image or video."

parser_few_shot_samples = [
  {"prompt": "Script: 어떻게 보면 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다고 생각해 본 적이 있으신가요?", "completion": "stupid | persistence"},
  {"prompt": "Script: 우공이산은 우리에게 한 가지 일에 집중하고 끝까지 밀고 나가는 열정과 결단력의 중요성을 상기시켜줍니다.", "completion": "concentration | determination"},
  {"prompt": "Script: 그래서 우리는 어떤 어려움이 있더라도 포기하지 않고 열심히 노력하며 끝까지 밀고 나가는 자세를 가지는 것이 중요하다는 것을 기억해야 합니다.", "completion": "difficulty | effort"}
]

generator_instruction = "You are an image designer who makes story telling videos. For given Korean script, images will be generated for each line. Depict each image in one English phrase. Focus on people and don't include names."

generator_few_shot_samples = [
  {"prompt": "Speaker:\nScript:", "completion": ""},
  {"prompt": "Speaker:\nScript:", "completion": ""},
  {"prompt": "Speaker:\nScript:", "completion": ""}
]
