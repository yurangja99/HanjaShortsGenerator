# HanjaShortsGenerator

## Environment
- python 3.11.4
- selenium

## How to use
0. get your own [openai api key](https://platform.openai.com/account/api-keys) and save it in `keys.py`
0. ```pip install -r requirements.txt```
0. ```set GOOGLE_APPLICATION_CREDENTIALS=[GCP key location].json```
0. ```python main.py [keyword]```

## Pipeline
```mermaid
flowchart TD
	START(( )) --Text: 사자성어--> C([Crawler])
	C --Text: 한자,뜻,유래--> A[Author]
	A --Text: 대본--> S[Splitter]
	S --Text: 구분된 대본--> G[Image Generator]
	S --Text: 구분된 대본--> T[TTS]
	G --Image: 이미지--> V[Video Generator]
	T --Data: 음성 길이--> V
	V --Video: 움직이는 이미지--> E([Editor])
	T --Sound: 음성--> E
	E --Video: 완성 동영상--> END(( ))
```

## Crawler
네이버 한자사전에서 주어진 사자성어 (혹은 고사성어) 를 검색하여 한자, 의미, 그리고 유래를 얻는다. 

## Author
사자성어 (혹은 고사성어) 정보를 이용하여 유튜브 쇼츠 대본을 작성한다. 대본의 구성은 아래와 같이 작성한다. 

0. 호스트가 시청자들에게 사자성어에 관련된 흥미로운 질문을 던지며 동영상이 시작된다. 
0. 호스트가 사자성어의 한자를 한 글자씩 간략하게 설명하고 사자성어의 뜻을 설명해 준다. 
0. 호스트가 사자성어의 유래를 이야기 형식으로 설명하며, 중간중간 등장 인물의 대사를 섞어 준다. 
0. 호스트가 사자성어의 뜻과 유래를 통해 얻을 수 있는 교훈을 시청자들에게 설명하며 동영상이 끝난다. 

대본 작성을 위한 기술로는 [ChatGPT](https://chat.openai.com/)와 [KoAlpaca](https://github.com/Beomi/KoAlpaca)를 고려하였다. 선택을 위해 내가 고려한 사항은 아래와 같다. 

||ChatGPT|KoAlpaca|
|-|-|-|
|성능|상대적으로 좋음|상대적으로 나쁨|
|모델 크기|상대적으로 큼|상대적으로 작음|
|Few-shot|가능|가능|
|로컬 실행|불가능|가능|
|API 지원|지원|미지원|
|가격|유료|로컬 실행 시 무료|

ChatGPT를 사용한다면 파이썬 환경에서 API 호출을 통해 사용하고, KoAlpaca를 사용한다면 로컬 컴퓨터에 모델을 다운로드하여 사용하고자 하였다. 그러나 KoAlpaca를 로컬에서 실행할 정도로 로컬 컴퓨터 성능이 좋지 않고 ChatGPT의 API가 접근성이 훨씬 좋았기 때문에 일단 ChatGPT API를 활용하기로 하였다. 추후 KoAlpaca를 로컬 환경에서 실행하는 것이 가능해지면 KoAlpaca와 비교해 볼 예정이다. 

ChatGPT와 KoAlpaca 모두 내가 제시한 대본 형식을 따르지 않거나 사실과 다른 내용을 제공할 때가 있다. 따라서 여러 번 결과를 내도록 하거나 검수하는 과정이 필수적이다. 

## Splitter
[Author](#author)에서 작성된 대본을 [TTS](#tts)나 [Image Generator](#image-generator)에서 쉽게 이해할 수 있도록 형식을 변환하고, 이미지 기준으로 분리하는 역할을 한다. (한 이미지/동영상을 띄워 놓고 어디까지 말할 것인가? 를 정한다.)

`Splitter` 클래스의 `split()` 함수는 두 개의 값을 반환한다 - `speakers`, `scenes` - 그리고 두 값의 형태는 아래와 같다. 

### speakers
```json
["호스트", "우공"]
```

### scenes
```json
[
	[
		{"speaker": 0, "content": "어떻게 보면 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다고 생각해 본 적이 있으신가요? 오늘은 그런 상황을 나타내는 사자성어, '우공이산'에 대해 이야기해 볼까요?"}
	], 
	[
		{"speaker": 0, "content": "우공이산. 어리석을 우, 공평할 공, 옮길 이, 산 메 산으로 이루어진 사자성어에요. 남이 보기에는 어리석은 일처럼 보이지만 한 가지 일을 끝까지 밀고 나가면 언젠가는 목적을 달성할 수 있다는 의미를 가지고 있어요."}
	], 
	[
		{"speaker": 0, "content": "우공이산의 유래는 중국 북산에 우공이라는 90세 된 노인이 살고 있었어요. 그는 태행산과 왕옥산 사이에 있는 큰 산을 평평하게 만들어서 길을 내고 싶다고 가족들에게 말했어요. 아내는 반대하며 그의 힘으로는 불가능하다고 말했지만 우공은 결심하고 돌과 흙을 파내어 나르기 시작했어요."},
		{"speaker": 1, "content": "이렇게 해서 언젠가는 산을 옮길 수 있을 거야!"},
		{"speaker": 0, "content": "사람들은 우공을 비웃었지만 그는 자신의 결심에 힘입어 끝까지 일을 밀고 나갔어요. 결국 천제의 감동을 받아 산은 다른 곳으로 옮겨지게 되었답니다."}
	],
	[
		{"speaker": 0, "content": "'우공이산'은 우리에게 한 가지 일에 집중하고 끝까지 밀고 나가는 열정과 결단력의 중요성을 상기시켜줍니다. 어리석어 보일지라도 끝까지 노력하면 언젠가는 목적을 달성할 수 있다는 교훈이 담겨있어요."},
		{"speaker": 0, "content": "그래서 우리는 어떤 어려움이 있더라도 포기하지 않고 열심히 노력하며 끝까지 밀고 나가는 자세를 가지는 것이 중요하다는 것을 기억해야 합니다."}
	]
]
```

## TTS
![Author](#author) 부분에서 작성한 대본을 Text-to-Speech 기술을 활용하여 음성으로 변환한다. 
TTS 기술로는 ![GCP TTS](https://cloud.google.com/text-to-speech?hl=ko)를 이용하였다. 

## Image Generator

## Video Generator

## Editor
