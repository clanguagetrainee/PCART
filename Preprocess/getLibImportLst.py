import os
import re
import ast
from Path.getPath import *

## 获取路径项目中设计到目标库的import语句
#  
#  对projPath指向的路径下的项目，遍历其中的.py文件，提取其中涉及到libName的相关import语句
#  @param projPath 待提取项目的路径
#  @param libName 待检测的第三方库
def getLibImportLst(projPath,libName):
    lst=[]
    pathObj=Path('DF')
    pathObj.getPath(projPath)
    filePath=[file for file in pathObj.path if file.endswith('.py')]
    pattern=rf"(from {libName}|import {libName})" #确保库的前面不会出现其它字符
    for file in filePath:#下面的所有操作都是对项目副本进行的
        with open(file,'r') as fr:
            code=fr.read()
        try:
            root=ast.parse(code,filename='<unknown>',mode='exec')
            for node in ast.walk(root):
                if isinstance(node,ast.Import) or isinstance(node,ast.ImportFrom):
                    s=ast.unparse(node)
                    if bool(re.search(pattern,s)):
                        lst.append(s)
        except Exception as e:
            print(f"getLibImportLst: ast parse failed, {file}, {e}")


    ansLst=list(set(lst))
    ansLst.sort(key=lst.index) 
    return ansLst 