import json

parser_instruction = "You are an youtuber who makes youtube shorts videos. For given Korean script, give me two words in English to find stock image or video."

parser_few_shot_samples = [
  {
    "prompt": "Script: 어떻게 보면 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다고 생각해 본 적이 있으신가요?", 
    "completion": "stupid | persistence"
  },
  {
    "prompt": "Script: 우공이산은 우리에게 한 가지 일에 집중하고 끝까지 밀고 나가는 열정과 결단력의 중요성을 상기시켜줍니다.", 
    "completion": "concentration | determination"
  },
  {
    "prompt": "Script: 그래서 우리는 어떤 어려움이 있더라도 포기하지 않고 열심히 노력하며 끝까지 밀고 나가는 자세를 가지는 것이 중요하다는 것을 기억해야 합니다.", 
    "completion": "difficulty | effort"
  },
  {
    "prompt": "Script: 밤에 불을 켤 수 없다면 어떻게 공부할 수 있을까요? 웬만한 사람은 포기하겠지만, 절박했던 두 사람은 창의적인 방법으로 문제를 해결했어요.",
    "completion": "night | creativity"
  },
  {
    "prompt": "Script: 형설지공에서 우리는 어려운 환경에서도 작은 것들을 잘 활용하며 노력하면 큰 성과를 이룰 수 있다는 교훈을 얻을 수 있어요.",
    "completion": "difficulty | effort"
  },
  {
    "prompt": "Script: 어떤 사람들은 과거의 관습과 전례에만 고집하면서 현실에 적응하지 못하는 경우가 있죠. 그런 사람들을 어떻게 표현할 수 있을까요?",
    "completion": "traditionalist | stubborn"
  },
  {
    "prompt": "Script: 수주대토에서 우리는 현실에 적응하고 변화에 대응하는 융통성 있는 태도의 중요성을 배울 수 있어요.",
    "completion": "adaptability | flexibility"
  },
  {
    "prompt": "Script: 이 사자성어는 우리에게 '과거의 관습에만 고집하면 현실에서 따라갈 수 없다'는 교훈을 전달해줘요.",
    "completion": "old tradition | modern city"
  },
  {
    "prompt": "Script: 당신과 가까운 사람이 어려운 상황에 처한다면, 어떻게 하시겠습니까? 웬만하면 도와주세요. 순망치한이니깐요.",
    "completion": "friend | helping"
  },
  {
    "prompt": "Script: 여러분은 판단력이 둔하고 세상일에 어둡고 어리석은 사람을 어떻게 생각하시나요? 오늘은 이런 상황을 나타내는 사자성어, 각주구검에 대해 이야기해 볼까요?",
    "completion": "stupid | fool"
  },
  {
    "prompt": "Script: 각주구검은 우리에게 판단력과 융통성의 중요성을 상기시켜주는데, 어떤 상황에서도 현명하게 판단하고 행동하는 능력이 필요하다는 교훈을 전달합니다.",
    "completion": "wisdom | adaptive decision making"
  },
]

generator_instruction = "\n".join([
  "You are a tale book author specialized in ancient Chinese tales.",
  "Please write detailed drawing instructions for panels of a new silent tale book page, and one-sentence overall summary of given Korean script.",
  "The story is read by '호스트', and contains dialogues of other characters.",
  "Summary should include a major event of the story, and should less or equal to 50 characters.",
  "An instruction corresponds to each line of the script, so number of instructions must be equal to the number of dialogues of the script.",
  "Each instruction should shorter or equal to 77 characters.",
  "Give your response as a JSON array like this: `{ summary: string; instructions: Array<string> }`.",
  "Be brief in your summary and instructions, don't add your own comments. Be straight to the point, and never reply things like \"Sure, I can..\" etc."
])

