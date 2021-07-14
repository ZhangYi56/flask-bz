@echo off 
if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin
set PYTHONPATH=.
set PATH=%PATH%
twistd -n web --port tcp:5555 --wsgi app.app
