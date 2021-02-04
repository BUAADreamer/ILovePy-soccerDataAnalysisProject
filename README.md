# ILovePy-soccerDataAnalysisProject
## Main Function

这是一个关于足球数据分析和可视化展示的网站，可以自动爬取网上的部分数据，也可以获得用户的文件文件来分析数据,也有静态的对世界杯历年数据进行分析的网页展示

## The Main Technique Path

* 后端主要采用 `flask+mysql`

* 前端采用 `material-kit` 主题作为模板进行修改和对应配置，参考官网:https://demos.creative-tim.com/material-kit/index.html

## Introduce

* 本项目在2021年的北航暑期数据科学训练营里由北航1906的fzc和2073的ysq,lzn,tld,ljy五位同学共同开发完成
* 目前本项目只是制作了部署在本地`localhost`的`demo`，实现了基本的登录退出，上传文件，爬虫获取数据可视化，展示静态世界杯数据等功能。

## local config

### 先克隆到本地并创建虚拟环境
``` shell
git clone git@BUAADreamer
cd ./ILovePy/
conda create --name <env> --file requirements.txt
  
```

### 本地配置好mysql，并在app.py里对应位置修改自己的用户名和密码

### 用pycharm打开ILovePy项目


``` shell
#打开shell
conda activate <your-name>
flask run
就可以打开localhost对应的IP看到结果

```



