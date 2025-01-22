# Copyright © 2025 Alexei Bezborodov. Contacts: <AlexeiBv+obfuscator@narod.ru>
# License: Public domain: http://unlicense.org/


import enum
from enum import auto

class VarType(enum.Enum):
    LOCAL_VAR = auto()
    MEMBER_VAR = auto()
    CLASS_NAME = auto()
    FUNCTION_NAME = auto()

import re

pyton_templates = {
    VarType.LOCAL_VAR:      '(?:\A|;)\s*(\w+)\s*\=',
    VarType.MEMBER_VAR:     '(?:\A|;)\s*self\.([\w]+)\s*\=',
    VarType.CLASS_NAME:     '(?:\A|;)\s*class\s*([\w]+)\s*[:(]',
    VarType.FUNCTION_NAME:  '(?:\A|;)\s*def\s*([\w]+)\s*\(',
}

def PythonFindAll(text):
    result = [];
    for t in VarType:
        result += PythonFind(t, text)
    return result

def PythonFind(var_type, text):
    return re.findall(pyton_templates.get(var_type), text)

def Test():
    def isEqualArray(a, b):
        return str(a) == str(b)

    text = "\tx   = 234 ; yD1 = 123;a3=1;\tself.d31 = 23;"
    text1 = "\t   def   Test1 (sdfd): return;"
    text2 = "\t   class   Test2 (enum):"
    text3 = "\t   class   Test3 :"

    matches_var = PythonFind(VarType.LOCAL_VAR, text)
    matches_class_var = PythonFind(VarType.MEMBER_VAR, text)
    matches_func = PythonFind(VarType.FUNCTION_NAME, text1)
    matches_class1 = PythonFind(VarType.CLASS_NAME, text2)
    matches_class2 = PythonFind(VarType.CLASS_NAME, text3)

    matches_all = PythonFindAll(text + text1 + text2)

    assert isEqualArray(matches_var, ['x', 'yD1', 'a3']), matches_var
    assert isEqualArray(matches_class_var, ['d31'])
    assert isEqualArray(matches_func, ['Test1'])
    assert isEqualArray(matches_class1, ['Test2'])
    assert isEqualArray(matches_class2, ['Test3'])
    assert isEqualArray(matches_all, ['x', 'yD1', 'a3', 'd31', 'Test2', 'Test1']), matches_all

Test()


import sys
import random

def MakeRandomName(size):
    rand_word = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_"
    rand_dig = "1234567890"
    def RandWord(s):
        return random.choice(s)
    
    result = RandWord(rand_word)
    for i in range(size - 1):
        result += RandWord(rand_word + rand_dig)
    return result

def Obfuscator(in_file):
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()

    matches = []
    for l in lines:
        matches += PythonFindAll(l)

    rand_matches = []
    for m in matches:
        rand_matches += [MakeRandomName(16)]

    f = open(in_file+".map.txt", 'wb')
    for i in range(len(matches)):
        l = rand_matches[i] + '=' + matches[i] + "\n"
        f.write(l.encode('utf-8'))
    f.close()

    f = open(in_file+".ob.py", 'wb') #, encoding='utf-8')
    for l in lines:
        for i in range(len(matches)):
            l = re.sub(r"\b%s\b" % matches[i], rand_matches[i], l) #l.replace(matches[i], rand_matches[i])  # r"(:?\A|\s*|;)"+matches[i]+"(:?\Z|\s*|;|\(|\))"

        f.write(l.encode('utf-8'))
    f.close()

files_to_work = []

if __name__ == "__main__":
    for i in range(len(sys.argv)):
        param = sys.argv[i]
        if i > 0:
            files_to_work.append(param)

for f in files_to_work:
    Obfuscator(f)


