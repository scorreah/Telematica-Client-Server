import re

url = 'http://data.pr4e.org'
page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>It Works</h1>
    <img src="./img/tree.jpg" alt="">
</body>
</html>"""

x = re.findall("\s(?:src|href)(?:=\")(.+)\"\s", page)
print(x)