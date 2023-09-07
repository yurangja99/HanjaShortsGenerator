instruction = "\n".join([
  "당신은 한자로 이루어진 사자성어의 뜻, 유래, 교훈을 시청자들에게 설명하는 유튜브 쇼츠 동영상의 대본을 작성하는 작가입니다.",
  "대본은 한글로만 작성해야 하고, 최대한 쉬운 단어로 풀어서 설명합니다.",
  "대사 부분을 읽었을 때 걸리는 시간이 50초보다 길고 60초보다 짧아야 합니다.",
  "",
  "유튜브 쇼츠 동영상의 대본은 4개의 장면으로 이루어져 있습니다.",
  "장면 1에서는 호스트가 시청자들에게 사자성어와 관련이 있으면서도 시청자의 관심을 끌 수 있는 질문을 던지며 동영상이 시작됩니다.",
  "장면 2에서는 호스트가 사자성어를 구성하는 한자를 차례대로 한 글자씩 간략하게 설명하고 사자성어의 뜻을 설명해 줍니다. ",
  "장면 3에서는 호스트가 사자성어의 유래를 이야기 형식으로 설명합니다. 등장 인물의 독백이나 대화가 포함되어야 합니다.",
  "장면 4에서는 호스트가 동영상의 내용을 한 문장으로 정리하고, 사자성어의 뜻과 유래를 통해 얻을 수 있는 교훈을 시청자들에게 알려줍니다.",
  "",
  "당신은 사자성어의 한글 표기, 사자성어를 구성하는 한자, 사자성어의 의미, 사자성어의 유래를 입력으로 받습니다.",
  "당신은 입력에 대해 어떻게 대본을 작성해야 하는지 참고할 수 있는 예시 하나를 제시받습니다."
])

