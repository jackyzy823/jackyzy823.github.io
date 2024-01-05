Title: Sublime SVN/SFTP 破解
Date: 2014-04-29 00:05:36
Modified: 2023-07-21 00:00:00
Slug: sublime-svn-sftp-license-crack
Category: tech

注： 本文原来发布在CSDN，但是最近发现文章状态变成了审核未通过，原因是版权问题，于是复制到这边。

注2： 本文发布时间较早(**2014年**)，已经失效。在新版本中用"-"来判断新旧Key，有"-"，则为旧key，**并验证如果不在KEY_FILTER（已知的所有旧Key的Bloom Filter）中就是伪造的Key**。新key用椭圆曲线公私钥的方式验证。目前思路有修改bloom_filter.pyc，修改判断逻辑。

以下为原文：

注：使用一段时间后出现

./sublimesvn/commands.py:4230: UnicodeWarning: Unicode unequal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

这种问题，虽然不会弹出对话框，但是svn界面会显示unregistered，重启sublime后正常，明日早起研究

注：测试环境 Ubuntu14.10 Sublime Text 2 2221

window下将`sys.path.append('~/.config/sublime-text-2/Packages/SVN')`里的路径改成sublime->perferences->browser package所在的路径

`import sys;sys.path.append('~/.config/sublime-text-2/Packages/SVN');config={'email':"your_email_1",'product_key':'test'};from sublimesvn import commands;commands.SvnCommand.setup_elements(config);print commands.SvnCommand.get_prefix()`

email填自己的email，product_key暂时随便填

由于sublimesvn的pyc都是python2.6环境下生成的，所以必须调出sublime的console (Ctrl+`)，将以上代码复制进去 ，而不能用python，ipython之类的

当然如果还在用python2.6的话忽略以上一句

把最后算出来的值作为product_key和email放入svn.sublime-settings即可

算了一个供试用

SVN

email:cracked_by_jackyzy823
product_key:fb1255-184296-6565ae-ac9efd-2c6c30

SFTP

email:cracked_by_jackyzy823

product_key:a69fef-050040-e39de9-b2720f-64a9fc

-------------------------------
但是我用什么email 算出来都是这个值。。。。
更正：因为setup_element 在Svncommand类里有elements时不会覆盖之。。重启一下sublime就好了

-------------------------------

在

SublimeText  -> Preferences -> Package Settings -> SFTP/SVN -> Setting Users

中增加以下内容
{

"email":"your_email",

"product_key":"calced_product_key"

}

完成激活

sftp

在sftp里get_prefix 并没有单独成为一个函数，虽然可以通过svn的get_prefix破解但是稍微有些麻烦，等有空把get_prefix函数研究透彻再更新。

commands.Svncommand.get_prefix 是通过使用decompile++反编译commands.pyc得到的，但是由于可能代码做了混淆，所以这段代码反编译不是十分清晰。

-----------

sftp代替方案
```Python
def calc_key_sftp(email):
    elements=[email,'sftp_flags','ssh_key_file','psftp'];
    key=elements[0];
    for e in elements:
        key=hmac.new(e.encode('utf-8'),key).digest();
    return key;
```

将email输入函数 将输出值代替以下代码的calc_key_sftp("email") 就可以算出sftp的product_key

注：需安装有sublime svn

`import sys;sys.path.append('~/.config/sublime-text-2/Packages/SVN');from sublimesvn import commands;commands.SvnCommand.elements=[0,calc_key_sftp(''email')];print commands.SvnCommand.get_prefix()`

与此同时 

svn也有同样的不讨好方法

```Python
def calc_key_svn(email):
    elements=[email,'status','checkout','diff'];
    key=elements[0]
    for e in elements:
        key=hmac.new(e.encode('utf-8'),key).digest();
    return key;
```

注释同sftp

`import sys;sys.path.append('~/.config/sublime-text-2/Packages/SVN');from sublimesvn import commands;commands.SvnCommand.elements=[0,calc_key_svn(''email')];print commands.SvnCommand.get_prefix()`

----------------------------------

更新：

将cal函数 lambda 化

svn

`import sys,hmac;sys.path.append('~/.config/sublime-text-2/Packages/SVN');from sublimesvn import commands;calc_key_svn=lambda x: hmac.new("diff",hmac.new("checkout",hmac.new("status",hmac.new(x,x).digest()).digest()).digest()).digest();commands.SvnCommand.elements=[0,calc_key_svn("your_email")];print commands.SvnCommand.get_prefix()`

sftp(需在svn存在情况下)

`import sys,hmac;sys.path.append('~/.config/sublime-text-2/Packages/SVN');from sublimesvn import commands;calc_key_sftp=lambda x: hmac.new("psftp",hmac.new("ssh_key_file",hmac.new("sftp_flags",hmac.new(x,x).digest()).digest()).digest()).digest();commands.SvnCommand.elements=[0,calc_key_sftp("your_email")];print commands.SvnCommand.get_prefix()`

​