#!/usr/bin/env python
# coding: utf-8

# # setting

# In[1]:


import os
import data_tpl
from jinja2 import DictLoader
from nbconvert import HTMLExporter
import sys

# In[2]:


# pyinstallerからカレントディレクトリを取得するための関数
# why? カレントディレクトリがデフォルトだとhomeに変更されていて、データの出力先を制御しにくいためこの関数を定義。
def mypath():
    import sys
    from pathlib import Path

    p = Path(sys.argv[0])
    if p.suffix == ".exe" or p.suffix == ".py":
        return p.parent

    return p.parent


def tpl_path():
    import sys
    from pathlib import Path

    p = Path(sys.argv[0])
    if p.suffix == ".exe" or p.suffix == ".py":
        return p.parent
    else:
        return sys._MEIPASS + "/"


# In[3]:


# pathの参照先を確認
# why? もともと開発をjupyter notebook でやっていたため、pyinstaller特有のpathへ変更されることを確認するため。
print("mypath", mypath())


if "__file__" in locals():
    print("__file__", __file__)
else:
    print("__file__", "is not defined")


# # INPUT_PATH

# In[4]:


if "get_ipython" in globals():
    INPUT_PATH = "./"  # from jupyter notebook
else:
    INPUT_PATH = str(mypath()) + "/"  # from exefile


inpath_notebooks = []
for i in os.listdir(INPUT_PATH):
    if i.endswith(".ipynb"):
        inpath_notebooks.append(INPUT_PATH + i)

outpath_notebooks = list(map(lambda x: x.replace(".ipynb", ".html"), inpath_notebooks))

for i in list(zip(inpath_notebooks, outpath_notebooks)):
    print("input and output files:", i)


# # main

# In[5]:


# 変換元となるipynbをテキストとして読み込む
def readFile(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


target_notebook_list = list(map(lambda x: readFile(x), inpath_notebooks))


# In[6]:


# テキストデータをnotebook形式に変換
import nbformat

target_notebook_nb = list(
    map(lambda x: nbformat.reads(str(x), as_version=4), target_notebook_list)
)

print(target_notebook_nb[0].cells[0])


# In[7]:


# jinja2の形式で書かれたtplファイルを複数読み込む
dl = DictLoader(data_tpl.dict_tpl)
exportHTML = HTMLExporter(
    template_name="classic",
    template_paths=[
        tpl_path() + "templates/",
        tpl_path() + "templates/base/",
        tpl_path() + "templates/classic/",
    ],
    extra_loaders=[dl],
)
exportHTML.template_file = "toc2.tpl"


# In[8]:


# htmlファイルへ変換
for notebook, outpath in zip(target_notebook_nb, outpath_notebooks):
    (body, resources) = exportHTML.from_notebook_node(notebook)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(body)
