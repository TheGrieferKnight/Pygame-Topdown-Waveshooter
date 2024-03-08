for /f "usebackq tokens=* delims=" %%a in ("player.py") do (echo(%%a)>>~.py
move /y  ~.py "player.py"