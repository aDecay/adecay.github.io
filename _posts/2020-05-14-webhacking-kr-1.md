---
layout: post
title: "[webhacking.kr] old-1번 문제"
subtitle: "쿠키에 대한 이해"
date: 2020-05-14 06:10:00 -0400
background: '/img/posts/webhacking-kr-old-1/background.png'
---
![web-01.png](/img/posts/webhacking-kr-old-1/web-01.png)  
1번 문제로 들어가면 위와 같은 창이 뜹니다.  
하이퍼링크가 적용된 view-source를 클릭하면 다음과 같이 php로 된 소스코드를 볼 수 있습니다.  
![view-source-1.png](/img/posts/webhacking-kr-old-1/view-source-1.png)  
이제 이 코드를 살펴보도록 하겠습니다.  
'''PHP
<?php
  include "../../config.php";
  if($_GET['view-source'] == 1){ view_source(); }
  if(!$_COOKIE['user_lv']){
    SetCookie("user_lv","1",time()+86400*30,"/challenge/web-01/");
    echo("<meta http-equiv=refresh content=0>");
  }
?>
'''
앞부분은 파일을 include 하는 내용과, 소스코드를 보여주기 위한 코드이기 때문에 문제를 푸는 데 필요한 내용이 아닙니다.  
여기서 중요한 부분은 두 번째 if문 입니다.  
user_lv이라는 이름의 쿠키가 없으면 user_lv이라는 쿠키를 만들고 값은 1로 설정합니다. 
쿠키를 만든 후 바뀐 내용을 적용하기 위해 페이지를 새로고침합니다.  
SetCookie 함수는 SetCookie(쿠키명, 쿠키값, 만료시간, 사용경로)의 방식으로 사용됩니다.  
![cookie-initial.png](/img/posts/webhacking-kr-old-1/cookie-initial.png)  
위 소스코드에서 본 것과 같이, 실제로 쿠키가 생성되어 있음을 확인할 수 있었습니다.  
쿠키 관련 작업은 크롬의 EditThisCookie 확장 프로그램을 사용하였습니다.  
'''PHP
<?php
  if(!is_numeric($_COOKIE['user_lv'])) $_COOKIE['user_lv']=1;
  if($_COOKIE['user_lv']>=6) $_COOKIE['user_lv']=1;
  if($_COOKIE['user_lv']>5) solve(1);
  echo "<br>level : {$_COOKIE['user_lv']}";
?>
'''
다음으로 봐야 할 부분은 이 부분입니다.  
user_lv 쿠키의 값이 숫자가 아니면 값을 1로 바꾸고, 6 이상의 값일 때에도 마찬가지로 값을 1로 바꿉니다.  
이후, user_lv 쿠키의 값이 5보다 크면 문제 풀이에 성공합니다.  
  
위 내용을 통해 user_lv 쿠키의 값을 5와 6 사이의 임의의 숫자로 설정하면 문제를 풀 수 있다는 것을 알 수 있습니다.  
저는 다음과 같이 user_lv 쿠키의 값을 5.5로 설정했습니다.  
![cookie-changed.png](/img/posts/webhacking-kr-old-1/cookie-changed.png)  
마지막으로 바뀐 쿠키를 적용하기 위해 페이지를 새로고침 하면 문제 풀이에 성공할 수 있습니다.  