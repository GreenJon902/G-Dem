rulesRaw = open("src/rulesRaw.txt", "r").read()
rulesRaw = rulesRaw.rstrip("\n")
open("out/rules.html", "w").write("")
rulesHtml = open("out/rules.html", "a")

rulesHtml.write("""
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>G-Dem SMP Rules & Info</title>
    <style>
      html {
        size: 100%, 100%;
        background-color: #111;
      }

      body {
          padding: 10px;
      }

      h {
        color: #fff;
        font-size: 30px;
      }

      .dropdownButton {
        background-color: #222;
        color: #fff;
        cursor: pointer;
        padding: 18px;
        width: 100%;
        border: none;
        text-align: left;
        outline: none;
        font-size: 20px;
        border-radius: 10px;
        margin-top: 10px;
      }

      .active {
        background-color: #222;
      }

      .dropdownAnimator {
        overflow: hidden;

        -moz-transition: height .25s;
        -ms-transition: height .25s;
        -o-transition: height .25s;
        -webkit-transition: height .25s;
        transition: height .25s;
        height: 0px;
      }

      .dropdownHolder {
        padding: 18px;

        background-color: #191919;
        color: #fff;
        font-size: 1em;

        border-radius: 10px;
      }

      @font-face {
        font-family: span;
        src: url(calibril.ttf);
      }

      @font-face {
        font-family: button;
        src: url(uni_sans.otf);
      }

      span {
        display: inline-block;
        font-family: span;
      }

      button {
        font-family: button;
      }

      a {
        color: white;
      }

      .link {
        text-decoration-color: #888
      }
    </style>
  </head>
  <body>
    <h style="font-family: button;"><u><a href="index.html">G-Dem SMP</a></u> Rules & Infomation</u></h>

    <div>
""")

ruleNumber = 0
for rule in rulesRaw.split("\n\n---\n"):
    ruleNumber += 1
    rulesHtml.write("<button type=\"button\" class=\"dropdownButton\" id=\"{0}\">{1}. {2}</button><div class=\"dropdownAnimator\"><div class=\"dropdownHolder\">".format(rule.split("\n")[0].lower(), ruleNumber, rule.split("\n")[0]))

    for line in rule.split("\n")[1:]:

        leadingTabs = 0
        for char in line:
            if char == "	":
                leadingTabs += 1
            else:
                break
        line = line.lstrip("    ")

        line = line.replace("[LINK]", "<a class=\"link\" href=\"./rules.html#")
        line = line.replace("|LINK|", "\">")
        line = line.replace("[/LINK]", "</a>")

        line = line.replace("[HYPERLINK]", "<a class=\"link\" href=\"")
        line = line.replace("|HYPERLINK|", "\">")
        line = line.replace("[/HYPERLINK]", "</a>")

        rulesHtml.write("<span style=\"margin-left:{0}ch\">{1}</span><br>".format(leadingTabs * 4, line.replace("   ", "&emsp;")))
    rulesHtml.write("</div></div>")

rulesHtml.write("""
    </div>
  </body>

  <script>
  var coll = document.getElementsByClassName("dropdownButton");
  var i;

  for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.clientHeight) {
      content.style.height = 0;
    } else {
      content.style.height = content.children[0].clientHeight + "px";
    }
  });
  }

  function hashHandler(){
    this.oldHash = "";
    this.Check;

    var that = this;
    var detect = function(){
        if(that.oldHash!=window.location.hash){
            var hash = window.location.hash.substring(1); //Puts hash in variable, and removes the # character
            var elem = document.getElementById(decodeURI(hash));
            if(elem != null) {
                elem.classList.add("active");
                var content = elem.nextElementSibling;
                content.style.height = content.children[0].clientHeight + "px";
            }

            that.oldHash = window.location.hash;
        }
    };
    this.Check = setInterval(function(){ detect() }, 100);
  }

  var hashDetection = new hashHandler();
  </script>
</html>""")
rulesHtml.close()
