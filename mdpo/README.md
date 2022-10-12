![header](https://capsule-render.vercel.app/api?type=wave&color=auto&height=250&section=header&text=mdpo%20&fontSize=90)

<img src="https://mondeja.github.io/mdpo/latest/_static/mdpo.png" width= "200px" alt = "mdpo" />
<p>
</p>
<h2>mdpo 사용법</h2>
<p>
</p>
<img src="https://img.shields.io/badge/mdpo 라이브러리--3178C6?style=flat&logo=로고이름&logoColor=white" />
<a href=":https://github.com/mondeja/mdpo">:https://github.com/mondeja/mdpo </a>
<p>
<p>
<ul>
<li><h3>How to install mdpo</h3></li>
<img src="https://img.shields.io/badge/설치방법--3178C6?style=flat&logo=로고이름&logoColor=white" /> 
<ol>
<h5><li> python version3 설치<img src="https://img.shields.io/badge/python-E34F26?style=flat&logo=python&logoColor=white" /></li>
<h5><li> terminal에  pip install mdpo 입력
</li>
</ol>
<p>
<p>
<li><h3>How to change md to po</h3></li>
<p>
<p>
<img src="https://img.shields.io/badge/실행방법--3178C6?style=flat&logo=로고이름&logoColor=white" /> 
<p>
<p>
<ol>
<h5><li>디렉토리 안에 변환할 md 파일을 위치시킨다
<h5><li>md2po md파일명 -q -s -p ./po파일명.po
</ol>
<p>
<p>
<li><h3>How to change po to md</h3></li>
<img src="https://img.shields.io/badge/실행방법--3178C6?style=flat&logo=로고이름&logoColor=white" /> 
<ol>
<h5><li>디렉토리 안에 원본md파일, po파일을 위치시킨다 </h5>
<h5><li>po2md 원본md파일명.md -p po파일명.po -q -s 변환후md파일명.md
</h5>
</ol>

<li><h3>커맨드 설명</h3></li>
<ul>
<h4><li>md2po README.md -q -s -p ./readme.po</li>
<h4><li>po2md README.md -p readme.po -q -s readmekr.md
</li>

<h5>
-q : Do not print output to STDOUT. (can be replaced by --quiet )
</h5>
<h5>
-s : Save new found msgids to the po file indicated as parameter --po-filepath (can be replaced by --save )
</h5>
<h5>
-p : Path where new pofile will be saved (can be replaced by --po-filepath)
</h5>
