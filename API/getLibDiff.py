import re
import os
import sys
from Path.getPath import getRelativePath

## 利用两个版本库 文件：API 字典 相减获取差值的函数
#
#  使用库文件：API字典partBefore减去字典partAfter，获取每个文件下partBefore->partAfter弃用的API
#  @param libName 待相减库的库名
#  @param partBefore 被减库的文件: API 字典
#  @param partAfter 减库的文件: API 字典
#  @param file_path 相减后得到的差值文件的路径
def subLibInfo(libName,partBefore,partAfter,file_path):          #简单相减嘛
    with open(file_path,'w',encoding='UTF-8') as fr:
        for key,value in partBefore.items():
            fr.write(40*"-"+key+40*"-"+'\n')    #文件相对路径信息组成的文件分隔行 如：----------------------------------------torch/functional.py----------------------------------------
            if key not in partAfter:
                for line in partBefore[key].split('\n'):
                    if line!='':
                        fr.write(line+'\n')
            else:
                partAfterLines=partAfter[key].split('\n')   #partAfter在当前key下的API列表
                for line in value.split('\n'):
                    if line!='' and line not in partAfterLines:
                        fr.write(line+'\n')

## 获取库的 文件：API 字典 的函数
# 
#  对file_path下的存储的库API信息，提取出 文件相对路径：API 的字典
#  @param file_path 存放着待生成字典的库API信息文件的路径
#  @param libName 待处理库的库名                        
def getLibDict(file_path,libName):
    separator_pattern = r"^-{40}.+-{40}$"  ##< 文件名的匹配模式                 
    LibDict={}  ##< 用于存储返回值的字典
    code=''
    with open(file_path,'r',encoding='UTF-8') as fr:
        code=fr.read()
    matches = re.findall(separator_pattern,code, flags=re.MULTILINE)
    Len=len(matches)
    for i in range(Len):
        if (i==Len-1):
            tempAPIs=code.split(matches[i])[-1]
        else:
            tempAPIs=code.split(matches[i])[-1]             #两段横线间是这一段的API
            tempAPIs=tempAPIs.split(matches[i+1])[0]
        completeAPIs=tempAPIs.rstrip('\n').lstrip('\n')     #删掉末尾的空白行
                
        completeAPILst=completeAPIs.split('\n')             # 将字符串划分为列表去除后面的参数部分 
                                                            # 如： torch.functional.lu_unpack(LU_data,LU_pivots,unpack_data=True,unpack_pivots=True)
                                                            #        -> torch.lu_unpack

        APINameLst=[line.split('(')[0] for line in completeAPILst if line[:2] != 'A:']
        APINames='\n'.join(APINameLst)

        key=matches[i].lstrip('-').rstrip('-')     # key是库的文件相对路径  
                                                   # 如：  ----------------------------------------torch/functional.py----------------------------------------
                                                   #          ->   torch/functional.py
        #if key not in ['Modules_with_namespacePackages','Modules_without_namespacePackages']:  #Py3.3
        if key !='Modules':   
            key=getRelativePath(key,libName)
        LibDict[key]=APINames
    return LibDict
   
