# Building_manager

### Description:
**Building Manaager** is an android app that makes for better interaction between building manager and building inhabitants.<br>
In this project building manager can manage some building and all people they inhabit in those buildings. also manager can register notificaion, receipt , repais and so on.<br>
This app is useful and useable for building managers and building inhabitants<br>
this repository is server side app of **Building Manager**. so you can find android app [here](https://github.com/SINAsoheili/Building_manager)

### Installation:
For install this app you first need to fork project in you'r repository and clone that in you'r pc.<br>
you need python3 to run app.py module but before run app you must install *REQUIRE.txt* on you'r system.<br>
Also you need Mysql  or Mariadb to create server side databse.To import data base on you mysql or mariadb you can use followin steps :
1. create a user for databse `CREATE USER user_name;`
1. create a database `CREATE DATABASE BUILDING_MANAGER`
1. import existing databse table into you'r database `mysql -u user_name -p BUILDING_MANAGER < BUILDING_MANAGER.sql`

after creat database you must rewrite *db_config.py* as you want.<br>

