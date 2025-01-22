# Copyright © 2025 Alexei Bezborodov. Contacts: <AlexeiBv+obfuscator@narod.ru>
# License: Public domain: http://unlicense.org/


import enum
from enum import auto

class VarType(enum.Enum):
    LOCAL_VAR = auto()
    MEMBER_VAR = auto()
    CLASS_NAME = auto()
    FUNCTION_NAME = auto()
    FOR_VAR = auto()
#    FUNCTION_PARAM = auto()

import re

pyton_templates = {
    VarType.LOCAL_VAR:      '(?:\A|;)\s*(\w+)\s*\=',
    VarType.MEMBER_VAR:     '(?:\A|;)\s*self\.([\w]+)\s*\=',
    VarType.CLASS_NAME:     '(?:\A|;)\s*class\s*([\w]+)\s*[:(]',
    VarType.FUNCTION_NAME:  '(?:\A|;)\s*def\s*([\w]+)\s*\(',
    VarType.FOR_VAR:        '(?:\A|;)\s*for\s*([\w]+)\s*in',
#    VarType.FUNCTION_PARAM: '(?:\A|;)\s*def\s*[\w]+\s*\( [\s,\w]*\b([\w]+)\b[\s,\w]*\)\s\:',
}

pyton_guard = dir(__builtins__)
pyton_guard += ["__init__", "items"]

html_guard_s = "checked n t h1 h2 h3 h4 h5 h6 h7 h8 br html head body title bgcolor text link vlink alink pre h1 h6 b i tt cite em font size color a href img src name align p blockquote dl dt dd li div border hr table tr td th cellspacing width valign colspan rowspan frameset rows  cols frame noframes  marginwidth marginheight scrolling noresize select multiple option textarea input checkbox radio value submit reset image"
html_guard = html_guard_s.split()

start_guard = "#start_guard"
stop_guard = "#stop_guard"

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
    text4 = "\t   for  id3 in dfd :"

    matches_var = PythonFind(VarType.LOCAL_VAR, text)
    matches_class_var = PythonFind(VarType.MEMBER_VAR, text)
    matches_func = PythonFind(VarType.FUNCTION_NAME, text1)
    matches_class1 = PythonFind(VarType.CLASS_NAME, text2)
    matches_class2 = PythonFind(VarType.CLASS_NAME, text3)
    matches_for = PythonFind(VarType.FOR_VAR, text4)
 #   matches_param = PythonFind(VarType.FUNCTION_PARAM, text1)

    matches_all = PythonFindAll(text + text1 + text2)

    assert isEqualArray(matches_var, ['x', 'yD1', 'a3']), matches_var
    assert isEqualArray(matches_class_var, ['d31'])
    assert isEqualArray(matches_func, ['Test1'])
    assert isEqualArray(matches_class1, ['Test2'])
    assert isEqualArray(matches_class2, ['Test3'])
    assert isEqualArray(matches_for, ['id3'])
 #   assert isEqualArray(matches_param, ['sdfd']), matches_param
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

class Guard:
    def __init__(self):
        self.guard_level = 0;

    def Update(self, cur_str):
        if cur_str.find(start_guard) != -1:
            self.guard_level += 1
        elif cur_str.find(stop_guard) != -1:
            self.guard_level -= 1
        return self.guard_level == 0

def Obfuscator(in_file):
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()

    g = Guard()
    matches = []
    for l in lines:
        if g.Update(l):
            matches += PythonFindAll(l)

    matches = list(set(matches) - set(pyton_guard) - set(html_guard))

    new_matches = []
    for m in matches:
        if len(m) > 2:
            new_matches += [m]
    matches = new_matches

    rand_matches = []
    for m in matches:
        rand_matches += [MakeRandomName(16)]

    f = open(in_file+".map.txt", 'wb')
    for i in range(len(matches)):
        l = rand_matches[i] + '=' + matches[i] + "\n"
        f.write(l.encode('utf-8'))
    f.close()

    f = open(in_file+".ob.py", 'wb') #, encoding='utf-8')
    g = Guard()
    for l in lines:
        if g.Update(l):
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


