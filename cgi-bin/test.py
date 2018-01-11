#!/usr/bin/python
# -*- coding:utf-8 -*-

import cgi
form = cgi.FieldStorage()

html_body1 = """
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<body>
"""

html_body2 = """
</body>
</html>
"""

content = ''
content += "Hello %s !<br />" % form.getvalue('name', '')

print("Content-type: text/html\n")
print(html_body1 + content + html_body2)
