import ast
#访问import节点和importFrom节点
class Import(ast.NodeVisitor):
    def __init__(self):
        self._md_name={}

    def get_md_name(self):
        return self._md_name

    def visit_Import(self, node):
        item=[nn.__dict__ for nn in node.names] #item中每个元素都是一个字典
        for it in item:
            if it["asname"] is None:
                self._md_name[it["name"]]=it["name"]
            else:
                self._md_name[it["asname"]]=it["name"]

    def visit_ImportFrom(self, node):
        if node.module is not None:
            item=[nn.__dict__ for nn in node.names]
            for it in item:
                if it["asname"] is None:
                    self._md_name[it["name"]]=node.module+'.'+it["name"]
                else:
                    self._md_name[it["asname"]]=node.module+'.'+it["name"]



#从根节点开始，直接找根节点的孩子，Call存在于Expr和Assign节点中
class GetFuncCall:
    def __init__(self):
        self._func_call=[] #list中每个元素都是一个tuple

    @property
    def func_call(self):
        return self._func_call

    #采用深度遍历,先一直往下走
    #结束条件：遇到Call节点或当前节点无子节点
    def dfsVisit(self,node):
        #先递推再回归 
        for n in ast.iter_child_nodes(node):
            self.dfsVisit(n)
        
        if isinstance(node,ast.Call):
            callName=ast.unparse(node.func)
            callState=ast.unparse(node) #还原之后的语句可能和项目中的语句存在差异，比如空格等
            argLst=[]
            for arg in node.args:
                argLst.append(ast.unparse(arg))
            for keyword in node.keywords:
                argLst.append(ast.unparse(keyword))
            parameters=','.join(argLst)
            if (callName,parameters,callState,node.lineno) not in self._func_call:
                # print(node.lineno,'<-->',callState)
                self._func_call.append((callName,parameters,callState,node.lineno)) #四元组：callAPI名，callAPI参数，...
            else:
                pass
                # print(node.lineno,'<-->',callState)
            return


#找到所有的Assign节点
#对于Assign节点，只需要关注等号左右两边的名字   
class AssignVisitor(ast.NodeVisitor):       #这里是不是对所有右侧为调用语句可能出现别名的情况做了记录，如果对全局和非全局的API重命名进行区分，可以更为精确的恢复
    def __init__(self):
        self._targetCall={} #记录的是，库中的函数调用，类实例化，以及类中方法的调用（恢复了路径）语句的记录
        self._alias={}      #这里记录别名信息，那么对于弃用后调用其它api的兼容性保持情况就能识别出来
        self._container=[]  #库中可以调用的容器API，包括了字典、列表、集合。不需要记录等式右边中存储的字典内容

    def get_target_call(self):
        return self._targetCall
    
    def get_alias_API(self):
        return self._alias
    
    def get_container(self):
        return self._container

    def visit_Assign(self,node):       #TODO: 局部声明的全局容器和别名信息
        if isinstance(node.value,ast.Call):
            targetName=ast.unparse(node.targets)
            valueExpr=ast.unparse(node.value)
            self._targetCall[targetName]=valueExpr
    
    def visit(self,node):        #这里对顶层的结点：全局的容器和别名信息的记录
        if isinstance(node, ast.Module):
            for global_node in node.body:
                if isinstance(global_node, ast.Assign):     #TODO:对全局的API重命名记录后如何获取完整的原API信息
                    if isinstance(global_node.value,(ast.Dict,ast.List)):       #对于[],{}声明的全局容器
                        if ast.unparse(global_node.targets)=='__all__':     #all这个全局容器没用，不是api
                            pass
                        else:
                            self._container.append(ast.unparse(global_node.targets))
                    elif isinstance(global_node.value,ast.Call) and ast.unparse(global_node.value).split('(')[0] in ["dict","list","set"]: #对于dict(),list(),set()声明的全局容器
                        self._container.append(ast.unparse(global_node.targets))
                    elif isinstance(global_node.value,ast.Name):              
                        self._alias[ast.unparse(global_node.targets)]=ast.unparse(global_node.value)       #对全局赋值别名进行记录
        super().visit(node)
    
