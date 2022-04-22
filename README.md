# checksum
为一个文件夹建立一个快照(snapshot)放在一个checksum.pk文件中，下次打开这个文件夹(不管这个文件夹被挪动或者复制下载到何处)，再根据checksum.pk检验该文件夹下的文件哪些不变，哪些被修改、删除。 为了快速校验文件完整性，采用MD5或者SHA1。 

使用python tkinter制作的GUI   使用python hashlib的md5函数。 

使用pyinstaller打包exe ， 在release中下载Checksum.exe使用。  Checksum.exe的哈希码是 2b40e0abbf20706c4d14797ce68cfe61

[![截图](https://github.com/kongmadai/checksum/blob/main/screenshot1.png)]


[![截图](https://github.com/kongmadai/checksum/blob/main/screenshot2.png)]
