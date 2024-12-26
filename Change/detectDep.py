import os
import re
import ast
from Path.getPath import *
from Preprocess.getLibImportLst import getLibImportLst
from Extract.getCall import getCallFunction
from Path.getPath import Path
from  Load.loadData import loadDepAPILst

## 判断import语句是否失效
#
#  根据抽取statement访问了模块，api信息判断其是否被弃用来判断import语句是否失效
#  @param statement 待判断的import语句
#  @param targetModulesLst 目标库的模块列表
#  @param targetAPIsLst 目标库的API列表
def isImportDepr(statement,targetModulesLst,targetAPIsLst):         #TODO: 这里的import语句的 ./..情况的分析
    partLst=statement.split(' ')
    if partLst[1] not in targetModulesLst:   #第二部分的模块必须存在
        return True
    
    if len(partLst)>2 and partLst[2]!='as':   #from a import b情况下a.b也必须存在
        apiName='.'.join([partLst[1],partLst[3]])
        if apiName in targetAPIsLst or apiName in targetModulesLst:
            return False
        else:
            return True

## 用来实现对Import语句弃用情况的检测
#  
#  对于导入语句列表，实现对这些Import语句在目标版本是否被弃用（使用会发生报错）进行检测，返回被弃用的Import语句列表
#  @param libName 变更的两个版本库的库名
#  @param currentVersion 库的当前版本
#  @param targerVersion 库的目标版本
#  @param ImportLst 待检测的Import语句列表
#  @param lowVersionFlag 库运行环境python版本是否低于3.3版本标志
def detectImportDeprecated(libName,currentVersion,targetVersion,projPath,lowVersionFlag=0):
    targetModuelsLst=[] #目标版本的模块列表
    targetAPIsLst=[]    # 对于import语句中的API弃用情况检查需要目标版本所有的API列表
    targetAPIFilePath=f'LibAPIExtraction/{libName}/{libName}{targetVersion}'    # 这里是源API文件路径   TODO: 路径不止一种情况

    with open(targetAPIFilePath,'r') as fr:
        content=fr.read()

        #sep1=40*'-'+'Modules_with_namespacePackages'+40*'-'+'\n'
        #sep2=40*'-'+'Modules_without_namespacePackages'+40*'-'+'\n'
        #sep3=40*'-'
        #if lowVersionFlag==0:
            #ModuelLines=content.split(sep1)[-1]
            #ModuelLines=ModuelLines.split(sep2)[0]
        #else:
            #ModuelLines=content.split(sep2)[-1]
           # ModuelLines=ModuelLines.split(sep3)[0]
        sep1=40*'-'+'Modules'+40*'-'+'\n'
        sep2=40*'-'+'\n'
        ModuleLines=content.split(sep1)[-1]
        ModuleLines=ModuleLines.split(sep2)[0]
        targetModuelsLst=ModuleLines.split('\n')
        targetModuelsLst=[module[2:] for module in targetModuelsLst]#去掉前缀

        APIlines=content.split('\n')
        for line in APIlines:               #去掉前缀和无用行
            if line[:2] not in ['--','M:','P:','A:']:
                targetAPIsLst.append(line)
            elif line[:2] in ['L:','C:']:
                targetAPIsLst.append(line[2:])
            else:
                pass
    
    ImportLst=getLibImportLst(projPath,libName)
    deprecatedImportLst=[statement for statement in ImportLst if isImportDepr(statement,targetModuelsLst,targetAPIsLst)]
    return deprecatedImportLst



"""
对于弃用API的提取需要实现的是：
1. 提取所有API
2. 分析所有API的弃用情况，生成文档信息（使用的弃用API以及可能的推荐API）
    进一步：弃用API的参数，文件路径行号等信息（这里分开实现是因为getCallFunction函数只能提取出所有的API调用参数情况，路径等信息在覆盖阶段记录的）
3. 在后续的阶段上——覆盖API调用相关的信息文件进行判断是否需要处理API替换推荐
4. 考虑是否输出一个该项目的所有使用的弃用API的情况及替代API的文档说明（这里得捕捉更详细的信息）
"""

"""
对于API弃用推荐的文档信息的实现相关：
这里也考虑使用需要时再进行分析，对有分析过的记录作为库API弃用相关的信息记录下来
    这是考虑到提前将所有的弃用相关分析可能需要太大的空间以及用户期间处理整个库又会增加时间开销
    因此可以每次只分析项目中的弃用api，而且可以增加一个推荐可靠的用户判断，既提供了推荐API给用户，用户的测试结果又可以作为反馈存储在cache中
    还有更多的可实现操作
"""




## 用来实现对弃用API的检测
#
#  提取projPath中所有.py文件的目标库的API调用并对其弃用情况进行分析，返回所有的弃用API
#  param libName 目标库库名
#  param projPath 项目库的路径
#  param currentVersion 项目库的当前版本
#  param targetVersion 项目库的目标版本
def detectAPIDep(libName,projPath,currentVersion,targetVersion):
    fileInfo=Path('DF')
    fileInfo.getPath(projPath)      #获取所有的.py文件
    fileLst=fileInfo.path
    fileLst=[file for file in fileLst if file[-3:]=='.py']   

    mayCalledAPIs=[]        #整个项目中可能调用到的API
    for file in fileLst:
        _,tempCalledAPIsDict=getCallFunction(file,libName)   # 返回值是两个字典，第二个是  调用信息：参数信息 的字典，这里只需要第二个字典
        for detail,param in tempCalledAPIsDict.items():
            formatDetail=detail.replace(' ','')
            formatParam=param.replace(' ','')
            if f'({formatParam})' not in formatDetail:
                print("Change.detectAPIDep.detectAPIDep格式可能需要处理一下，并不是规范的")
            else:
                calledAPI=formatDetail.split(f'({formatParam})')[0]
                if calledAPI not in mayCalledAPIs:
                    mayCalledAPIs.append(calledAPI)

    deprecatedAPILst=loadDepAPILst(libName,currentVersion,targetVersion)        #这里时库版本发生变更时所有的弃用API的列表
    projDeprecatedAPILst=[API for API in mayCalledAPIs if API in deprecatedAPILst]
    return projDeprecatedAPILst
    
