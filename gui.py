# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 01:04:18 2022

@author: YS
"""

import multiprocessing
import threading

import time
import os
import sys   

codepath = os.getcwd()
if codepath not in sys.path: sys.path.append(codepath)

#import tkinter as tk # exe = 7.5MB

from tkinter import Tk

from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import IntVar
from tkinter import Checkbutton

from tkinter import WORD

from tkinter import ttk
from tkinter import scrolledtext # 导入滚动文本框的模块  


from tkinter.filedialog import askdirectory

from strings import right20cn_round 

from picklefile import PickleFile
from findfiles import findfile_onelevel, findfile
from md5 import generate_file_md5, generate_file_sha1


def isset(v): 
    '''isset('xyz') check if xyz variable exists
    '''
    try :       type(eval(v))
    except :    return 0
    else :      return 1
    #finally:    pass

class MatStruct(object):
    """ like Matlab struct.
    类似Matlab的结构体.
    """
    pass

class DataFolder(object):
    """
    目标文件夹的对象
    """
    def __init__(self, path, includemode=1, encodemode='MD5'):
        """
         
        """
        self.path = path
        self.checksumfile = os.path.join(self.path, 'checksum.pk') 
        self.checksum = MatStruct()
        self.includemode = includemode
        self.encodemode = encodemode
        self.log = []
        
        #初始化  如果不存在路径  mkdir
        try:
            if not os.path.exists(self.path):  
                os.mkdir(self.path)
                print('make new dir : ' + self.path)
                self.log.append('make new dir : ' + self.path)
        except Exception as e :
            errormsg = 'DataFolder.__init__()except1: '+ str(e)
            print (errormsg)
            self.log.append(errormsg)
        
        #初始化  如果不存在文件 建立文件    如果存在文件那么读取文件到checksum_.pk    
        checksumfile_ = PickleFile(self.checksumfile)
        
        self.checksum = checksumfile_.pk
        
        if self.checksum == 1:
            errormsg = "checksum.pk doesn't exist , a new file is created"
            self.log.append(errormsg)

    def run_checksum(self, dump_option = 'yes'):
        '''

        Returns
        -------
        None.

        '''
        checksumdict = MatStruct()
        if self.encodemode == 'MD5':
            checksumdict.method = 'md5'
        elif self.encodemode == 'SHA1':
            checksumdict.method = 'sha1'
        else:
            return ''
        if self.includemode == 2:
            checksumdict.includesub = 'included'
            filelist_ = findfile(self.path, '*')
        elif self.includemode == 1:
            checksumdict.includesub = 'excluded'
            filelist_ = findfile_onelevel(self.path, '*')
        else:
            return ''
        
        checksumdict.rootpath = self.path
        checksumdict.reportdate = time.strftime(
                                '%Y-%m-%d [%H:%M:%S]',  time.localtime())
        
        filelist = []
        for i in filelist_:
            if 'checksum.pk' in os.path.split(i)[1]:
                pass
            elif 'checksum_pk.temp' in os.path.split(i)[1]:
                pass
            else:
                filelist.append(i)        
                
        checksumdict.version = '1'
        checksumdict.database = {}
        
        for i in filelist:
            
            if isset('NOWMSGBOX'): 
                NOWMSGBOX.set( right20cn_round('Reading:'+ i,88) )
            
            if checksumdict.method == 'md5':
                value = generate_file_md5(i)
            elif checksumdict.method == 'sha1':
                value = generate_file_sha1(i)
            else:
                return ''
            
            checksumdict.database[i.replace(self.path,'')] = value
            
        self.checksum = checksumdict

        if dump_option == 'yes':
            checksumfile_ = PickleFile(self.checksumfile)
            checksumfile_.save_pk(checksumdict)
            errormsg = "checksum data is saved to checksum.pk "
            self.log.append(errormsg)
        
        # if isset('NOWMSGBOX'): 
        #     NOWMSGBOX.set('第一次运行，成功新建checksum.pk文件保存校验码。'[-88:])
        
        return checksumdict

         
    def build_checksum(self,):
        return self.run_checksum( dump_option = 'yes' )

    def build_checksum_again(self,):
        return self.run_checksum( dump_option = 'no' )


def UI():   
    
    def fix_path(path_):
        path_ = path_.replace('/','\\')
        # path_ = os.path.split(path_)[0]
        if path_[-2:] == '\\':
            path_ = path[:-2]
        return path_

    def Messageboxdisplay(string):
        if isset('NOWMSGBOX'):
            NOWMSGBOX.set(string[:88])
            
    def Scrolleddisplay(string):
        box_info =[]
        box_info.append(string)
        box_info_jn = '\n'.join(box_info)
        component_box.delete(1.0, 'end')
        component_box.insert("insert", box_info_jn)

    def analyze(input_):
        
        component_action1.grid_forget()
        
        Scrolleddisplay('处理中。。。 稍等一会')
        
        path = input_[0]
        includemode = input_[1]
        encodemode = input_[2]
        
        datafolder = DataFolder(path, includemode, encodemode)
        checksum = datafolder.checksum
        
        if checksum == 1:  # if checksum.pk file is new created 
            datafolder.build_checksum() # generate a real database for 1st time
            checksum = datafolder.checksum
            
            Scrolleddisplay('为'+str(len(checksum.database))+
                            '个文件创建了一个新的记录文件在checksum.pk中。')
            
            Messageboxdisplay('第一次运行，成功新建checksum.pk文件保存校验码。')
            
            component_action1.grid(row = 2, column = 0, columnspan=4)
            return checksum
        
        elif checksum == '':  # if checksum.pk file is broken 
        
            Scrolleddisplay('找到checksum.pk校验文件，但是文件已经损坏,所以不能分析。')
               
            Messageboxdisplay('找到checksum.pk校验文件，但是文件已经损坏')
            
            component_action1.grid(row = 2, column = 0, columnspan=4)    
            return checksum
        
        else: # if checksum is read successfully 
        
            try:
            
                if checksum.includesub == 'included':
                    includemode = 2
                elif checksum.includesub == 'excluded':
                    includemode = 1
                else:
                    Scrolleddisplay('找到checksum.pk校验文件，但是文件已经损坏,所以不能分析。')
                    Messageboxdisplay('找到checksum.pk校验文件，但是文件已经损坏')
                    return checksum
                
                if checksum.method == 'md5':
                    encodemode = 'MD5'
                elif checksum.method == 'sha1':
                    encodemode = 'SHA1'
                else:
                    Scrolleddisplay('找到checksum.pk校验文件，但是文件已经损坏,所以不能分析。')
                    Messageboxdisplay('找到checksum.pk校验文件，但是文件已经损坏')
                    component_action1.grid(row = 2, column = 0, columnspan=4)
                    return checksum
                
                lastreportdate = checksum.reportdate
                
            except Exception as e :
                errormsg = 'analyze()except1: '+ str(e)
                print (errormsg)
                
                Scrolleddisplay('找到checksum.pk校验文件，但是文件已经损坏,所以不能分析。')
                Messageboxdisplay('找到checksum.pk校验文件，但是文件已经损坏')
                
                component_action1.grid(row = 2, column = 0, columnspan=4)
                return checksum
                
                
            
            datafolder_again = DataFolder(path, includemode, encodemode)
            datafolder_again.build_checksum_again()
            checksum_again = datafolder_again.checksum
            
            filelist_unchanged =[]
            filelist_updated = []
            filelist_added = []
            filelist_removed = []
            for fi in checksum_again.database:
                if fi not in checksum.database:
                    filelist_added.append(path + fi)
            for fi in checksum.database:
                if fi not in checksum_again.database:
                    filelist_removed.append(path + fi)
            for fi in checksum_again.database:
                if fi in checksum.database:
                    if checksum_again.database[fi] == checksum.database[fi]:
                        filelist_unchanged.append(path + fi)
                    else:
                        filelist_updated.append(path + fi)
                    
            box_info =[]
            box_info.append('上次的状态文件的日期是 ' + lastreportdate + 
                            ' 与上次状态相比 :')
            if len(filelist_added) > 0:
                box_info.append('-'*60)
                box_info.append('下列 ' + str(len(filelist_added)) + 
                                ' 个文件是新增的：')
                for fi in filelist_added:
                    box_info.append(fi)
            
            if len(filelist_removed) > 0:
                box_info.append('-'*60)
                box_info.append('下列 ' + str(len(filelist_removed)) + 
                                ' 个文件是被删除的：')
                for fi in filelist_removed:
                    box_info.append(fi)
            
            if len(filelist_updated) > 0:
                box_info.append('-'*60)
                box_info.append('下列 ' + str(len(filelist_updated)) + 
                                ' 个文件是被修改过的：')
                for fi in filelist_updated:
                    box_info.append(fi)
                    
            if len(filelist_added) + len(filelist_removed) + len(filelist_updated) > 0:
                
                component_action2.grid(row = 2, column = 4, columnspan=4)
                checksumfiledump = os.path.join(codepath, 'checksum_pk.temp')  
                checksumfiledump_ = PickleFile(checksumfiledump)
                checksumfiledump_.save_pk(checksum_again)
                
            else:
                component_action2.grid_forget()
                
            if len(filelist_unchanged) > 0:
                box_info.append('-'*60)
                box_info.append('      ' + str(len(filelist_unchanged)) + 
                                ' 个文件没有改变')

            box_info_jn = '\n'.join(box_info)
            component_box.delete(1.0, 'end')
            component_box.insert("insert", box_info_jn)
        
            Messageboxdisplay('分析完成，找到以下差异，请检阅：')
                
            component_action1.grid(row = 2, column = 0, columnspan=4)    
            return checksum
            
        
        
    def acceptchanges():
        checksumfiledump = os.path.join(codepath, 'checksum_pk.temp')  
        checksumfiledump_ = PickleFile(checksumfiledump)
        checksum_again = checksumfiledump_.pk
        path_ = fix_path( path.get() )
        checksumfile = os.path.join(path_, 'checksum.pk')  
        checksumfile_ = PickleFile(checksumfile)
        checksumfile_.save_pk(checksum_again)

        component_action2.grid_forget()
        
        
        Scrolleddisplay('  Done')
        Messageboxdisplay('checksum.pk文件已经被最新的状态覆盖。')
        
        
    def UIselectPath():
        path_ = askdirectory()
        path.set(path_)
        
    def runchecksum():
        path_ = fix_path( path.get() )
        includemode_ = includemode.get()  #  2 include   or  1 exclude 
        encodemode_ = encodemode.get() # 'MD5' or 'SHA1'
        input_ = (path_, includemode_, encodemode_)
        # analyze(input_)
        # 使用threading 避免界面卡死 
        t = threading.Thread(target = analyze,  args=(input_,)  )
        t.start()
        
    
    root = Tk()
    root.geometry('626x398+400+20')
    root.title('Checksum程序 YSun 20220420') 
    # root.iconbitmap(r'colors.ico')
    
    global NOWMSGBOX
    NOWMSGBOX = StringVar()
    path = StringVar()
    includemode = IntVar(value=1)
    encodemode = StringVar()
       
    component_msgbox = Label(root,textvariable = NOWMSGBOX)
    component_msgbox.grid(row = 1, column = 0, columnspan = 8)
    NOWMSGBOX.set('请在上方选择目标路径')
    
    preposition = StringVar()
    preposition.set('甲乙丙丁戊己') # 相当于汉字6.5*8 = 52个 或者a * 88个 占位符
    component_preposition1 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition2 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition3 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition4 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition5 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition6 = Label(root,textvariable= preposition, fg= 'white') 
    component_preposition7 = Label(root,textvariable= preposition, fg= 'white')
    component_preposition8 = Label(root,textvariable= preposition, fg= 'white')  
    component_preposition1.grid(row=3, column=0, columnspan=1, padx=0, ipadx=0)
    component_preposition2.grid(row=3, column=1, columnspan=1, padx=0, ipadx=0)
    component_preposition3.grid(row=3, column=2, columnspan=1, padx=0, ipadx=0)
    component_preposition4.grid(row=3, column=3, columnspan=1, padx=0, ipadx=0)
    component_preposition5.grid(row=3, column=4, columnspan=1, padx=0, ipadx=0)
    component_preposition6.grid(row=3, column=5, columnspan=1, padx=0, ipadx=0)
    component_preposition7.grid(row=3, column=6, columnspan=1, padx=0, ipadx=0)
    component_preposition8.grid(row=3, column=7, columnspan=1, padx=0, ipadx=0)
    
    
    component_input1 = Label(root, text = "目标路径:")
    component_input1.grid(row = 0, column = 0) 
    
    component_input2 = Entry(root, textvariable = path, width=66)
    component_input2.grid(row=0, column=1, columnspan=6 , padx=0, sticky= 'W')


    component_input3 = Button(root, text = "或选择路径", command = UIselectPath)
    component_input3.grid(row = 0, column = 7)


    component_action1a = Label(root, text = " ")
    component_action1a.grid(row = 2, column = 0, pady = 10) 

    component_action1 = Button(root, 
                       text = "           点我开始分析该文件夹         ", 
                       command = runchecksum)
    component_action1.grid(row = 2, column = 0, columnspan=4)
    
    component_action2 = Button(root, 
           text = "已阅差异，将最新状态写入checksum.pk文件", 
           command = acceptchanges)
    component_action2.grid(row = 2, column = 4, columnspan=4)
    component_action2.grid_forget()
    
    
    component_input4a = Label(root, text = "如果创建新的状态文件,创建时 包括子目录的文件吗?")
    component_input4a.grid(row = 4, column = 0, columnspan=4, pady = 8) 
    
    component_input4 = Checkbutton(root, text = "是的", 
                       variable = includemode, onvalue = 2, offvalue = 1)
    component_input4.grid(row=4, column=4, columnspan=1 , padx=0, sticky= 'W')
    
    component_input5a = Label(root, text = "选择哈希算法")
    component_input5a.grid(row = 4, column = 6, columnspan=1) 
    
    component_input5 = ttk.Combobox(root, width=7 , height = 34, 
            textvariable=encodemode, values='MD5 SHA1' ,state='readonly')  
    component_input5.grid(row = 4, column = 7, columnspan = 1,padx = 2,sticky='w')

    component_input5.current(0)
    #component_input5.bind("<<ComboboxSelected>>", resety)  
    
    component_box = scrolledtext.ScrolledText(root, width=85, height=20, wrap=WORD, padx = 3)     

    component_box.grid(row = 3, column = 0, columnspan=8)   

    usertip = '''\
             
                        【使用说明】

  状态文件 (checksum.pk)       相当于一个存放文件hash校验码的数据库  
              或者说相当于为这个文件夹制作了一个BT种子存放这些文件的状态的快照


  选择一个文件夹，点分析按钮。


  如果文件夹下面没有checksum.pk文件，那么会新建一个checksum.pk文件。


  如果文件夹下面已经有checksum.pk文件，那么会根据该数据检查各个文件有没有变动。


  checksum.pk如果损坏，可以手工删之，然后重建。
    '''
    component_box.insert("insert",  usertip)  
    
    
    root.mainloop() 


if __name__=='__main__':
    
    """
    freeze_support解决打包GUI卡住的问题 见 
    https://blog.csdn.net/qq842977873/article/details/82505578 
    https://blog.csdn.net/zyc121561/article/details/82941056 
    """
    multiprocessing.freeze_support()
    
    UI()

    
'''
 打包 pip install pyinstaller    see https://blog.csdn.net/zt_xcyk/article/details/73786659
 pyinstaller -F -w -i colors.ico gui.py 
 pyinstaller -F -i xxx.ico gui.py 
 
 
 pyinstaller -F -w -i tool.ico gui.py 
    
'''
    
    
    
    