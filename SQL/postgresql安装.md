####目的：熟悉各种状态下postgresql ，理解postgresql 服务运行步骤和基本原理

 

# on linux  centos 7 

 

## 一、EDB 公司发行版 Interactive Installer  postgresql-10.6-1-linux-x64.run

  

```bash
chmod +x postgresql-10.6-1-linux-x64.run
./postgresql-10.6-1-linux-x64.run
```



一路选择即可

此种方法，自动初始化数据库 ,提供了systemctl控制脚本

软件目录 /opt/PostgreSQL/10,数据目录 /opt/PostgreSQL/10/data 

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(8).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image002.jpg)

 

pg_env.sh 里常见的系统变量

 

提供了 postgresql-10.service 

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(9).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image004.jpg)

/etc/systemd/system/multi-user.target.wants/postgresql-10.service 储存的是连接

/usr/lib/systemd/system/postgresql-10.service  储存的是文件

 

提供了卸载方法

卸载不会删除data文件目录  和 postgres account 

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(10).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image006.jpg)

service 脚本也删除了，只剩下链接

 

 

## 二 、rpm 版

<https://yum.postgresql.org/>

通过yum

wget <https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm>

 

yum install [pgdg-centos10-10-2.noarch.rpm](https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm)

 

```bash
yum list |grep postgresql 
```

选择postgresql-10

但是 这个网站被墙了 

于是手动下载rpm包 

按顺序安装，有顺序要求，如果顺序错了，按相应提示调整

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(11).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image008.jpg)

 

postgresql-10.service存在

现在需要初始化数据库

```
/usr/pgsql-10/bin/postgresql10-setup initdb 
```

 

postgresql10-setip 本质上是调用 bin/initdb     bin/intidb 是可以选择pgdata目录的

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(12).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image010.jpg)

 

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(13).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image012.jpg)

 

这种方式安装的特点，自动创建了postgres 用户

特定目录，需要初始化数据库，系统已经配置好了postgresql-10.service 启动脚本；不需要手动启动 

安装完后，需要设置密码；

少了很多插件，需要手动安装，比如plpython3u。

配置也需要空白，需要细心配置

 

![说明: C:\Users\ADMINI~1\AppData\Local\Temp\2\enhtmlclip\Image(14).png](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image014.jpg)

 

 

数据库服务，就是 软件+数据库目录； 数据库的安装和运行，总的来说，就是下载软件（bin），然后初始化数据目录，最后写一个服务脚本，添加到系统服务里面去。 

 

 

## 三、linux-binaries 版本

 

postgresql-10.6-1-linux-x64-binaries.tar.gz 

`tar -zxvf postgresql-10.6.1-linux-x64-binaries.tar.gz -C /opt/postgresql10`

需要创建一个非root用户

`useradd -M postgres `  -M 作用为只创建用户,不再home目录下添加用户根目录

服务的启动需要`postgres` 对软件目录有权限

`chown -R postgres  /opt/postgresql10`

`mkdir /opt/postgresql10/data `

`su postgres `

`/bin/initdb -D /opt/postgresql10/data `

`pg_ctl -D /opt/postgresql10/data  -l /opt/postgresql/data/startup.log  start `

 



## 四、源代码版本

  

下载代码<https://www.postgresql.org/ftp/source/v10.6/> 

postgresql-10.6.tar.gz

 

`tar -zxvf postgresql-10.6.tar.gz `

`cd postgresql-10.6 `

`./configure --help`  查看编译选项

`./configure --prefix=/opt/postgresql10`  (缺什么yum install   ,可能有gcc  zlib-devel readline-devel)

`make && make install `

（扩展的安装 contrib cd contrib/pg_stat_statements/ make && make install 全部扩展 cd contrib/../ make world && make install-world ） 

 

创建用户postgres 

```bash
useradd postgres -M password postgres 
mkdir  /opt/postgresql10/data
chown -R postgres:postgres /opt/postgresql10/data
/opt/postgresql10/bin/initdb -D /opt/postgresql10/data -E UTF8
```

启动服务

`/opt/postgresql10/bin/pg_ctl -D /opt/postgresql10/data -l /opt/postgresql10/data/startup.log start `

 

改密码 

`alter user postgres with password 'since2015'; `

改配置  `postgresql.conf   pg_hba.conf`   

/opt/postgresql10/bin/pg_ctl -D /opt/postgresql10/data -l /opt/postgresql10/data/startup.log restart  

# on windows 

 

## 一、EDB postgresql

postgresql-10.5-1-windows-x64.exe

一键安装 

 

## 二、windows binaries (绿色版)

 

MSVCR120.dll   缺vc2013  安装之

Visual Studio 6 ： vc6

Visual Studio 2003 ： vc7

Visual Studio 2005 ： vc8

Visual Studio 2008 ： vc9

Visual Studio 2010 ： vc10

Visual Studio 2012 ： vc11

Visual Studio 2013 ： vc12

Visual Studio 2015 ： vc14

Visual Studio 2017 ： vc15

\---------------------

```bash
bin\initdb -D C:\pgdata -U postgres -E UTF8  --locale=chs -W 
bin\pg_ctl -D c:\pgdata  -l c:\pgdata\startup.log start 
```



注册windows服务

```bash
bin\pg_ctl  register -N postgresql10 -D c:\pgsql 
```

 

删除服务 

```bash
bin\pg_ctl.exe unregister -N postgresql10 

sc delete postgresql 10

net stop postgresql10
```

 

 

# 与 mysql的横向对比

## 一 rpm 包

 ```bash
MySQL-5.6.26-1.linux_glibc2.5.x86_64.rpm-bundle.tar 

rpm -e --no-deps mariadb-libs 

rpm -ivh mysql-server 

rmp -ivh mysql-client 

rpm -ihv mysql-devel 

改配置  /ect/my.cnf 

systemctl start mysql 

改密码
 
set password=password('since2015');
 ```



## 二  binaries 安装

```bash
yum install autoconf 

rpm -e --nodeps mariadb-libs 

tar -zxvf ...  -C /opt 

/etc/my.cnf 

basedir=/opt/mysql     

datadir=/opt/mysql/data

character-set-server=utf8

collation-server=utf8_general_ci


初始化数据库

./bin/mysqld_safe --user=root & 


改密码

./bin/mysqladmin -uroot password since2015


登陆

./bin/mysql - u root -p 

```



三、源代码安装

 

 

 

 

 

 

 