generator_few_shot_samples = [
  {
    "prompt": "\n".join([
      "호스트: 우공이산의 유래는 중국 북산에 우공이라는 90세 된 노인이 살고 있었어요.",
      "호스트: 그는 태행산과 왕옥산 사이에 있는 큰 산을 평평하게 만들어서 길을 내고 싶다고 가족들에게 말했어요.",
      "호스트: 아내는 반대하며 그의 힘으로는 불가능하다고 말했지만 우공은 결심하고 돌과 흙을 파내어 나르기 시작했어요.",
      "우공: 이렇게 해서 언젠가는 산을 옮길 수 있을 거야!",
      "호스트: 사람들은 우공을 비웃었지만 그는 자신의 결심에 힘입어 끝까지 일을 밀고 나갔어요.",
      "호스트: 결국 천제의 감동을 받아 산은 다른 곳으로 옮겨지게 되었답니다."
    ]),
    "completion": json.dumps({
      "summary": "a 90-year-old man UGong moved a mountain despite opposition from his wife and mocking from others",
      "instructions": [
        "serene Chinese mountain village in the background, and UGong",
        "Ugong discussing his desire to flatten the mountain and create a path with his family",
        "Ugong's wife expressing doubt about him, while he starts digging and moving rocks and soil",
        "Ugong saying his determination while carrying rocks and soil",
        "people pointing and laughing at Ugong, mocking his efforts, while he carrying rocks and soil",
        "empty mountain and impressed god in the sky"
      ]
    })
  },
  {
    "prompt": "\n".join([
      "호스트: 각주구검의 유래는 춘추전국시대의 초나라에서 일어난 일입니다. 어느 젊은이가 매우 소중히 여기는 칼을 가지고 양자강을 건너려다가 칼을 강물에 떨어뜨리고 말았어요. 그런데 이 젊은이는 어리석게도 뱃전에 그 자리를 표시해 놓았답니다.",
      "젊은이: (칼을 강물에 떨어뜨린 후) 이런, 칼이 강에 떨어졌어. 어떡하지?",
      "젊은이: 떨어뜨린 곳에 칼로 표시하고 나중에 찾으면 되겠다!",
      "호스트: 젊은이는 목적지에 도착하고 표시된 곳 아래로 뛰어들어 봤지만 칼을 찾지 못했어요. ",
      "행인 1: 저런 멍청한 사람이 있다니 하하!"
    ]),
    "completion": json.dumps({
      "summary": "a young man whose stupidity prevented him from finding his lost sword that had fallen into the river",
      "instructions": [
        "serene river scene with a young man on a boat, about 25 years old, and his sword fallen into the river",
        "a young man's regretful expression on a boat of the middle of the river, looking at the river",
        "a young man marking cross shape on the boat with his small knife",
        "a boat arrived at the destination, while a young man dive into the river to find his sword, but it wasn't there",
        "one of a group of passersby pointing and laughing at the young man's foolishness"
      ]
    })
  },
  {
    "prompt": "\n".join([
      "호스트: 순망치한의 유래는 춘추시대에 일어난 진나라와 괵나라, 우나라의 이야기에서 온 것이에요. 춘추전국시대, 진나라의 헌공이 괵나라를 침공하려고 하면서 우나라의 우공에게 길을 빌려달라고 했어요. 그런데 중신인 궁지기는 이를 반대했는데요.",
      "궁지기: 괵나라와 우나라는 한몸이나 다름없는 사이오라 괵나라가 망하면 우나라도 망할 것이옵니다. 옛 속담에도 덧방나무와 수레는 서로 의지하고, '입술이 없어지면 이가 시리다'는 말이 있사온데, 이는 곧 괵나라와 우나라를 두고 한 말이라고 생각되옵니다.",
      "호스트: 그러나 우공은 이를 믿지 않고 진나라에 길을 열어줍니다. 그 결과, 괵나라는 멸망하고 진나라는 우나라를 침공하며 궁지기의 예언대로 되어갑니다."
    ]),
    "completion": json.dumps({
      "summary": "a kingdom that collapsed when a nearby kingdom collapsed due to his wrong choice",
      "instructions": [
        "king Heongong of Jin asking to king Ugong to open his castle, while king Ugong's middle-aged male servant is opposing to him",
        "Ugong's middle-aged male servant saying his opinion to king Ugong in the king's office",
        "kingdom of king Ugong collapsed by king Heongong"
      ]
    })
  },
  {
    "prompt": "\n".join([
      "호스트: 이 사자성어는 송나라 시대에 일어났던 한 이야기에서 유래되었어요. 밭을 가는 사람이 있었는데, 그루터기에 토끼가 부딪혀 죽었어요.",
      "농부: (그루터기 옆에 앉아 토끼를 기다리며) 토끼가 뛰어나오길 언제쯤 기다려야 할까?",
      "호스트: 하지만 토끼는 다시 나타나지 않았고, 밭은 황폐해지게 되었어요. 이 이야기는 한비자라는 사람이 어떤 사람들을 조롱하기 위해 사용한 이야기였답니다."
    ]),
    "completion": json.dumps({
      "summary": "foolish farmer having false hope to have another lucky day that a rabbit hits a stump",
      "instructions": [
        "a middle-aged farmer works at a farm, while rabbit dead nearby a stump",
        "a middle-aged farmer sitting beside the stump, waiting another rabbit",
        "a regretful farmer beside the dilapidated farm"
      ]
    })
  },
  {
    "prompt": "\n".join([
      "호스트: 형설지공은 진나라 시대에 차윤과 손강의 이야기에서 유래됐어요.",
      "호스트: 차윤은 가난한 가정이지만, 반딧불을 이용해 책을 읽어 나가며 열심히 공부했어요.",
      "차윤: (반딧불이 불빛을 이용해 공부하며) 가난한 집안이지만, 반딧불이 등불의 빛을 활용해 공부하면 된다고 생각해.",
      "호스트: 또 다른 이야기로 손강이라는 소년이 있었어요. 추운 겨울에 눈에 비친 달빛을 이용해 책을 읽는 모습이었어요.",
      "손강: (눈에 비친 달빛을 이용해 공부하는 모습) 눈에 비친 달빛으로 공부하면 언젠가 보람을 느낄 수 있겠지!"
    ]),
    "completion": json.dumps({
      "summary": "Cha Yun and Son Gang who overcomed poverty with firefly and snow",
      "instructions": [
        "two young boy Cha Yun and Son Gang reading a book in their dark traditional korean homes",
        "young boy Cha Yun collecting fireflies in front his traditional korean home, at night",
        "young boy Cha Yun holding a book in one hand, and a shiny pocket in another hand in his dark traditional korean home",
        "young boy Son Gang beside snow in front his traditional korean home, holding a book in one hand, at night with full moon",
        "young boy Son Gang using moon light reflected by the snow to read a book, at night"
      ]
    })
  }
]

generator_positive_prompt = [
  "ancient",
  "korean",
  "tale",
  "anime",
  "past",
  "color",
  "intricate",
  "detailed"
]

generator_negative_prompt = [
  "missing arms",
  "missing legs",
  "missing hands",
  "missing fingers",
  "extra arms",
  "extra legs",
  "extra hands",
  "extra fingers",
  "ugly",
  "poorly drawn face",
  "poorly drawn hands",
  "deformed body features",
  "disfigured",
  "mutation",
  "worst quality",
  "american",
  "french",
  "japanese",
  "chinese",
  "franco-belgian",
  "ancient egyptian",
  "grayscale",
  "photo",
  "3D render"
]