few_shot_samples = [
  {
    "prompt": "\n".join([
      "사자성어: 형설지공",
      "",
      "한자: 螢 반딧불이 형 雪 눈 설 之 갈 지 功 공 공",
      "",
      "의미: 1. 「반딧불과 눈빛으로 이룬 공(功)」이라는 뜻으로, 가난을 이겨내며 반딧불과 눈빛으로 글을 읽어가며 고생 속에서 공부(工夫)하여 이룬 공(功)을 일컫는 말.",
      "",
      "유래: 진나라(晉--)의 차윤(車胤)이라는 소년(少年)이 있었다. 그는 어린 시절(時節)부터 음전한 노력가(努力家)로 공부(工夫)를 열심히 했으나 집안이 가난해 등불(燈-)을 켜는데 사용(使用)하는 기름조차 없었다. 엷은 명주 주머니를 벌레통처럼 만들어 그 속에 반디를 수십 마리 집어넣어 거기서 나오는 빛으로 책을 비추어 읽었다. 이렇게 열심히 노력(努力)한 끝에 상서랑(尙書郞)이라는 관리(官吏)로 출세(出世)했다. 또 같은 시대(時代)에 손강(孫康)이라는 소년(少年)은 어릴 때부터 열심히 공부(工夫)했으나, 역시 집안이 가난해 등불(燈-)을 켤 기름을 살 수가 없었다. 추위를 견디며 창(窓)으로 몸을 내밀고 쌓인 눈에 반사(反射)되는 달빛을 의지(依支)해 책을 읽었다. 후(後)에 어사대부(御史大夫)가 되었다."
    ]),
    "completion": "\n".join([
      "장면 1",
      "호스트: 밤에 불을 켤 수 없다면 어떻게 공부할 수 있을까요? 웬만한 사람은 포기하겠지만, 절박했던 두 사람은 창의적인 방법으로 문제를 해결했어요.",
      "장면 2",
      "호스트: 형설지공. 반딧불이 형, 눈 설, 그럴 지, 공 공으로 이루어져요. 가난한 환경에서도 반딧불과 눈빛만을 가지고 노력하여 이룬 성과를 의미해요. 즉, 가난함을 이겨내고 공부를 통해 얻은 성취를 말하는 말이에요.",
      "장면 3",
      "호스트: 형설지공은 진나라 시대에 차윤과 손강의 이야기에서 유래됐어요.",
      "호스트: 차윤은 가난한 가정이지만, 반딧불과 눈빛을 이용해 책을 읽어 나가며 열심히 공부했어요.",
      "차윤: (반딧불이 불빛을 이용해 공부하며) 가난한 집안이지만, 반딧불이 등불의 빛을 활용해 공부하면 된다고 생각해.",
      "호스트: 또 다른 이야기로 손강이라는 소년이 있었어요. 추운 겨울에 눈에 비친 달빛을 이용해 책을 읽는 모습이었어요.",
      "손강: (눈에 비친 달빛을 이용해 공부하는 모습) 눈에 비친 달빛으로 공부하면 언젠가 보람을 느낄 수 있겠지!",
      "장면 4",
      "호스트: 형설지공에서 우리는 어려운 환경에서도 작은 것들을 잘 활용하며 노력하면 큰 성과를 이룰 수 있다는 교훈을 얻을 수 있어요.",
      "호스트: 이 사자성어는 우리에게 '용기와 노력을 통해 어려움을 극복하고 성공을 이끌어낼 수 있다'는 인생 교훈을 전달해줘요.",
      "호스트: 이런 정신을 바탕으로 우리도 형설지공처럼 노력하며 성공을 이루어나갈 수 있을 거에요."
    ])
  },
  {
    "prompt": "\n".join([
      "사자성어: 수주대토",
      "",
      "한자: 守 지킬 수 株 그루 주 待 기다릴 대 兔 토끼 토",
      "",
      "의미: 1. 「그루터기를 지켜 토끼를 기다린다.」는 뜻으로, 고지식하고 융통성(融通性)이 없어 구습(舊習)과 전례(前例)만 고집(固執)함.",
      "",
      "유래: 송나라(宋--) 사람 중에 밭을 가는 사람이 있었다. 밭 가운데 나무 그루터기가 있었는데, 풀숲에서 갑자기 한 마리의 토끼가 뛰어나오다가 그루터기에 부딪쳐 목이 부러져 죽었다. 농부(農夫)가 이것을 보고 그 후부터 일도 하지 않으며 매일같이 그루터기 옆에 앉아서 토끼가 뛰어나오길 기다렸다. 그러나 토끼는 두 번 다시 나타나지 않았으며, 그 사이에 밭은 황폐해져서 쑥대밭이 되고 말았다. 그리하여 농부(農夫)는 온 나라의 웃음거리가 되었다. 한비자(韓非子)는 이 이야기로 언제까지나 낡은 습관에 묶여 세상(世上)의 변화(變化)에 대응(對應)하지 못하는 사람들을 비꼬고 있다. 한비가 살았던 시기는 전국시대(戰國時代) 말기(末期)인데 이 때는 전 시대(時代)에 비해 기술(技術)도 진보하고 생산도 높아졌으며, 사회(社會)의 성격(性格)도 변해 있었다. 그런데도 정치가(政治家) 중에는 옛날의 정치(政治)가 이상적(理想的)이라 하여 낡은 제도(制度)로 돌아갈 것만을 주장(主張)하는 사람이 많았다. 옛날에 훌륭한 것이었다고 해서 그것을 오늘날에 적응(適應)시키려는 것은 그루터기 옆에서 토끼를 기다리고 있는 것이나 다를 것이 없다고 한비는 주장(主張)했다.",
    ]),
    "completion": "\n".join([
      "장면 1",
      "호스트: 어떤 사람들은 과거의 관습과 전례에만 고집하면서 현실에 적응하지 못하는 경우가 있죠. 그런 사람들을 어떻게 표현할 수 있을까요?",
      "장면 2",
      "호스트: 수주대토. 지킬 수, 그루 주, 기다릴 대, 토끼 토로 이루어져 있어요. 그루터기를 지키며 토끼를 기다린다는 뜻으로, 과거의 관습과 전례에만 고집하면서 현실에 적응하지 못하는 사람들을 비꼬는 말이에요.",
      "장면 3",
      "호스트: 이 사자성어는 송나라 시대에 일어났던 한 이야기에서 유래되었어요. 밭을 가는 사람이 있었는데, 그루터기에 토끼가 부딪혀 죽었어요.",
      "농부: (그루터기 옆에 앉아 토끼를 기다리며) 토끼가 뛰어나오길 언제쯤 기다려야 할까?",
      "호스트: 하지만 토끼는 다시 나타나지 않았고, 밭은 황폐해지게 되었어요. 이 이야기는 한비자라는 사람이 어떤 사람들을 조롱하기 위해 사용한 이야기였답니다.",
      "장면 4",
      "호스트: 수주대토에서 우리는 현실에 적응하고 변화에 대응하는 융통성 있는 태도의 중요성을 배울 수 있어요.",
      "호스트: 이 사자성어는 우리에게 '과거의 관습에만 고집하면 현실에서 따라갈 수 없다'는 교훈을 전달해줘요.",
      "호스트: 우리는 수주대토를 통해 현실에 뒤떨어지지 않고 적응하며 성장할 수 있는 자세를 가질 필요가 있어요."
    ])
  },
  {
    "prompt": "\n".join([
      "사자성어: 순망치한",
      "",
      "한자: 脣 입술 순 亡 망할 망 齒 이 치 寒 찰 한",
      "",
      "의미: 1. 「입술을 잃으면 이가 시리다.」는 뜻으로,",
      "a. 가까운 사이의 한쪽이 망(亡)하면 다른 한쪽도 그 영향(影響)을 받아 온전(穩全)하기 어려움을 비유(比喩ㆍ譬喩)하여 이르는 말.",
      "b. 서로 도우며 떨어질 수 없는 밀접(密接)한 관계(關係). 또는 서로 도움으로써 성립(成立)되는 관계(關係)를 비유(比喩ㆍ譬喩)하여 이르는 말.",
      "",
      "유래: 춘추시대(春秋時代) 말엽, 오패의 한 사람인 진나라(晉--) 문공의 아버지 헌공(獻公)이 괵, 우, 두 나라를 공략(攻略)할 때의 일이다. 괵나라(虢--)를 치기로 결심한 헌공(獻公)은 통과국(通過國)인 우나라(虞--)의 우공(愚公)에게 길을 빌려주면 많은 재보를 주겠다고 제의했다. 우공(愚公)이 이 제의를 수락하려 하자 중신(重臣) 궁지기(宮之奇)가 극구 간했다. 「전하(殿下), 괵나라(虢--)와 우나라(虞--)는 한몸이나 다름없는 사이오라 괵나라(虢--)가 망하면 우나라(虞--)도 망할 것이옵니다. 옛 속담에도 덧방나무와 수레는 서로 의지(依支)하고, 「입술이 없어지면 이가 시리다.」란 말이 있사온데, 이는 곧 괵나라(虢--)와 우나라(虞--)를 두고 한 말이라고 생각되옵니다. 그런 가까운 사이인 괵나라(虢--)를 치려는 진나라(秦--)에 길을 빌려 준다는 것은 언어도단이옵니다.」 「경은 진나라(秦--)를 오해하고 있는 것 같소. 진나라(秦--)와 우나라(虞--)는 모두 주 황실(皇室)에서 갈라져 나온 동종의 나라가 아니오? 그러니 해를 줄 리가 있겠소?」 「괵나라(虢--) 역시 동종이옵니다. 하오나 진나라(秦--)는 동종의 정리를 잃은 지 오래이옵니다. 예컨대 지난날 진나라(秦--)는 종친인 제나라(齊--) 환공(桓公)과 초나라(楚--) 장공(莊公)의 겨레붙이까지 죽인 일도 있지 않사옵니까? 전하(殿下)께서 그런 무도(無道)한 진나라(秦--)를 믿어선 아니되옵니다.」 그러나 재보에 눈이 먼 우공(愚公)은 결국 진나라(秦--)에 길을 내주고 말았다. 그러자 궁지기(宮之奇)는 화가 미칠 것을 두려워하여 일가권속을 이끌고 우나라(虞--)를 떠났다. 그 해 12월, 괵나라(虢--)를 멸하고 돌아가던 진나라(秦--) 군사(軍士)는 궁지기(宮之奇)의 예언(豫言)대로 단숨에 우나라(虞--)를 공략(攻略)하고 우공(愚公)을 포로(捕虜)로 잡아갔다."
    ]),
    "completion": "\n".join([
      "장면 1",
      "호스트: 당신과 가까운 사람이 어려운 상황에 처한다면, 어떻게 하시겠습니까? 웬만하면 도와주세요. 순망치한이니깐요.",
      "장면 2",
      "호스트: 순망치한. 입술 순, 망할 망, 이 치, 찰 한으로 이루어져 있어요. 가까운 사이에서 한 쪽이 망하면 다른 한 쪽도 영향을 받는다는 뜻을 가지고 있어요.",
      "장면 3",
      "호스트: 순망치한의 유래는 춘추시대에 일어난 진나라와 괵나라, 우나라의 이야기에서 온 것이에요. 춘추전국시대, 진나라의 헌공이 괵나라를 침공하려고 하면서 우나라의 우공에게 길을 빌려달라고 했어요. 그런데 중신인 궁지기는 이를 반대했는데요.",
      "궁지기: 괵나라와 우나라는 한몸이나 다름없는 사이오라 괵나라가 망하면 우나라도 망할 것이옵니다. 옛 속담에도 덧방나무와 수레는 서로 의지하고, '입술이 없어지면 이가 시리다'는 말이 있사온데, 이는 곧 괵나라와 우나라를 두고 한 말이라고 생각되옵니다.",
      "호스트: 그러나 우공은 이를 믿지 않고 진나라에 길을 열어줍니다. 그 결과, 괵나라는 멸망하고 진나라는 우나라를 침공하며 궁지기의 예언대로 되어갑니다.",
      "장면 4",
      "호스트: 이렇게 괵나라와 우나라를 통해 서로 협력하고 도움을 주며 발전하는 관계의 중요성을 알려줍니다. 우리의 인생도 서로 의지하고 함께 발전해야 더 큰 성취를 이룰 수 있답니다."
    ])
  },
  {
    "prompt": "\n".join([
      "사자성어: 각주구검",
      "",
      "한자: 刻 새길 각 舟 배 주 求 구할 구 劍 칼 검",
      "",
      "의미: 1. 「칼을 강물에 떨어뜨리자 뱃전에 그 자리를 표시(表示)했다가 나중에 그 칼을 찾으려 한다.」는 뜻으로, 판단력(判斷力)이 둔하여 융통성(融通性)이 없고 세상일(世上-)에 어둡고 어리석다는 뜻.",
      "",
      "유래: 춘추전국시대(春秋戰國時代) 초나라(楚--)의 한 젊은이가 매우 소중히 여기는 칼을 가지고 양자강(揚子江)을 건너기 위하여 배를 탔다. 배를 타고 가다가 강 한복판에서 그만 실수(失手)로 쥐고 있던 칼을 강물에 떨어뜨리고 말았다. 놀란 이 사람은 얼른 주머니칼을 꺼내서 칼을 빠뜨린 부분의 뱃전에 자국을 내어 표시(表示)를 해 놓았다. 그는 「칼이 떨어진 자리에 표시(表示)를 해놓았으니 찾을 수 있겠지.」라고 생각하고 배가 언덕에 닿자 뱃전에서 표시(表示)를 해 놓은 물 속으로 뛰어 들어가 칼을 찾았으나 칼은 없었다. 이것을 보고 사람들이 그의 어리석은 행동(行動)을 비웃었다. 어리석고 융통성(融通性)이 없음을 나타내는 말이다."
    ]),
    "completion": "\n".join([
      "장면 1",
      "호스트: 여러분은 판단력이 둔하고 세상일에 어둡고 어리석은 사람을 어떻게 생각하시나요? 오늘은 이런 상황을 나타내는 사자성어, 각주구검에 대해 이야기해 볼까요?",
      "장면 2",
      "호스트: 각주구검. 새길 각, 배 주, 구할 구, 칼 검으로 이루어진 사자성어에요. 칼을 강물에 떨어뜨리고 뱃전에 표시를 해놓았다가 찾으려 한다는 뜻으로, 판단력이 둔하고 세상일에 어둡고 어리석은 사람을 비유적으로 표현한 말이에요.",
      "장면 3",
      "호스트: 각주구검의 유래는 춘추전국시대의 초나라에서 일어난 일입니다. 어느 젊은이가 매우 소중히 여기는 칼을 가지고 양자강을 건너려다가 칼을 강물에 떨어뜨리고 말았어요. 그런데 이 젊은이는 어리석게도 뱃전에 그 자리를 표시해 놓았답니다.",
      "젊은이: (칼을 강물에 떨어뜨린 후) 이런, 칼이 강에 떨어졌어. 어떡하지?",
      "젊은이: 떨어뜨린 곳에 칼로 표시하고 나중에 찾으면 되겠다!",
      "호스트: 젊은이는 목적지에 도착하고 표시된 곳 아래로 뛰어들어 봤지만 칼을 찾지 못했어요. ",
      "행인 1: 저런 멍청한 사람이 있다니 하하!",
      "장면 4",
      "호스트: 각주구검에서 우리는 판단력이 둔하고 세상일에 어둡고 어리석은 사람의 행동을 비웃는 이야기를 들을 수 있습니다. 이렇게 판단력이 부족하거나 융통성이 없는 사람은 중요한 결정을 내리기 어려울 뿐만 아니라 그의 행동이 주변에 웃음거리로 전해지기도 하겠죠.",
      "호스트: 각주구검은 우리에게 판단력과 융통성의 중요성을 상기시켜주는데, 어떤 상황에서도 현명하게 판단하고 행동하는 능력이 필요하다는 교훈을 전달합니다."
    ])
  },
  {
    "prompt": "\n".join([
      "사자성어: 우공이산",
      "",
      "한자: 愚 어리석을 우 公 공평할 공 移 옮길 이 山 메 산",
      "",
      "의미: 1. 「우공(愚公)이 산을 옮긴다.」는 말로, 남이 보기엔 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적(目的)을 달성(達成)할 수 있다는 뜻.",
      "",
      "유래: 옛날, 중국(中國)의 북산(北山)에 우공(愚公)이라는 90세 된 노인(老人)이 있었는데, 태행산(太行山)과 왕옥산(王屋山) 사이에 살고 있었다. 이 산은 사방이 700리, 높이가 만 길이나 되는 큰 산으로, 북쪽이 가로막혀 교통(交通)이 불편했다. 우공(愚公)이 어느 날 가족을 모아 놓고 말했다. 「저 험한 산을 평평하게 하여 예주(豫州)의 남쪽까지 곧장 길을 내는 동시(同時)에 한수(漢水)의 남쪽까지 갈 수 있도록 하겠다. 너희들 생각은 어떠하냐?」 모두 찬성했으나 그의 아내만이 반대(反對)하며 말했다. 「당신 힘으로는 조그만 언덕 하나 파헤치기도 어려운데, 어찌 이 큰 산을 깎아 내려는 겁니까? 또, 파낸 흙은 어찌하시렵니까?」 우공(愚公)은 흙은 발해(渤海)에다 버리겠다며 세 아들은 물론 손자(孫子)들까지 데리고 돌을 깨고 흙을 파서 삼태기와 광주리 등으로 나르기 시작(始作)했다. 황해 근처의 지수라는 사람이 그를 비웃었지만 우공(愚公)은 「내 비록 앞날이 얼마 남지 않았으나 내가 죽으면 아들이 남을 테고, 아들은 손자(孫子)를 낳고……. 이렇게 자자손손 이어 가면 언젠가는 반드시 저 산이 평평해 질 날이 오겠지.」 하고 태연(泰然)히 말했다. 한편 두 산을 지키는 사신(蛇神)이 자신(自身)들의 거처가 없어질 형편(形便)이라 천제(天帝)에게 호소했더니, 천제(天帝)는 우공(愚公)의 우직함에 감동(感動)하여 역신(力神) 과아씨(夸蛾氏)의 두 아들에게 명하여 두 산을 하나는 삭동(朔東)에, 또 하나는 옹남(雍南)에 옮겨 놓게 했다고 한다."
    ]),
    "completion": "\n".join([
      "장면 1",
      "호스트: 어떻게 보면 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다고 생각해 본 적이 있으신가요? 오늘은 그런 상황을 나타내는 사자성어, 우공이산에 대해 이야기해 볼까요?",
      "장면 2",
      "호스트: 우공이산. 어리석을 우, 공평할 공, 옮길 이, 산 메 산으로 이루어진 사자성어에요. 남이 보기에는 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다는 의미를 가지고 있어요.",
      "장면 3",
      "호스트: 우공이산의 유래는 중국 북산에 우공이라는 90세 된 노인이 살고 있었어요. 그는 태행산과 왕옥산 사이에 있는 큰 산을 평평하게 만들어서 길을 내고 싶다고 가족들에게 말했어요. 아내는 반대하며 그의 힘으로는 불가능하다고 말했지만 우공은 결심하고 돌과 흙을 파내어 나르기 시작했어요.",
      "우공: 이렇게 해서 언젠가는 산을 옮길 수 있을 거야!",
      "호스트: 사람들은 우공을 비웃었지만 그는 자신의 결심에 힘입어 끝까지 일을 밀고 나갔어요. 결국 천제의 감동을 받아 산은 다른 곳으로 옮겨지게 되었답니다.",
      "장면 4",
      "호스트: 우공이산은 우리에게 한 가지 일에 집중하고 끝까지 밀고 나가는 열정과 결단력의 중요성을 상기시켜줍니다. 어리석어 보일지라도 끝까지 노력하면 언젠가는 목적을 달성할 수 있다는 교훈이 담겨있어요.",
      "호스트: 그래서 우리는 어떤 어려움이 있더라도 포기하지 않고 열심히 노력하며 끝까지 밀고 나가는 자세를 가지는 것이 중요하다는 것을 기억해야 합니다."
    ])
  }
]
