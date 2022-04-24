# checksum  (English version is added into release, see Checksum-EN.exe)  Build for Windows X64 
 
这是一个检测文件夹是否被篡改的工具，可以审核文件夹完整性。实现了MD5DEEP的一部分功能， 但是本工具是用python实现的有图形界面。

# 使用场景
使用场景A:  我有一些资料，分卷压缩成zip，一百个文件 放在www网站或ftp让别人下载，  别人下载的文件是不是我提供的？ 网络传输有没有错误？  我提供一个checksum.pk文件 和这些zip文件放在同一个目录下， 别人下载后就可以验证这些文件的完整性了。  

使用场景B:  我本地硬盘有一些相册或者工程数据，我在云端做了备份或者移动硬盘做了备份。 但是云端或者移动硬盘的访问不太方便，或者速度太慢。所以我能不能定期审核一下本地硬盘这个文件夹，看看有没有哪些文件被误删、病毒篡改、坏道损坏？ 如果发现不合法的修改，我再从云端备份把原始文件找回来。 

使用场景C:  我有一些资料从硬盘拷到优盘拷到另一个电脑上，在传输过程中有没有出错？  

使用场景D:  我有一个移动硬盘摔坏了，使用恢复软件恢复了一些文件出来，但是文件名没有了，目录结构也没有了。 幸好我恢复了一个checksum.pk文件，其中有各个文件的hash码和路径结构。所以可以根据md5码重建文件目录和重命名文件名。  



# 实现方法

第一次打开数据文件夹时，在文件夹下建立一个checksum.pk文件，其中内容是这个文件夹的快照(snapshot)，下次再打开这个文件夹时根据checksum.pk检验该文件夹下的文件哪些不变，哪些被修改、删除。 
使用python tkinter制作的GUI   使用python hashlib的md5函数。 为了提高速度，选择使用MD5或者SHA1算法。

# 下载 \ Download
使用pyinstaller打包的exe ， 在release中下载Checksum.exe使用。   Download from the release.

Checksum.exe中文版的哈希码是 2b40e0abbf20706c4d14797ce68cfe61 

Checksum-EN.exe ' Hash code is 44e00d2b574d577eb425d874c32f01e5

# User Interface : 

[![截图](https://github.com/kongmadai/checksum/blob/main/screenshotA.png)]

[![截图](https://github.com/kongmadai/checksum/blob/main/screenshotB.png)]


[![截图](https://github.com/kongmadai/checksum/blob/main/screenshotC.png)]

[![截图](https://github.com/kongmadai/checksum/blob/main/screenshotD.png)]
