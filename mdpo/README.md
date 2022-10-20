
# WEBLATE를 활용한 Azure localization


![Weblate](https://s.weblate.org/cdn/Logo-Darktext-borders.png)


 [Weblate](https://weblate.org/ko/)를 통해 [Azure-sdk](https://github.com/Azure/azure-sdk) 에서 타깃한 마크다운 파일들을 지속적으로 현지화합니다.


## 기능 설명

* 타깃으로 할 마크다운 파일들을 settings.yaml(링크 예정)을 통해 특정합니다.

* 타깃으로 한 파일들이 [Azure-sdk](https://github.com/Azure/azure-sdk) 에서 업데이트 될 경우, 현재 레포에 있는 Github Action(링크 예정)이 업데이트된 마크다운을 가져옵니다.
* Github Action2(링크 예정)이 mdpo를 활용하여 .po(portable object) 로 변환 후 
[Weblate](https://weblate.org/ko/)에 업로드 시켜줍니다.

* Weblate에서 일정 퍼센티지 이상 번역이 됐을 경우 [devrel-kr/azure-sdk-korea](https://github.com/devrel-kr/azure-sdk-korean) 에 번역된 마크다운을 po파일과 함께
Pull request해 줍니다.

## 사용한 Library
<img src="https://mondeja.github.io/mdpo/latest/_static/mdpo.png" width= "100px" alt = "mdpo" />

[mdpo](https://github.com/mondeja/mdpo) (1.0.3 version)

#### mdpo 설치
* terminal에  pip install mdpo 입력
#### md to po 변환
* 디렉토리 안에 변환할 md 파일을 위치시킨다
* md2po md파일명 -q -s -p ./po파일명.po
#### po to md 변환
* 디렉토리 안에 원본md파일, po파일을 위치시킨다
* po2md 원본md파일명.md -p po파일명.po -q -s 변환후md파일명.md
#### 예시
>md2po README.md -q -s -p ./ko.po

>po2md README.md -p ko.po -q -s po/readme.md

[사이트](https://mondeja.github.io/mdpo/latest/) 참조.

## Weblate 기본 환경 구성 방법

....
