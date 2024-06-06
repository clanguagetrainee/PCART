import sys
import json
from Path.getPath import *
from Extract.getDef import get_def_function
from multiprocessing import Pool
from Tool.tool import getSourceCodePath

def extractLibAPI(version, sourceCodePath):
    libName=sourceCodePath.split('/')[-1]
    get_def_function((libName, version, sourceCodePath))



if __name__=='__main__':
    config=sys.argv[2]
    currentVersion, targetVersion, currentSourceCodePath, targetSourceCodePath = getSourceCodePath(config)
    
    # print(currentVersion, currentSourceCodePath)
    # print(targetVersion, targetSourceCodePath)

    extractLibAPI(currentVersion, currentSourceCodePath)
    extractLibAPI(targetVersion, targetSourceCodePath) 