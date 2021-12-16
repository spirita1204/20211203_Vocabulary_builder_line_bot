# 20211203_Vocabulary_builder_line_bot

$ pip install django  
$ pip install line-bot-sdk  
$ pip install beautifulsoup4     
$ pip install requests   
$ pip install psycopg2     #PostgreSQL used
  
Line bot setup:  
1.build Provider  
2.build Messaging API channel  
3.setting LINE Bot access token  
4.develope LINE Bot applicarion 
5.install Ngrok  
6.setting LINE Webhook URL  
  
Heroku tips:  
1.install gits(version control,push to Heroku's git repository)   
  
2.$ pip install gunicorn  
install gunicorn(Responsible for the communication between the web server (Heroku cloud platform) and the web application (LINE Bot) use WSGI(Web Server Gateway Interface))  
  
3.install Heroku CLI  
Command Line Interface ->raise efficiency(https://devcenter.heroku.com)  
ssap:DanielDaniel123456!  
$ heroku login    
$ heroku create [application]   
return ->HTTPS url & git repository  
  
4.line bot  project setting   
告訴heroku啟動網站的方式  
build Procfile : tell heroku using gunicorn server to execute the wsgi in django project  
Peocfile content : web: gunicorn mylinebot.wsgi  
  
5.build requirements.txt  
tell Heroko what kits we should pre install  
$ pip freeze > requirements.txt (all packages) or use   
$ pipreqs ./ --encoding=utf8  
  
6.build Static repo(js,css,image...)      
  
7.setting ALLOWED_HOSTS  
'line-bot-vb.herokuapp.com' in ur setting.py
 
8.deploy to Heroku  
$ git init  
$ git add .  
$ git commit -m "initial"  
$ heroku git : remote -a line-bot-dict   
$ git push heroku main
  
9.LINE Bot Webhook URL reset  
well done!!  
#############  
$heroku run python 執行的檔案 runserver  於本地端糾錯指令  
$heroku ps:scale web=1  執行部屬  
$heroku logs --tail  查看錯誤  
$heroku run python manage.py migrate 同步資料庫    
see DB on website : https://heroku-data-explorer.herokuapp.com/  
  
$ pip install dj-database-url   
$ pip install dj-static  
  
待新增:     
歷史紀錄(字母)(複檢)  
中文輸入  
圖片輸入#impracticable 
語音輸入
第二版:發音  
  
2021/12/04 英漢辭典初步雛形,Crawler  
2021/12/05 簡體->繁體  
2021/12/06 輸入錯誤->錯誤提示,輸入近似->button message提示,沒本辭典解釋->網路釋義  
2021/12/07 檢索沒例句->找originalSound->找authority->都沒有output:No example!!,install PostgreSQL&setting  
2021/12/08 重複->搜索postgreSQL資料庫  
2021/12/13 搜尋->存到資料庫(加速存取),Heroku部屬失敗  
2021/12/14 Heroku deploy success   
2021/12/15 add kk音標  
