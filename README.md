# HanjaShortsGenerator

## Environment
- python 3.11.4
- selenium

## How to use
0. ```pip install -r requirements.txt```
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

## Splitter

## TTS

## Image Generator

## Video Generator

## Editor
