#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import re
from fuzzywuzzy import fuzz


def get_block(file_path, n):  # 获取行号所在的函数体{ }号
    start = -1
    stop = -1
    stack = []
    label = True
    file = open(file_path, encoding='utf-8')
    file_list = file.readlines()
    # print('nn',n)
    file_list_num = list(enumerate(file_list))
    for h, sentence in file_list_num[n - 1::-1]:
        sentence = sentence.strip()
        if sentence == '':
            continue
        if sentence[0] == '/':
            continue
        if sentence[0] == '*':
            continue

        if 'function' in sentence:
            if '{' in sentence:
                start = h
                break
            else:
                for g, sentence in file_list_num[h:]:
                    if '{' in sentence:
                        start = g
                        break
                else:
                    continue
                break
        if 'contract' in sentence:
            if '{' in sentence:
                start = h
                break
            else:
                for g, sentence in file_list_num[h:]:
                    if '{' in sentence:
                        start = g
                        break
                else:
                    continue
                break
    for i, sentence in file_list_num[start:]:
        # if

        if '{' in sentence:
            stack.append((i, '{'))
            # print(sentence)
        if '}' in sentence and stack != []:
            stack.pop()
            # print(sentence)
        if stack == []:
            stop = i
            break
        else:
            continue
    return start, stop


# 输入源文件路径名，替换的字符串，行号，新文件名
def copyfile(sourcepath, ss, ln, i, targetpath):
    # if not os.path.exists('./test/repair10/mutation2'):
    #     os.makedirs('./test/repair10/mutation2/')
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
    f = open(sourcepath, 'r+')

    flist = f.readlines()
    line = flist[ln]
    cmindex = line.find(r'//')
    if cmindex != -1:
        line = line[0:cmindex]

    print(line.strip(), ss.strip(), fuzz.ratio(line.strip(), ss.strip()))
    if fuzz.ratio(line.strip(), ss.strip()) >= 94:
        return

    lnnum = ln + 1
    flist[ln] = ss + f'//Mutation Here for <{lnnum}>' + '\n'
    (filepath, tempfilename) = os.path.split(sourcepath)
    (filename, extension) = os.path.splitext(tempfilename)
    ln += 1
    if 'int(' in ss or 'int8(' in ss or 'int16(' in ss or 'int32(' in ss or 'int64(' in ss or 'int128(' in ss or 'int256(' in ss:
        newp = targetpath + '/' + filename + '_mutation_for_inttruncate_' + str(ln) + '_' + str(
            i) + extension
    else:
        newp = targetpath + '/' + filename + '_mutation_for_uinttruncate_' + str(ln) + '_' + str(
            i) + extension
    # print(newp)
    f = open(newp, 'w+')
    f.writelines(flist)
    # print('ff', f.name)


def change(list, mg1, mg2):
    if ('uint', mg2) in list:
        s1 = 'uint128(' + mg2 + ')'
        return mg1 + s1
    if ('uint256', mg2) in list:
        s1 = 'uint128(' + mg2 + ')'
        return mg1 + s1
    if ('uint128', mg2) in list:
        s1 = 'uint64(' + mg2 + ')'
        return mg1 + s1
    if ('uint64', mg2) in list:
        s1 = 'uint32(' + mg2 + ')'
        return mg1 + s1
    if ('uint32', mg2) in list:
        s1 = 'uint16(' + mg2 + ')'
        return mg1 + s1
    if ('uint16', mg2) in list:
        s1 = 'uint8(' + mg2 + ')'
        return mg1 + s1

    if ('int16', mg2) in list:
        s1 = 'int8(' + mg2 + ')'
        return mg1 + s1
    if ('int32', mg2) in list:
        s1 = 'int16(' + mg2 + ')'
        return mg1 + s1
    if ('int64', mg2) in list:
        s1 = 'int32(' + mg2 + ')'
        return mg1 + s1
    if ('int128', mg2) in list:
        s1 = 'int64(' + mg2 + ')'
        return mg1 + s1
    if ('int256', mg2) in list:
        s1 = 'int128(' + mg2 + ')'
        return mg1 + s1
    if ('int', mg2) in list:
        s1 = 'int128(' + mg2 + ')'
        return mg1 + s1
    return mg1 + mg2


def up(ss, list):
    # 匹配运算符和变量
    pattern = re.compile(r'([+-/*%=])\s*([a-zA-Z_][a-zA-Z\d_]*)')
    pattern2 = re.compile(r'(\+=|-=|/=|\*=|%=)\s*([a-zA-Z_][a-zA-Z\d_]*)')
    if len(re.findall(pattern2, ss)) != 0:
        return True
    if len(re.findall(pattern, ss)) <= 1:
        return False
    return True

    # if len(re.findall(pattern, ss)) == 0:
    #     return ss
    # newss = re.sub(pattern, lambda x: change(list, x.group(1), x.group(2)), ss)
    # # print('up', list, newss)
    # return newss


