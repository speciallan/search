#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import tkinter as tk
import tkinter.font as tkFont

mygui = tk.Tk(className='爬虫进度')
mygui.geometry('800x800+500+100')

mymenu = tk.Menu()
mymenu.add_command(label='open')

label = tk.Label(mygui,
                      text="this is a word",
                      bg="pink", fg="red",
                      font=("宋体", 20),
                      width=800,
                      height=800,
                      wraplength=800,
                      justify="left",
                      anchor="nw")

# 显示出来
# label.pack()

def show():
    print(111)

button1 = tk.Button(mygui, text="按钮", command=show, width=20, height=10)
# button1.pack()

ft = tkFont.Font(family='Courier', size=15)

# for ft in ('Arial', ('Courier New',), ('Comic Sans MS',), 'Fixdsys', ('MS Sans Serif',), ('MS Serif',), 'Symbol', 'System', ('Times New Roman',), 'Verdana'):
#     label = tk.Label(mygui, text='hello sticky', font=ft).grid()
#     label.pack()

text = tk.Text(mygui, width=800, height=800, font=ft)
scroll = tk.Scrollbar()
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text.pack(side=tk.LEFT, fill=tk.Y)

# 关联
# scroll.config(command=test.yview)
text.pack()

str = '''盖闻天地之数，有十二万九千六百岁为一元。将一元分为十二会，乃子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥之十二支也。每会该一万八百岁。且就一日而论：子时得阳气，而丑则鸡鸣；寅不通光，而卯则日出；辰时食后，而巳则挨排；日午天中，而未则西蹉；申时晡而日落酉；戌黄昏而人定亥。譬于大数，若到戌会之终，则天地昏蒙而万物否矣。再去五千四百岁，交亥会之初，则当黑暗，而两间人物俱无矣，故曰混沌。又五千四百岁，亥会将终，贞下起元，近子之会，而复逐渐开明。邵康节曰：“冬至子之半，天心无改移。一阳初动处，万物未生时。”到此，天始有根。再五千四百岁，正当子会，轻清上腾，有日，有月，有星，有辰。日、月、星、辰，谓之四象。故曰，天开于子。又经五千四百岁，子会将终，近丑之会，而逐渐坚实。易曰：“大哉乾元！至哉坤元！万物资生，乃顺承天。”至此，地始凝结。再五千四百岁，正当丑会，重浊下凝，有水，有火，有山，有石，有土。水、火、山、石、土谓之五形。故曰，地辟于丑。又经五千四百岁，丑会终而寅会之初，发生万物。'''

text.insert(tk.INSERT, str)

str = '\n 111111111111'
text.insert(tk.INSERT, str)
text.update()

mygui.config(menu=mymenu)
# mygui.option_add("*Font", "宋体")
tk.mainloop()
