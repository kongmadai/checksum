# checksum
为一个文件夹建立一个快照(snapshot)放在一个checksum.pk文件中，下次打开这个文件夹(不管这个文件夹被挪动或者复制下载到何处)，再根据checksum.pk检验该文件夹下的文件哪些不变，哪些被修改、删除。

使用pyinstaller打包exe ， 在release中下载Checksum.exe