def pdmutation(fn, en, spath, list, tpath):
    file = open(spath)

    linenum = 0;
    pattern1 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (\w+)')
    pattern2 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (public|internal|private) (\w+)')
    pattern3 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (\w+)')
    pattern4 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (public|internal|private) (\w+)')
    # pattern3 = re.compile(r'([a-zA-Z\$_][a-zA-Z\d_]*)\s*([+-/*=])\s*([a-zA-Z\$_][a-zA-Z\d_]*)')

    listpa = list
    for line in file:
        cmindex = line.find(r'//')
        if cmindex != -1:
            line = line[0:cmindex]
        if linenum in range(fn, en + 1):
            # 匹配uint和int
            ret1 = re.findall(pattern1, line.strip())
            ret2 = re.findall(pattern2, line.strip())
            ret3 = re.findall(pattern3, line.strip())
            ret4 = re.findall(pattern4, line.strip())
            listpa += ret1
            listpa += fromthreegettwo(ret2)
            listpa += ret3
            listpa += fromthreegettwo(ret4)
            # 如果是在范围内行就进行判断截取

            if line.strip().find('function') != -1:
                fn1, en1 = get_block(spath, linenum + 1)
                # print(fn1, en1)
                pdmutation2(fn1, en1, spath, listpa, tpath)
            #     获取新的字符串如果不是赋值语句
            patternf = re.compile(r'(if\s+)|(if\()|(while\s+)|(while\()')
            if re.search(patternf, line) != None:
                linenum += 1
                continue
            stringbool = up(line, listpa)
            if stringbool:
                everymutation(spath, line.strip(), listpa, linenum, tpath)
        linenum += 1


def pdmutation2(fn, en, spath, list, tpath):
    file = open(spath)

    linenum = 0;
    pattern1 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (\w+)')
    pattern2 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (public|internal|private) (\w+)')
    pattern3 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (\w+)')
    pattern4 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (public|internal|private) (\w+)')
    listpa = list
    for line in file:
        cmindex = line.find(r'//')
        if cmindex != -1:
            line = line[0:cmindex]
        # 如果是在范围内行就进行判断截取
        if linenum in range(fn, en + 1):
            # 匹配uint和int
            ret1 = re.findall(pattern1, line.strip())
            ret2 = re.findall(pattern2, line.strip())
            ret3 = re.findall(pattern3, line.strip())
            ret4 = re.findall(pattern4, line.strip())
            listpa += ret1
            listpa += fromthreegettwo(ret2)
            listpa += ret3
            listpa += fromthreegettwo(ret4)
            # continue
            #     获取新的字符串
            #     获取新的字符串如果不是赋值语句
            patternf = re.compile(r'(if\s+)|(if\()|(while\s+)|(while\()')
            if re.search(patternf, line) != None:
                linenum += 1
                continue
            stringbool = up(line, listpa)
            if stringbool:
                everymutation(spath, line.strip(), listpa, linenum, tpath)
        linenum += 1


def everymutation(spath, old, list, linenum, tpath):
    pattern = re.compile(r'([+-/*=])\s*([a-zA-Z_][a-zA-Z\d_]*)')
    pattern2 = re.compile(r'(\+=|-=|/=|\*=|%=)\s*([a-zA-Z_][a-zA-Z\d_]*)')
    mm2 = re.search(pattern2, old)
    if mm2 != None:
        # print(f'change前的{list}')
        strr = change(list, mm2.group(1), mm2.group(2))
        s, e = mm2.span()
        strr2 = old.replace(old[s:e], strr, 1)
        copyfile(spath, strr2.strip(), linenum, 0, tpath)
        return
    match = re.search(pattern, old)
    i = 0
    for m in re.finditer(pattern, old):
        strr = change(list, m.group(1), m.group(2))
        s, e = m.span()
        strr2 = old.replace(old[s:e], strr, 1)
        copyfile(spath, strr2.strip(), linenum, i, tpath)
        i += 1


def fromthreegettwo(list):
    newlist = []
    for x, y, z in list:
        newlist.append((x, z))
    return newlist


def p(spath, tpath):
    file = open(spath)
    lnum = 0
    listpa = []
    pattern1 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (\w+)')
    pattern2 = re.compile(r'(^int256|^int64|^int32|^int8|^int) (public|internal|private) (\w+)')
    pattern3 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (\w+)')
    pattern4 = re.compile(r'(uint256|uint64|uint32|uint16|uint8|uint) (public|internal|private) (\w+)')
    for line in file:
        ret1 = re.findall(pattern1, line.strip())
        ret2 = re.findall(pattern2, line.strip())
        ret3 = re.findall(pattern3, line.strip())
        ret4 = re.findall(pattern4, line.strip())
        listpa += ret1
        listpa += fromthreegettwo(ret2)
        listpa += ret3
        listpa += fromthreegettwo(ret4)
        if line.strip().find("contract") != -1:
            fn, en = get_block(spath, lnum + 1)
            pdmutation(fn, en, spath, listpa, tpath)
            # print(line.strip())
        lnum += 1

# p('test/AI_repair.sol')
