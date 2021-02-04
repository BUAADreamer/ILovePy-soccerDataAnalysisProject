import webbrowser
from random import randrange
import os
from flask import Flask, render_template, send_from_directory, url_for, session
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from flask_sqlalchemy import SQLAlchemy
# import db
import flask
import pandas as pd
import pymysql
import requests
from lxml import etree
import re
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.charts import Scatter
from jinja2 import Markup

app = Flask(__name__, template_folder="./static",
            static_folder="./static",
            static_url_path="")
app.config['SECRET_KEY'] = os.urandom(24)


def register(name, password):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='Soccer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT * FROM client \
           WHERE NAME = '%s'" % name
    cursor.execute(sql)

    if cursor.rowcount > 0:
        result = cursor.fetchall()[0]
        db.close()
        if (result[1] == password):
            return 1
        else:
            return 0
    else:
        sql = "INSERT INTO client (name, password) VALUES (%s, %s)"
        val = (name, password)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        return 2


def getUser():
    if "user" not in session.keys():
        user = "Stranger"
    else:
        user = session["user"]
    return user


@app.route("/")
def index():
    return render_template('index.html', user=getUser())


@app.route("/login", methods=['GET', 'POST'])
def login():
    if flask.request.method == "GET":
        return render_template("examples/login-page.html", user="Stranger")

    elif flask.request.method == "POST":
        # print("post")
        name = flask.request.form['name']
        password = flask.request.form['password']
        # print(name,password)
        # print("hello")
        x = register(name, password)
        if (x):
            session['user'] = name
            return render_template('index.html', user=name)
        else:
            return render_template("examples/login-page.html", user="Stranger")


@app.route("/logout", methods=['GET', 'POST'])
def out():
    session['user'] = "Stranger"
    return render_template("examples/login-page.html", user="Stranger")


@app.route("/profile")
def profile():
    return render_template("examples/profile-page.html", user=getUser())


@app.route('/analyze', methods=["GET", 'POST'])
def upload():
    if flask.request.method == "GET":
        return render_template('upload.html', user=getUser())
    else:
        f = flask.request.files['file']
        path = os.path.join('./files', f.filename)
        f.save(path)
        t = f.filename.split(".")[1]
        if (t == "csv"):
            df = pd.read_csv(path).describe()
            data = {}
            for i in df.columns:
                dic = {}
                for j in df.index:
                    dic[j] = df.loc[j, i]
                data[i] = dic
        print(data)
        return render_template('analyze.html', data=data, user=getUser(), file=f.filename)


@app.route("/1")
def describe():
    return render_template("1.html", user=getUser())


@app.route("/2")
def worldmap():
    return render_template("2.html", user=getUser())


