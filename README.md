# Text-summarizer

## 데이터 선정이유
- 자연어처리분야 
- 요약기술을 통해 기사,문서,논문 등의 중복적인 내용을 제거하고 핵심내용을 파악할 수 있게 도와주는 서비스 제공

### 데이터 파이프라인

![image](https://user-images.githubusercontent.com/39218451/221802966-31257dac-0d75-4094-a445-25a20b8beef4.png)

### 문서요약 종류 확인
- 1. 추출적 요약(TextRank) : 원문에서 중요한 핵심문장과 단어를 뽑아 이들로 구성된 요약
>- 단점 : 이미 존재하는 문장, 단어로만 구성되어 모델의 언어표현능력 제한
- 2. 추상적 요약(seq2seq) : 원문에 없던 문장이라도 핵심문맥을 반영한 새로운 문장을 생성하여 요약
>- 단점 : seq2seq같은 지도학습 모델을 사용하여 원문과 요약된 레이블 데이터가 둘 다 필요함

## 1. 데이터 수집 
- AI hub 문서요약텍스트 데이터 사용
- 약 30만개 정도의 법률문서, 사설잡지, 신문기사 데이터로 구성

| DataSet | Size |
| --- | --- |
| Train | 271093 |
| Valid | 30122 |

![image](https://user-images.githubusercontent.com/39218451/221803813-2620b674-7958-474d-b4f6-297fc4807031.png)

## 2. 데이터 전처리

- 약 670개 정도로 이루어진 불용어사전을 가져온 후 본문데이터에서 제거
- 전처리 함수를 사용하여 url,이메일,기호 등 메타문자 제거

| DataSet | Size |
| --- | --- |
| Train | 270637  |
| Valid | 29830  |

![image](https://user-images.githubusercontent.com/39218451/221804730-b9abf20d-410e-4946-980a-66ac4857fee2.png)

![image](https://user-images.githubusercontent.com/39218451/221807592-cc5ac47c-7c02-4388-933e-36fb8c778f4d.png)
![image](https://user-images.githubusercontent.com/39218451/221807695-426fdc72-b838-40e7-8e3d-3175317f7927.png)

## 3. 모델적용
- 추출적 요약(TextRank)
>- KoNLPy를 토크나이저로 사용
>- textrank의 KeywordSummarizer를 사용하여 중요 키워드 추출

- 추상적 요약(seq2seq)
>- seq2seq모델을 사용하여 입력된 시퀀스로부터 다른 도메인의 시퀀스 출력
>- KoBART-summarizaton 사용 : https://github.com/SKT-AI/KoBART
>- 데이터 추가 후 학습

## 4. 평가지표
- ROGUE metric 사용 : 시스템요약(모델이 만든 요약)과 참조요약(사람이 만든 요약)간 겹치는 단어의 수를 가지고 평가
- ROUGE-1 : 시스템 요약본과 참조 요약본 간 겹치는 unigram의 수(n=1)
- ROUGE-2 : 시스템 요약본과 참조 요약본 간 겹치는 bigram의 수(n=2) ex) the cat, the bed..
- KoBART모델의 rogue지표

![image](https://user-images.githubusercontent.com/39218451/221809215-173d7c3f-a4fd-49ee-bb99-3ddabb17a5c9.png)

## 5. 결과
- 실제 뉴스기사를 스크랩하여 두 가지 요약기법 비교결과 추출적요약은 중복도 섞인 방면 추상적요약은 더 깔끔하게 요약한 것으로 보여짐

![image](https://user-images.githubusercontent.com/39218451/221810199-22db6bdd-cd37-4455-99a2-b10b9cd48151.png)

- 서비스 시연
>- flask를 통해 로컬웹 제작
>- heroku를 통해 웹 배포

![image](https://user-images.githubusercontent.com/39218451/211130476-bf2a3acf-3ca3-412f-975a-e6f8065cb8e8.png)