## 两版本的库的API弃用情况生成的函数
#  
#  获取libName这个库，的currentVersion-targetVersion, targetVersion-currentVersion的两个 文件粒度下API的差值信息，
#  以及currentVersion->targetVersion的API弃用情况
#  @param libName 待处理的库的名称
#  @param currentVersion 旧版本的库版本号
#  @param targetVersion 新版本的库版本号
#  @param config 输入的配置文件名
def getLibDiff(libName,currentVersion,targetVersion,config):      
    CsubTFilePath=f'LibAPIExtraction/API_libDiff/{libName}/{currentVersion}sub{targetVersion}'   ##< 在文件粒度上current版本的相较target版本多出的API的信息的记录文件存储路径
    TsubCFilePath=f'LibAPIExtraction/API_libDiff/{libName}/{targetVersion}sub{currentVersion}'   ##< 在文件粒度上target版本的相较current版本多出的API的信息的记录文件存储路径
    deprecatedFilePath=f'LibAPIExtraction/API_libDiff/{libName}/{currentVersion}_{targetVersion}'    ##< 在整个库的层面上，current->target的弃用的API的记录文件保存路径

    if not os.path.exists(f'LibAPIExtraction/API_libDiff'):     #这里是创建保存路径中的文件夹
        os.mkdir(f'LibAPIExtraction/API_libDiff')
    if not os.path.exists(f'LibAPIExtraction/API_libDiff/{libName}'):
        os.mkdir(f'LibAPIExtraction/API_libDiff/{libName}')

    if not os.path.exists(CsubTFilePath) or not os.path.exists(TsubCFilePath):      #没有sub文件的情况则获取sub文件
        currentLibInfoPath=f'LibAPIExtraction/{libName}/{libName}{currentVersion}'
        targetLibInfoPath=f'LibAPIExtraction/{libName}/{libName}{targetVersion}'
        if not os.path.exists(currentLibInfoPath) or not os.path.exists(targetLibInfoPath):
            print(f"The libraries API information is missing and needs to be extracted first.\n\nUse 'python extractLibAPI.py -cfg {config}' to obtain the lib's API documentation.")#详细操作
            sys.exit(0)
        else:
            currentDict=getLibDict(currentLibInfoPath,libName)
            targetDict=getLibDict(targetLibInfoPath,libName)
            subLibInfo(libName,currentDict,targetDict,CsubTFilePath)
            subLibInfo(libName,targetDict,currentDict,TsubCFilePath)

    if not os.path.exists(deprecatedFilePath):              #没有弃用文件则获取弃用文件
        newAddAPIs=[]       #Target sub Current中的API的弃用信息
        targetModuleInfo=[]         #Target版本中的模块记录（P+M)
        #lowVersionTargetModuleInfo=[]  #Py3.3
        deprecatedFileLines=[]      #最终弃用文件的行保存列表
        with open(TsubCFilePath,'r',encoding='UTF-8') as fr:         #这里提取的新增API的列表
            targetInfo=fr.readlines()
            newAddAPIs=[line for line in targetInfo if line[0] != '-'] 
        try:                                                  #这里考虑到模块和包有可能相同路径的情况，提取目标版本的源文件的所有模块信息来作为判断  
            targetLibInfoPath=f'LibAPIExtraction/{libName}/{libName}{targetVersion}'    #TODO: 这里的路径可不止一条     
            with open(targetLibInfoPath,'r',encoding='UTF-8') as fr:
                content=fr.read()

                sep=40*'-'+'Modules'+40*'-'+'\n'
                #sep1=40*'-'+'Modules_with_namespacePackages'+40*'-'+'\n'
                #sep2=40*'-'+'Modules_without_namespacePackages'+40*'-'+'\n'        #Py3.3

                #partWith=content.split(sep1)[-1]
                #partWith=partWith.split(sep2)[0]

                #partWithout=content.split(sep2)[-1]
                #partWithout=partWithout.split(40*'-')[0] 

                partWith=content.split(sep)[-1]
                partWith=partWith.split(40*'-')[0] 

                targetSourceInfo=partWith.split('\n')
                #lowVersionTargetModuleInfo=partWithout.split('\n')
                
        except FileNotFoundError:
            print(f"The libraries API information is missing and needs to be extracted first.\n\nUse 'python extractLibAPI.py -cfg {config}' to obtain the lib's API documentation.")
            exit(0)

        with open(CsubTFilePath,'r',encoding='UTF-8') as fr:
            currentInfo=fr.readlines()          #Current - Target 弃用文件的内容
            moduleCompareSwitch=0           #用来确定模块的弃用比较列表
            for line in currentInfo:
                #if line==40*'-'+'Modules_without_namespacePackages'+40*'-':    #Py3.3
                #    moduleCompareSwitch=1

                if line[:2] in ['M:','P:']:             #对于弃用的模块信息进行判断是否记录到弃用中
                    if moduleCompareSwitch==0:#开关为0这里是对包含namespace包的模块弃用信息的比较收集
                        if 'M:'+line[2:] not in targetModuleInfo and 'P:'+line[2:] not in targetModuleInfo:
                            deprecatedFileLines.append(line[2:])
                        else:
                            pass
                    #else:                     #开关为1这里对低版本的模块弃用信息的比较收集Py3.3
                        #if 'M:'+line[2:] not in lowVersionTargetModuleInfo and 'P:'+line[2:] not in lowVersionTargetModuleInfo:
                            #deprecatedFileLines.append(line[2:])
                        #else:
                            #pass
                else:
                    if line not in newAddAPIs:          #对于普通API等信息的判断，其中特殊的API，全局别名，全局容器也只以API接口名称的形式存储
                        if line[:2] in ['L:','C:']:
                            line=line[2:]
                            line=line.split('->')[0]
                        deprecatedFileLines.append(line)    
                    else:
                        pass
        with open(deprecatedFilePath,'w',encoding='UTF-8') as fr:       #这里对空的文件路径进行删除后写入弃用文件中
            l=len(deprecatedFileLines)

            importantTag=40*'-'+'Modules'+40*'-'+'\n'
            #importantTag1=40*'-'+'Modules_with_namespacePackages'+40*'-'+'\n'
            #importantTag2=40*'-'+'Modules_without_namespacePackages'+40*'-'+'\n'
            for i in range(l-1):
                if deprecatedFileLines[i] !=importantTag  and deprecatedFileLines[i][0]=='-' and deprecatedFileLines[i+1][0]=='-' :
                    continue
                fr.write(deprecatedFileLines[i])
            if deprecatedFileLines[l-1][0]!='-':
                fr.write(deprecatedFileLines[l-1])