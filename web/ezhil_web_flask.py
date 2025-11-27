#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import sys
from random import choice
from flask import Flask, request, render_template_string

from ezhil import EzhilFileExecuter

app = Flask(__name__)


def saveYourCode(program):
    tprefix = time.ctime().replace(' ', '_').replace(':', '_')
    program = program.replace('\n','\\n').replace('"','\\"').replace(">","&gt;").replace("<","&lt;")
    return f"""
    <tr><td>
    <a href="javascript:download('ezhil_program_{tprefix}.n','{program}')">
    உங்கள் நிரலை சேமிக்க (save your code)
    </a>
    </td></tr>
    """


class EzhilWeb:
    @staticmethod
    def get_image(kind):
        if kind == 'success':
            img = choice(['trophy-gold', 'trophy-silver', 'trophy-bronze'])
        else:
            img = choice(['dialog-warning', 'software-update-urgent', 'stock_dialog-error'])
        return img + '.png'

    @staticmethod
    def error_qualifiers(progout):
        FAILED_STRINGS = [
            "Traceback (most recent call last)",
            "Run-time error Cannot Find Identifier"
        ]
        return any(s in progout for s in FAILED_STRINGS)

    def do_ezhil_execute(self, program):
        failed = False

        # Format program lines
        program_fmt = "<table><tr><td><table><tr><td><font color='blue'><ol>"
        program_fmt += "\n".join([f"<li>{line}</li>" for line in program.split("\n")])
        program_fmt += "</ol></font></td></tr></table></td><td>"

        try:
            obj = EzhilFileExecuter(
                file_input=[program],
                redirectop=True,
                TIMEOUT=120
            )

            obj.run()
            f1, f2, progout = obj.get_output()

            # cleanup
            for f in [f1, f2]:
                try:
                    os.unlink(f)
                except:
                    pass

            if obj.exitcode != 0 and self.error_qualifiers(progout):
                failed = True
                img_tag = f"<img width='64' src='/static/icons/{self.get_image('failure')}' alt='failure'/>"
                op = f"{program_fmt}<b>{img_tag} Failed Execution</b><br/><pre>{progout}</pre></td></tr></table>"
            else:
                failed = False
                img_tag = f"<img width='64' src='/static/icons/{self.get_image('success')}' alt='success'/>"
                op = f"{program_fmt}<b>{img_tag} Succeeded</b><br/><pre>{progout}</pre></td></tr>"
                op += saveYourCode(program)
                op += "</table>"

        except Exception as e:
            failed = True
            img_tag = f"<img width='64' src='/static/icons/{self.get_image('failure')}' alt='failure'/>"
            op = f"{program_fmt}<b>{img_tag} FAILED</b><br/><pre>{str(e)}</pre></td></tr>"
            op += saveYourCode(program)
            op += "</table>"

        header = (
            "<h2>Your program has some errors! Try correcting it.</h2><hr/>"
            if failed else
            "<h2>Your program executed correctly! Congratulations.</h2><hr/>"
        )

        return header + op


@app.route("/", methods=["GET", "POST"])
def home():
    program = request.form.get("prog")

    if not program:
        program = 'printf("You can write Tamil programs from your browser!")'

    executor = EzhilWeb()
    html_output = executor.do_ezhil_execute(program)

    # wrap inside minimal HTML
    page = f"""
    <html>
    <head>
        <title>Ezhil Interpreter</title>

        <script src="/static/js/Blob.js"></script>
        <script src="/static/js/FileSaver.js"></script>

        <script>
        function download(filename, content) {{
            saveAs(new Blob([content], {{type: 'application/x-ezhil;charset=utf-8'}}), filename);
        }}
        </script>
    </head>

    <body>
        {html_output}
    </body>
    </html>
    """

    return render_template_string(page)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
