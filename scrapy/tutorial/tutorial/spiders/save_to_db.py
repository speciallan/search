#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

def save():

    f = open('./product_url.txt', 'r', encoding='utf-8')
    content = f.read()
    lines = content.split('-----')[:-1]

    for line in lines:
        t = line.split('---')
        print(t)
        exit()

if __name__ == '__main__':

    save()