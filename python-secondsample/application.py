from wsgiref.simple_server import make_server

response = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>GroupMakr</title>
  <style>

    body {
      color: #ffffff;
      background-color: #ccffcc;
      font-family: Impact, Charcoal, sans-serif;
      font-size:14px;
      -moz-transition-property: text-shadow;
      -moz-transition-duration: 4s;
      -webkit-transition-property: text-shadow;
      -webkit-transition-duration: 4s;
      text-shadow: none;
    }
    body.blurry {
      -moz-transition-property: text-shadow;
      -moz-transition-duration: 4s;
      -webkit-transition-property: text-shadow;
      -webkit-transition-duration: 4s;
      text-shadow: #fff 0px 0px 25px;
      }
    div {
      width: 100%-25px;
      padding: 25px;
      border: 25px solid navy;
      margin: 25px;
    }
    a {
      color: #00000c;
    }

    .textColumn {
      position: absolute;
      top: 0px;
      right: 0px;
      bottom: 0px;
      left: 0px;

      text-align: center;
      padding-top: 11em;
      background-color: #0188cc;
      background-image: -moz-radial-gradient(left top, circle, #6ac9f9 0%, #0188cc 60%);
      background-image: -webkit-gradient(radial, 0 0, 1, 0 0, 500, from(#6ac9f9), to(#0188cc));
    }

    .button {
      border-top: 1px solid #96d1f8;
      background: #65a9d7;
      background: -webkit-gradient(linear, left top, left bottom, from(#3e779d), to(#65a9d7));
      background: -webkit-linear-gradient(top, #3e779d, #65a9d7);
      background: -moz-linear-gradient(top, #3e779d, #65a9d7);
      background: -ms-linear-gradient(top, #3e779d, #65a9d7);
      background: -o-linear-gradient(top, #3e779d, #65a9d7);
      padding: 12.5px 25px;
      -webkit-border-radius: 8px;
      -moz-border-radius: 8px;
      border-radius: 8px;
      -webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;
      -moz-box-shadow: rgba(0,0,0,1) 0 1px 0;
      box-shadow: rgba(0,0,0,1) 0 1px 0;
      text-shadow: rgba(0,0,0,.4) 0 1px 0;
      color: white;
      font-size: 28px;
      font-family: Impact, Charcoal, sans-serif;
      text-decoration: none;
      vertical-align: middle;
    }
    .button:hover {
      border-top-color: #28597a;
      background: #28597a;
      color: #ccc;
    }
    .button:active {
      border-top-color: #1b435e;
      background: #1b435e;
    }

    h1 {
      font-size: 1000%;
      font-weight: normal;
      margin-bottom: 0em;
      text-shadow: 5px 5px 5px #000080;
    }
    h2 {
      font-size: 400%;
      font-weight: normal;
      margin-bottom: 0em;
    }

    input[type=text] {
      width: 300px;
      display: block;
      margin-bottom: 10px;
      margin-left: auto;
      margin-right: auto;
      background-color: #CCFFFF;
      font-size: 200%;
    }

    input[type=button] {
      width: 120px;
      margin-left: 35px;
      display: block;
    }
  </style>
</head>

<body id="sample">
  <div class="textColumn">
    <h1>GroupThis!</h1>

    <form name="input" action="" method="get">
      User:<input type="text" name="Name" value="" size="80">
      Password:<input type="text" name="Name" value="" size="80">
      <button class="button"> GO! </button>
    </form>
  </div>

</body>
</html>

"""

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print "Serving on port 8000..."
    httpd.serve_forever()
