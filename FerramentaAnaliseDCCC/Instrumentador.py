from Parser import *

def parse_test(filepath):
    print("Function Declarations")
    funcDeclList = get_FuncDecls(filepath)
    for Decl in funcDeclList:
        Decl.show()
    
    # funcCallList = get_FuncCalls(filepath)
    # for Call in funcCallList:
    #     Call.show()

    # funcDefList = get_FuncDefs(filepath)
    # for Def in funcDefList:
    #     Def.show()

    