import os
import json
from core.server import server_action
from main import app
from datetime import datetime

def redoc_export():
    """
    Script to export the ReDoc documentation page into a standalone HTML file.
    Created by https://github.com/pawamoy on https://github.com/Redocly/redoc/issues/726#issuecomment-645414239
    """

    HTML_TEMPLATE = """<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <title>My Project - ReDoc</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
        <style data-styled="" data-styled-version="4.4.1"></style>
    </head>
    <body>
        <div id="redoc-container"></div>
        <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
        <script>
            var spec = %s;
            Redoc.init(spec, {}, document.getElementById("redoc-container"));
        </script>
    </body>
    </html>
    """
    
    date_time = (datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    file_name = f"/api-docs-{date_time}.html"
    directory = "../documentation/redoc"
    
    if not os.path.exists(directory):
        os.mkdir(directory)

    @server_action
    def func():
        with open(directory + file_name, "w",) as fd:
            print(HTML_TEMPLATE % json.dumps(app.openapi()), file=fd)
            print("Archivo ReDoc creado correctamente en: " + directory + file_name)