@app.route("/crawler", methods=["GET", "POST"])
def crawler():
    if flask.request.method == "GET":
        return render_template("crawler.html", user=getUser())
    else:
        country = flask.request.form["country"]
        t = flask.request.form["t"]
        print(country,t)
        urld = {"England": "https://www.dongqiudi.com/data/1", "Spain": "https://www.dongqiudi.com/data/3",
                "Italy": "https://www.dongqiudi.com/data/2", "German": "https://www.dongqiudi.com/data/4",
                "France": "https://www.dongqiudi.com/data/10", "China": "https://www.dongqiudi.com/data/231"}
        html_code = get_response(urld[country])
        content = etree.HTML(html_code)
        team = content.xpath("//span[@class='team-icon']/b/text()")  # 队名
        events = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[3]/text()")  # 场数
        win = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[4]/text()")  # 胜场
        lose = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[5]/text()")  # 败场
        draw = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[6]/text()")  # 平局
        goals = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[7]/text()")  # 进球
        fumble = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[8]/text()")  # 失球
        points = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[10]/text()")
        data = [list(x) for x in zip(goals, fumble, team)]
        s = pic(country, t).strip().strip("<body>").strip("</body>")
        print(s)
        s='''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8"/>
    <link rel="apple-touch-icon" sizes="76x76" href="./assets/img/apple-icon.png">
    <link rel="icon" type="image/png" href="./assets/img/favicon.png">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <title>
        ILovePy
    </title>
    <meta content='width=device-width, initial-scale=1.0, shrink-to-fit=no' name='viewport'/>
    <!--     Fonts and icons     -->
    <link rel="stylesheet" type="text/css"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Roboto+Slab:400,700|Material+Icons"/>
    <!--    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css">-->
    <!-- CSS Files -->
    <link href="./assets/css/material-kit.css?v=2.0.7" rel="stylesheet"/>
    <!-- CSS Just for demo purpose, don't include it in your project -->
    <link href="./assets/demo/demo.css" rel="stylesheet"/>

    <!-- 图表插入的JS World map  -->
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/world.js"></script>
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts-liquidfill.min.js"></script>
    <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts-wordcloud.min.js"></script>
    <!-- 回到顶部 和 音乐播放的 CSS-->
    <link href="./assets/css/back to top.css" type="text/css" rel="stylesheet"/>
</head>

<body class="index-page sidebar-collapse">
<nav class="navbar navbar-transparent navbar-color-on-scroll fixed-top navbar-expand-lg" color-on-scroll="100"
     id="sectionsNav">
    <div class="container">
        <div class="navbar-translate">
            <a class="navbar-brand" href="http://127.0.0.1:5000/ ">
                Index</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" aria-expanded="false"
                    aria-label="Toggle navigation">
                <span class="sr-only">Toggle navigation</span>
                <span class="navbar-toggler-icon"></span>
                <span class="navbar-toggler-icon"></span>
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ml-auto">
                <li class="dropdown nav-item">
                    <a href="#" class="dropdown-toggle nav-link" data-toggle="dropdown">
                        <i class="material-icons">apps</i> charts
                    </a>
                    <div class="dropdown-menu dropdown-with-icons">
                        <a href="./1" class="dropdown-item" target="_self">
                            <i class="material-icons">bar_chart</i> Describe
                        </a>
                        <a href="./2" class="dropdown-item" target="_self">
                            <i class="material-icons">border_inner</i> World map
                        </a>
                    </div>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="./analyze" target="_self">
                        <i class="material-icons">library_add</i> Analyze
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="./crawler" target="_self">
                        <i class="material-icons">cloud_download</i> crawler
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="./profile" target="_self">
                        <i class="material-icons">account_box</i> profile
                    </a>
                </li>
                <!--          <li class="nav-item">-->
                <!--            <a class="nav-link" rel="tooltip" title="" data-placement="bottom" href="https://twitter.com/CreativeTim" target="_blank" data-original-title="Follow us on Twitter" rel="nofollow">-->
                <!--              <i class="fa fa-twitter"></i>-->
                <!--            </a>-->
                <!--          </li>-->
                <!--          <li class="nav-item">-->
                <!--            <a class="nav-link" rel="tooltip" title="" data-placement="bottom" href="https://www.facebook.com/CreativeTim" target="_blank" data-original-title="Like us on Facebook" rel="nofollow">-->
                <!--              <i class="fa fa-facebook-square"></i>-->
                <!--            </a>-->
                <!--          </li>-->
                <!--          <li class="nav-item">-->
                <!--            <a class="nav-link" rel="tooltip" title="" data-placement="bottom" href="https://www.instagram.com/CreativeTimOfficial" target="_blank" data-original-title="Follow us on Instagram" rel="nofollow">-->
                <!--              <i class="fa fa-instagram"></i>-->
                <!--            </a>-->
                <!--          </li>-->
            </ul>
        </div>
    </div>
</nav>
<div class="page-header header-filter clear-filter" data-parallax="true"
     style="background-image: url('./assets/img/bg_for_soccer.jpg');">
    <div class="container">
        <div class="row">
            <div class="col-md-8 ml-auto mr-auto">
                <div class="brand">
                    <h1 style="color:white; font-family: Bell MT">ILovePy</h1><br>
                    <font face="Microsoft PhagesPaC" size="+2">Use dqd's data to generate some graph.</font>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="main main-raised">
    <div class="section section-basic">
        <div class="container">
            <div class="title">
                <h2 style="font-family: 'Edwardian Script ITC'; font-size: 75px;">World map</h2>
            </div>
            <!--  图表整体1 -->
            <div id="buttons" class="cd-section">
                <div class="title">
                    <h4 style="font-weight: bolder;">test</h4>
                </div>
                <div id="913d6c5c710d4efbafc979181ffb340e" class="chart-container" style="width:900px; height:500px; margin-left: 100px;">'''+s+'''</div>
                <div class="row">
                    <br>
                </div>
                <div class="row">
                    <div class="col-md-6 mx-auto" style="padding-left: 100px;">
                        <button class="btn btn-primary btn-warning">Comments</button>
                        <button class="btn btn-primary btn-round">Share</button>
                        <button class="btn btn-primary btn-round btn-info">
                            <i class="material-icons">favorite</i> Like
                        </button>

                        <button class="btn btn-primary btn-link "><font color="#00BCD4">Like</font></button>
                    </div>
                </div>
                <!-- 回到顶部 和 音乐播放  -->
                <div class="backtotop">
                    <a href="#">
                        <img id="solid" src="assets/img/rocket-sprite.png" width="48" height="78" alt=""/>
                    </a>
                    <img id="cover" src="assets/img/rocketfire.png" width="48" height="78" alt=""/>
                </div>
                <div class="music_play hi">
                    <img src="assets/img/bilibili_logo_smalltv_pink.png" onClick="play()" alt="user">
                    <audio id="music" src="assets/video/1.mp3" loop autoplay></audio>
                </div>

            </div>

            <div class="space-70"></div>

            <div class="space-50"></div>
            <!--                 textarea/checkbox/radio/toggle -->


        </div>


    </div>


</div>
<!-- Classic Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Modal title</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <i class="material-icons">clear</i>
                </button>
            </div>
            <div class="modal-body">
                <p>Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live
                    the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large
                    language ocean. A small river named Duden flows by their place and supplies it with the necessary
                    regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.
                    Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic
                    life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the
                    far World of Grammar.
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-link">Nice Button</button>
                <button type="button" class="btn btn-danger btn-link" data-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
<!--  End Modal -->
<!--   Core JS Files   -->
<script src="./assets/js/core/jquery.min.js" type="text/javascript"></script>
<script src="./assets/js/core/popper.min.js" type="text/javascript"></script>
<script src="./assets/js/core/bootstrap-material-design.min.js" type="text/javascript"></script>
<script src="./assets/js/plugins/moment.min.js"></script>
<!--	Plugin for the Datepicker, full documentation here: https://github.com/Eonasdan/bootstrap-datetimepicker -->
<script src="./assets/js/plugins/bootstrap-datetimepicker.js" type="text/javascript"></script>
<!--  Plugin for the Sliders, full documentation here: http://refreshless.com/nouislider/ -->
<script src="./assets/js/plugins/nouislider.min.js" type="text/javascript"></script>
<!--  Google Maps Plugin    -->
<!-- Control Center for Material Kit: parallax effects, scripts for the example pages etc -->
<script src="./assets/js/material-kit.js?v=2.0.7" type="text/javascript"></script>


<!--小部件的JS-->
<script src="./assets/js/back to top.js" type="text/javascript"></script>
<script src="./assets/js/music_play.js" type="text/javascript"></script>


<!--<script>-->
<!--    $(document).ready(function() {-->
<!--        //init DateTimePickers-->
<!--        materialKit.initFormExtendedDatetimepickers();-->

<!--        // Sliders Init-->
<!--        materialKit.initSliders();-->
<!--    });-->


<!--    function scrollToDownload() {-->
<!--        if ($('.section-download').length != 0) {-->
<!--            $("html, body").animate({-->
<!--                scrollTop: $('.section-download').offset().top-->
<!--            }, 1000);-->
<!--        }-->
<!--    }-->
<!--</script>-->
</body>

</html>'''
        src="./static/graph/%s_%s.html"%(country,t)
        src1="graph/%s_%s.html"%(country,t)
        with open(src, "w", encoding="utf-8") as f:
            f.write(s)
            f.close()
        return app.send_static_file(src1)


