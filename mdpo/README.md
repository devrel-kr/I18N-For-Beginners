![header](https://capsule-render.vercel.app/api?type=wave&color=auto&height=250&section=header&text=mdpo%20&fontSize=90)



# mdpo 사용법

### mdpo 라이브러리 링크
<img src="https://mondeja.github.io/mdpo/latest/_static/mdpo.png" width= "200px" alt = "mdpo" />

<a href=":https://github.com/mondeja/mdpo">https://github.com/mondeja/mdpo </a>

### mdpo 설치
* terminal에  pip install mdpo 입력
### md to po 변환
* 디렉토리 안에 변환할 md 파일을 위치시킨다
* md2po md파일명 -q -s -p ./po파일명.po

### po to md 변환
* 디렉토리 안에 원본md파일, po파일을 위치시킨다
* po2md 원본md파일명.md -p po파일명.po -q -s 변환후md파일명.md

#### 예시
>md2po README.md -q -s -p ./readme.po

>po2md README.md -p readme.po -q -s readmekr.md


* -q : Do not print output to STDOUT. (can be replaced by --quiet )
* -s : Save new found msgids to the po file indicated as parameter --po-filepath (can be replaced by --save )
* -p : Path where new pofile will be saved (can be replaced by --po-filepath)
