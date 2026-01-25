#!/usr/bin/python -u
# -*- coding: utf-8 -*-
## 
## (C) 2013-2015 Muthiah Annamalai,
## Licensed under GPL Version 3
## 
## Ezhil language Interpreter via Web

## Ref: http://wiki.python.org/moin/BaseHttpServer

import time

import sys, os
from random import choice

# NB: this program imports Ezhil library from the installed version
from ezhil import EzhilFileExecuter #, EzhilInterpExecuter
from contextlib import redirect_stdout
import io 
import json

class EzhilWeb():
    """ Class that does the job on construction """
    def __init__(self,debug = False):
        self.debug = debug
        self.img_outcome = '' #image str indicating success/failure
        if ( self.debug ):
            # debugging tips
            import cgitb
            cgitb.enable()
        
        self.form = cgi.FieldStorage()
        try:
            program = self.form.getvalue('prog')
        except Exception as e:
            print("could not load the program from GET method, exception ",str(e))
        finally:
            if ( not program ):
                program = "printf(\"You can write Tamil programs from your browser!\")"
        
        if ( self.debug ):
            print(str(program))
        
        self.do_ezhil_execute( program )
    
    @staticmethod
    def get_image( kind ):
        if kind == 'success':
            img = choice(['trophy-gold','trophy-silver','trophy-bronze'])
        else:
            img = choice(['dialog-warning','software-update-urgent','stock_dialog-error'])
        img = img + '.png'
        return img
    
    @staticmethod
    def error_qualifiers( progout ):
        """ filter program execution output for Ezhil interpreter or Python stack traces"""
        FAILED_STRINGS = ["Traceback (most recent call last)",
                          "Run-time error Cannot Find Identifier"]
        return any([x for x in FAILED_STRINGS if progout.find(x) > -1])
    
    def do_ezhil_execute(self,program):
        progin = ''
        evaluated = False
        failed = False
        progout = ''
        exception = ''
        try:
            print("Starting to Ezhil file executer")
            evaluated = True
            # 10s timeout and executor 
            with io.stringIO() as output_buffer:
                with redirect_stdout(output_buffer):
                    EzhilFileExecuter(file_input = [program],debug=self.debug,redirectop=False,TIMEOUT=10)
                    progout = output_buffer.getvalue()

        except Exception as e:
            exception = str(e)
            failed = True

        response_dict = {
                        'evaluated_flag':evaluated,
                        'failed_flag':failed,
                        'program_input':progin,
                        'program_output':progout, 
                        'exception_message':exception
                         }
        return json.dump(response_dict)


def saveYourCode( program ):
    tprefix = time.ctime().replace(' ','_').replace(':','_')
    return """<TR><TD>
<a  href="javascript:download('"""+"ezhil_program_"+tprefix+".n','"+program.replace('\n','\\n').replace('"','\"').replace(">","&gt;").replace("<","&lt;")+"""')">உங்கள் நிரலை சேமிக்க (save your code)</a></TD></TR>"""

if __name__ == '__main__':
    print("Content-Type: text/html")    # HTML is following
    print("")                              # blank line, end of headers
    # do the Ezhil thing
    EzhilWeb(debug=False)