def get_response(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    response = requests.get(url, headers=header)
    return response.content.decode("utf-8")


def updateBar(win, draw, lose, team):
    c = (
        Bar()
            .add_xaxis(team)
            .add_yaxis("胜场", win, stack="stack1", color="#000079")
            .add_yaxis("平局", draw, stack="stack1", color="#7B7B7B")
            .add_yaxis("败场", lose, stack="stack1", color="#FF0000")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ), xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            ), yaxis_opts=opts.AxisOpts(
                name="场数",
                type_="value",
                interval=5,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ), )
    )
    return c


def updateScatter(goals, fumble, team):
    data = [list(x) for x in zip(goals, fumble, team)]
    y_data = [[d[1], d[2]] for d in data]
    c = (
        Scatter(init_opts=opts.InitOpts(width="", height="1000px"))
            .add_xaxis(goals)
            .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol_size=10,
            label_opts=opts.LabelOpts(formatter=JsCode(
                "function (data) {return data.value[2];}"
            )),
        )
            .set_series_opts()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                name="进球数", type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name="失球数",
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=False
            ),
        )

    )
    return c


def pic(country, t):
    urld = {"England": "https://www.dongqiudi.com/data/1", "Spain": "https://www.dongqiudi.com/data/3",
            "Italy": "https://www.dongqiudi.com/data/2", "German": "https://www.dongqiudi.com/data/4",
            "France": "https://www.dongqiudi.com/data/10", "China": "https://www.dongqiudi.com/data/231"}
    html_code = get_response(urld[country])
    content = etree.HTML(html_code)
    team = content.xpath("//span[@class='team-icon']/b/text()")  # 队名
    events = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[3]/text()")  # 场数
    win = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[4]/text()")  # 胜场
    lose = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[5]/text()")  # 败场
    draw = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[6]/text()")  # 平局
    goals = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[7]/text()")  # 进球
    fumble = content.xpath("//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[8]/text()")  # 失球
    points = goals = content.xpath(
        "//div[@class='team_point_ranking']/div/div/div[2]/p[@class='td']/span[10]/text()")  # 积分
    if t == "b":
        html = Markup(updateBar(goals, fumble, lose, team).render_embed())
    else:
        html = Markup(updateScatter(win, draw, lose).render_embed())
    content = etree.HTML(html)
    s = content.xpath("//body")[0]
    s = etree.tostring(s, pretty_print=True, encoding='utf-8').decode('utf-8')
    # print(s)
    return s


if __name__ == "__main__":
    app.run()
    # print("done")
