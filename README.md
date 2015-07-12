# ForumSiteByFlask

这个网站

#简介：
>这个是我看了神书《flask web开发》而做的，里面有不少书上原文的影子，但自己也做了些改进，数据库用的是mysql。功能包括登录注册，登出，发文，评论，每个用户还能自己填写用户资料，用户也能关注别人


#使用：

>mysql操作：

>开发使用：

    create database devmyflasky;
    
>测试使用 ：   
    
    create database testmyflasky;
    
>生产使用： 

***
    
>还要在config.py那里把你的mysql用户名和密码输入（那个是我开发版本的mysql用户名和密码，懒得改了= =） ，这样sqlalchemy才能连上数据库   
    
    
    create database myflasky;

    python manage.py shell
  
    db.create_all()

>建立数据
  
    Role.insert_roles()
  
>建立用户role的角色的初始化数据库
  
    python manage.py runserver
