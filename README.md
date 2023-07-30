# ipynb2html

![demo](https://github.com/dai-a/ipynb2html-EXE/wiki/images/output.gif)



# os
macOS Mojave 10.14.5

# env and run

## env
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.9.4<br>
pyenv global 3.9.4<br>
pip3 install -U pip<br>
pip3 install pyinstaller<br>
pip3 install jupyter<br>

## run
pyinstaller ipynb2html.py \
    --onefile \
    --add-data "./data_tpl.py:." \
    --add-data "./py374/share/jupyter/nbconvert/templates/classic:./templates/classic"  \
    --add-data "./py374/share/jupyter/nbconvert/templates/base/:./templates/base"
or 
pyinstaller ipynb2html_add_py.py --onefile

