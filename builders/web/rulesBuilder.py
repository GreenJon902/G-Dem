from builders.builder import Builder

pre_rules = """
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
"""

post_rules = """
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
</html>
"""

rule_start = ("<button type=\"button\" class=\"dropdownButton\" id=\"{0}\">{1}. {2}</button>\n"
              "<div class=\"dropdownAnimator\"><div class=\"dropdownHolder\">\n")
rule_line = "<span style=\"margin-left:{0}ch\">{1}</span><br>\n"
rule_end = "</div></div>\n"

link_start = "[LINK]"
link_start_replacement = "<a class=\"link\" href=\"./rules.html#"
link_middle = "|LINK|"
link_middle_replacement = "\">"
link_end = "[/LINK]"
link_end_replacement = "</a>"

hyperlink_start = "[HYPERLINK]"
hyperlink_start_replacement = "<a class=\"link\" href=\""
hyperlink_middle = "|HYPERLINK|"
hyperlink_middle_replacement = "\">"
hyperlink_end = "[/HYPERLINK]"
hyperlink_end_replacement = "</a>"

rule_separator = "\n\n---\n"


class RulesBuilder(Builder):
    @staticmethod
    def build(data: str) -> str:
        rules_html = ""
        rules_html += pre_rules

        # Run for each rule
        ruleNumber = 0
        for rule in data.split(rule_separator):
            ruleNumber += 1
            rules_html += rule_start.format(rule.split("\n")[0].lower(), ruleNumber, rule.split("\n")[0])

            for line in rule.split("\n")[1:]:  # Loop through each line in the current rule

                # Deal with indentation
                leadingTabs = 0
                for char in line:
                    if char == "\t":
                        leadingTabs += 1
                    else:
                        break
                line = line.lstrip(" "*4)

                # Deal with links and hyperlinks (links are inside the rules, hyperlinks go outside)
                line = line.replace(link_start, link_start_replacement)
                line = line.replace(link_middle, link_middle_replacement)
                line = line.replace(link_end, link_end_replacement)

                line = line.replace(hyperlink_start, hyperlink_start_replacement)
                line = line.replace(hyperlink_middle, hyperlink_middle_replacement)
                line = line.replace(hyperlink_end, hyperlink_end_replacement)

                # Write the actual rule
                rules_html += rule_line.format(leadingTabs * 4, line.replace("   ", "&emsp;"))
            rules_html += rule_end

        # Add ending and return
        rules_html += post_rules
        return rules_html
