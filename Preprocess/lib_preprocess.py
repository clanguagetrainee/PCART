import re
import os
import sys

def lib_sub(part_before,part_after,file_path):          #简单相减嘛
    with open(file_path,'w',encoding='UTF-8') as fr:
        for key,value in part_before.items():
            fr.write(40*"-"+key+40*"-"+'\n')
            if key not in part_after:
                for line in part_before[key].split('\n'):
                    if line!='' and line[0] not in ['A','-']:
                        fr.write(line+'\n')
            else:
                for line in value.split('\n'):
                    if line!='' and line[0] not in ['A','-'] and line not in part_after[key].split('\n'):
                        fr.write(line+'\n')
                    
        

def lib_dif_Process(libName,currentVersion,targetVersion):
    Path_f=f'Cache/{libName}/{currentVersion}-{targetVersion}'
    Path_b=f'Cache/{libName}/{targetVersion}-{currentVersion}'
    Path_deprecated=f'Cache/{libName}/{currentVersion}_{targetVersion}'
    if os.path.exists(Path_deprecated):
        return  #两个文件都有了直接返回

    if not os.path.exists(f'Cache/{libName}'):
        os.mkdir(f'Cache/{libName}')

    current_lib_path=f'LibAPIExtraction/{libName}/{libName}{currentVersion}'
    target_lib_path=f'LibAPIExtraction/{libName}/{libName}{targetVersion}'
    if not os.path.exists(current_lib_path) or not os.path.exists(target_lib_path):
        print("The libraries API information is missing and needs to be extracted first.")
        sys.exit(0)
    else:
        separator_pattern = r"^-{40}.+-{40}$"
        cur_parts={}        #两个版本的文件名：API的键值对
        tar_parts={}
        with open(current_lib_path,'r',encoding='UTF-8') as fr:
            code=fr.read()
            matches = re.findall(separator_pattern,code, flags=re.MULTILINE)
            Len=len(matches)
            for i in range(Len-1):
                temp=code.split(matches[i])[-1]     #两段横线间是这一段的API
                temp=temp.split(matches[i+1])[0]
                temp=temp.rstrip('\n').lstrip('\n')                #删掉末尾的空白行
                
                temp2=temp.split('\n')
                temp2=[line.split('(')[0] for line in temp2]
                temp='\n'.join(temp2)
                key=matches[i].lstrip('-').rstrip('-')     #key是文件名
                key=key.split(f'{libName}{currentVersion}/')[-1]
                cur_parts[key]=temp
            temp=code.split(matches[Len-1])[-1]     #最后一段单独处理
            temp=temp.rstrip('\n').lstrip('\n')
            temp2=temp.split('\n')
            temp2=[line.split('(')[0] for line in temp2]
            temp='\n'.join(temp2)

            key=key.split(f'{libName}{currentVersion}/')[-1]
            cur_parts[key]=temp

              
        with open(target_lib_path,'r',encoding='UTF-8') as fr:
            code=fr.read()
            matches = re.findall(separator_pattern,code, flags=re.MULTILINE)
            Len=len(matches)
            for i in range(Len-1):
                temp=code.split(matches[i])[-1]     #两段横线间是这一段的API
                temp=temp.split(matches[i+1])[0]
                temp=temp.rstrip('\n').lstrip('\n')                 #删掉末尾的空白行
                
                temp2=temp.split('\n')
                temp2=[line.split('(')[0] for line in temp2]
                temp='\n'.join(temp2)                 #删掉末尾的空白行
                key=matches[i].lstrip('-').rstrip('-')     #key是文件名
                key=key.split(f'{libName}{targetVersion}/')[-1]
                tar_parts[key]=temp
            temp=code.split(matches[Len-1])[-1]     #最后一段单独处理
            temp=temp.rstrip('\n').lstrip('\n')
            temp2=temp.split('\n')
            temp2=[line.split('(')[0] for line in temp2]
            temp='\n'.join(temp2)
            key=key.split(f'{libName}{targetVersion}')[-1]
            tar_parts[key]=temp
    if not os.path.exists(Path_f):
        lib_sub(cur_parts,tar_parts,Path_f)
    if not os.path.exists(Path_b):
        lib_sub(tar_parts,cur_parts,Path_b)
    
    code_cur=[]
    code_tar=[]

    with open(Path_b,'r',encoding='UTF-8') as fr:
        code_tar=fr.readlines()
        code_tar=[line for line in code_tar if line[0] != '-']
    with open(Path_f,'r',encoding='UTF-8') as fr:
        code_cur=fr.readlines()
        code_cur=[line for line in code_cur if line not in code_tar]
    with open(Path_deprecated,'w',encoding='UTF-8') as fr:
        l=len(code_cur)
        for i in range(l-1):
            if code_cur[i][0]=='-' and code_cur[i+1][0]=='-' :
                continue
            fr.write(code_cur[i])
        if code_cur[l-1][0]!='-':
            fr.write(code_cur[l-r])