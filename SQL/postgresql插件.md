

 

# 插件的安装

所有的插件都是通过源代码编译的 

 

安装方法

在window上需要自己用msvc去编译，在linux用 gcc 

 

## 1 在window上用别人编译好的binary 版 

 

下载binary版 ，对照postgresql 目录，复制相应文件到对应文件中去

![img](file:///C:\Users\jacky\AppData\Local\Temp\msohtmlclip1\01\clip_image002.jpg)

 

以plv8为例，对照 PG_HOME 。

 

## 2 linux 上 pg_xs  make 

 

下载源代码 用 c/c++编译器编译

USE_PGXS=1 make

USE_PGXS=1 make install

## 3  pgxn 工具

pgxn是一款类似 pip一样的包管理工具，原理就是下载源代码，然后编译；

 

确定是 PGXN 的reposity不是那么全；所以综合来说，还是  手动make好

 

 

# 有哪些不能错过的插件

 

## 自带插件

查看官方文档，里面的包

 ![1548398868061](C:\Users\jacky\AppData\Local\Temp\1548398868061.png)



`file_fdw`

 `pg_trgm 相似度`

`fuzzystrmatch 字符串相似度`



## language包 

 

plpython2u  

 

plpython3u

 

plv8 

 

pl/tcl   pl/r 

特别的  plpython 

 

自带的情况下，postgresql9.6与 python3.3 对应 postgresql10 与python3.4对应 postgresql11与python3.6对应  

window上如何 安装 plpython3u  

centos7 上如何安装plpython3u 

centos7上需要对python3重新编译，增加动态链接支持 

 

## fdw

 

外部表，可以把数据库、文件、接口等数据源的数据，当作自己的表

 

### odbc_fdw配置 mysql

 

实验平台window+postgresql10 

1 在postgresql 上安装 odbc_fdw 

 

2 在 window上安装 myql odbc driver  ,配置数据源

 

3 postgresql 中创建外部表

 

/* 1 创建server

drop server if exists mysql_192_168_3_172;

create server mysql_192_168_3_172 foreign data wrapper odbc_fdw

options(dsn'mysql1',encoding'gbk');

/

 

/*2 创建 用户映射

create user mapping for postgres server  mysql_192_168_3_172

options(odbc_UID'root',odbc_PWD'since2015');

*/

 

 

定义要导入的表

import foreign schema mysql 

from  server mysql 

into fdw 

options(

odbc_DATABASE 'mysql',

table 'mysql',

 

sql_query 'select * from mysql.user'

);

odbc_fdw配置 sqlserver 

 

### file_fdw  

```plsql
create server file_server foreign data wrapper ;


drop foreign table if exists file;

create foreign table file (

jgmc text,

xzqh text,

lyd text 

)

server file_server options(format'csv',filename'C:\Users\Administrator\Desktop\pdoc\example.csv',header'true');;



tds_fdw mssql 专属fdw 

mongo_fdw 

hive_fdw 

redis_fdw

hdfs_fdw

hive_fdw 

```





  

fdw 可以用来做ETL ，可以用来做分析平台的读写，可以用来做中间件（负载均衡、sql分发）

ETL 想到技术体系问题，ETL 可以用kettle  用python  用web api 来做，也可以用postgresql 做

 

## madlib  

 

apache顶级开源  机器学习模块

`postgreql  greenplum  hawq  `



安装

```bash
预装plpythonu(python2)

yum install   madlibxxx.rpm

su postgres

/usr/local/madlib/bin/madpack -s madlib –p postgres install

```



  

使用 例子  线性回归  

```sql
DROP TABLE IF EXISTS regr_example;

CREATE TABLE regr_example (

id int,

y int,

x1 int,

x2 int

);

INSERT INTO regr_example VALUES

(1, 5, 2, 3),

(2, 10, 7, 2),

(3, 6, 4, 1),

(4, 8, 3, 4);

 

x1,x2   ---> y  

```



**训练 **

```plsql
SELECT madlib.linregr_train (

'regr_example', -- source table

'regr_example_model', -- output model table

'y', -- dependent variable

'ARRAY[1, x1, x2]' -- independent variables

);
 
The intercept is computed by setting one of the independent variables to a constant 1, as shown in the preceding example.

array[1,x1,x2] 中的1  指的是 因变量维度为1 

```



 

**预测**

 ```sql
SELECT regr_example.*,

madlib.linregr_predict ( ARRAY[1, x1, x2], m.coef ) as predict,

y - madlib.linregr_predict ( ARRAY[1, x1, x2], m.coef ) as residual

FROM regr_example, regr_example_model m;

 ```

 

 

类比 python中的 sklearn  fit    predict 

 

 

 

## pg_jieba   

 

 

分词模块

 

 

## http  

 

爬虫模块

 

 

gist 

 

 

rum  

 

​    

 

## 自定义插件

 

三个条件

 

写一个c语言库，丢到pg/lib里面去

 

 

写一个 .sql 文件，提供函数接口 

 

写一个.control，定义版本和依赖关系

 

 

 

what i count create ,i cant not understand   Feiman

 

 

 

 

 

 

 

 