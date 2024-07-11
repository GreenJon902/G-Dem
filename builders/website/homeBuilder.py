from builders.builder import Builder, SimpleBuilder

home_start = """<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>G-Dem SMP</title>
    <style>
      html {
        size: 100%, 100%;
        background-color: #111;
      }

      body {
        size: 100%, 100%;
        padding-top: 10px;
        padding-left: 10%;
        padding-right: 10%;
      }

      .header {
        color: #fff;
        font-size: 60px;
        text-align: center;
        margin: 10px;
        display: block;
      }

      @font-face {
        font-family: span;
        src: url(calibril.ttf);
      }

      @font-face {
        font-family: button;
        src: url(uni_sans.otf);
      }

      button {
        font-family: button;
      }

      a {
        color: white;
        text-decoration-color: #fff;
        display: block;
        text-align: center;
        font-size: 30px;
        padding:20px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: button;
      }
    </style>
  </head>
  <body>
    <h class="header" style="font-family: button;"><u>G-Dem SMP</u></h>
    """

home_end = """  </body>
</html>"""

home_item = "<a href=\"{0}\" style=\"background-color:{1};\">{2}</a>\n"


class HomeBuilder(SimpleBuilder):
    @classmethod
    def _build(cls, data: str) -> str:
        home_html = ""
        home_html += home_start

        # For each item
        for line in data.split("\n"):
            line = line.strip()
            if line == "":  # If item is empty
                continue

            # If not add it
            home_html += home_item.format(*line.split(" ", 2))

        # Add end and return
        home_html += home_end
        return home_html
