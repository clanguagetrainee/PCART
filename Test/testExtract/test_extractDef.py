import unittest
import ast
from ...Extract.extractDef import *

class testFromImport(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        objectFromImport=FromImport()
    def teardown(self):
        objectFromImport._importDict={}
"""
这里是由from import 语句生成APi的缩短的替换字典。具体应该有以下几种测试及预计结果：
1. 从相对路径导入函数：from .moduleA import funcA   ——> {.moduleA.funcA: funcA}
2. 从默认路径导入函数：from moduleA import funcA    ——> {moduleA.funcA: funcA}
因为是init导入使用，这里在同级目录下其他模块只有非本模块（__init__.py）函数的导入的情况
3. 对当前init所在包的子包中的模块/模块的函数进行导入： from subPackage.moduleB import funcB  ——> {subPackage.moduleB.funcB: funcB}
4. 导入非当前包目录下的函数/模块 或 使用此方法子包/子模块/模块中的函数：
"""
    def test_visitImportFrom_01(self):
        setence="from a import b"
        node=ast.parse(setence)
