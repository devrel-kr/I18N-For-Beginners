# I18N-For-Beginners #


Internationalization for Microsoft Beginner series([Web-Dev-For-Beginners](https://github.com/devrel-kr/Web-Dev-For-Beginners) & [ML-For-Beginners](https://github.com/devrel-kr/ML-For-Beginners)) and other documents.

* **github pages** : [devrel-kr.github.io/i18n-for-beginners/](https://devrel-kr.github.io/I18N-For-Beginners/)
* **Target Branch**

    * **Original** : [microsoft/Web-Dev-For-Beginners](https://github.com/microsoft/Web-Dev-For-Beginners)

    * **Korean** : [devrel-kr/Web-Dev-For-Beginners](https://github.com/devrel-kr/Web-Dev-For-Beginners)

    


## Flow Chart ##

![Flow chart](./asserts/architecture_image.png)

```mermaid
%%{init: {
  "theme": "neutral",
  "curve": "step"
}}%%

flowchart LR
    A(start) --> B(Find changed docs)
    B -- Unchanged --> B
    B -- Update --> C(Select docs)
    C -- Delete --> B
    C --> |Calc diff| D(Show diff)
    D --> |Translated| E(Show translated docs)  
    E --> |Not Done| B
    E --> |Done| F(((stop)))
```
   

## API ##
* **[Azure Translator API](https://www.microsoft.com/ko-kr/translator/business/translator-api/)** : It translates the added changes in advance



## GitHub Secrets ##

Following GitHub Secrets are required for CI/CD :

* `USER_EMAIL`: Setting your commit Email address 

* `USER_NAME`: Setting your commit User Name 

* `TRANSLATEAPI`: Key to API used for Draft translation




## Development Tools ##

#### Prerequisites for Local Development ####

* [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=dotnet-58531-juyoo)
* [Github Action](https://pages.github.com/)
* [Jekyll](https://jekyllrb-ko.github.io/)
* [Github Pages](https://docs.github.com/en/actions)


## How to Contribute ##


You can click the **Fork** button in the upper-right area of the screen to create a copy of this repository in your GitHub account. This copy is called a *fork*. 

Make any changes you want in your fork, and when you are ready to send those changes to us, go to your fork and create a new pull request to let us know about it.


---

## LICENSE ##

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](https://github.com/devrel-kr/I18N-For-Beginners/blob/main/LICENSE) license.
