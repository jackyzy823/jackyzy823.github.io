Title: QMailAgent架构分析及破解
Date: 2022-06-20 14:32
Slug: qmailagent-analysis-and-crack
Tags: QMailAgent,crack,analysis,破解
Category: tech

注: 本次破解仅在QMailAgent 3.1.1下测试通过，不对未来版本做保证。

## 起因

受够了Gmail网页版的内存占用及其他一系列的心理障碍，迫切需要一个自建的支持一个登陆帐号内包含多个不同提供商(Gmail,Outlook等)的邮箱帐号的多平台（至少Web和安卓）聚合邮件系统(mail aggregator)。然而找了一圈市面上的解决方案都不符合我的心意。

Roundcube不支持多帐号，安卓上也没有客户端。NextCloud Mail虽然不错，可惜我没有NextCloud生态。也看过SOGOs和Horde都不太符合心意。

还有就是 QMailAgent 主要是因为家里有NAS且有安卓客户端，在有公网IP的情况下，安卓端的作用可以最大化。但是由于我想收Gmail,然而此地受限网络环境不允许。

我甚至动了自己写的心，包括但不限于修改NextCloud Mail或QMailAgent使其独立于其平台，但是开发安卓客户端实在是太麻烦了。最终还是妥协了，选择了QMailAgent，使用透明代理改造了本地的网络，使之能访问GMail。

## 经过
在尝试魔改QMailAgent的时候，对其进行了逆向工程，分析了其架构，并破解了Premium的限制。

- 代码分析

通过下载[QPKG包](https://download.qnap.com.cn/QPKG/qmailagent_3.1.1_20220524_x86_64.zip)并使用[工具](https://github.com/max-boehm/qnap-utils) 解包，其中的Python字节码(\*.pyc) 可以通过uncompyle6来反编译。

纵览代码可以发现QMailAgent整体上是由RoundCube 1.1.2加上自己写的Plugins（包括多帐号，备份还原，与FileStation交互等功能）在加上部分用于处理IMAP和POP3的Python库组成，例如 offlineimap ，例如使用Got-your-back 0.21 (非常老旧的版本)来支持GMail的获取。

- Premium破解

接下来就是Premium破解，不建议从license文件本身入手，因为我有过失败的尝试经历，除非一辈子不联网，否则QNAP是强制网络验证license的，比较难搞。

通过前端的入口 `_task=license&_action=get_info` 找到 `data/web/plugins/license/license.php` 中的 `$this->register_action('get_info', array($this, 'get_info_ajax'));`,进而找到`get_info_ajax` 函数，这里发现其调用了一个明显混淆过的函数`$info = $this->rcmail->license->wbf2d66a297();`，找到其定义的php文件`data/web/program/lib/Qmail/obfuscator/qmail_license.php`，显然obfuscator文件夹下的php文件都进行过混淆以保护代码，虽然可以手动恢复，但为了以后方便还是写了一个脚本自动反混淆，再用格式美化工具格式化一下就可以轻松阅读，甚至能够运行，至少直接`php xx.php`不会报错。

通过搜索所有包含`qmail_license.php`中的类名及`->license`的代码，发现所有付费功能在调用前都没有验证license，这也可以从`data/web/plugins/license/license.min.js`前端代码中进一步得到验证，又是可爱的前端验证，详见[之前的文章]({filename}/tech/bad-geolocation-restriction-implements.md)。这和QSirch、CAIYIN MediaSign之类的有所不同，它们都是在后端二进制文件中验证license的，相比而言防御等级更胜一筹。

所以可以通过Console控制台(F12)或者油猴等方式，每次运行时绕过前端的验证。也可以在代码前面加上`javascript:`后[存入书签](https://stackoverflow.com/questions/18872679/function-as-google-chrome-bookmark)，放在书签栏上。因为用到Premium功能的频率不高，我觉得通过Console控制台(F12)修改是可以接受的。

QNAP通过iframe的形式整合QMailAgent及其他应用，QMailAgent 的 iframe的id为 ext-gen+随机数+qmail ，因此可以通过css属性来找到这个iframe，详细javscript如下，伪造了一个到2099-12-31到期的license:
```javascript
document.querySelectorAll('[id^=ext-gen][id$=qmail]').forEach( k => {
  k.contentWindow.rcmail.license.stop_refresh();
  k.contentWindow.rcmail.license.update({"info": {"license": [{"status": "valid", "id": "Default", "name": "Default", "info": {"valid_from": "", "valid_until": "", "apply_date": "", "enable_func": {"add_account": {"limit": -1 } }, "expired_soon": false } }, {"status": "valid", "id": "Test", "name": "Test", "info": {"valid_from": "2020-01-01", "valid_until": "2099-12-31", "apply_date": "2020-01-01", "enable_func": {"add_account":{"limit": -1 }, "backup" :{}, "restore":{}, "merge":{}, }, "expired_soon": false } } ], "merge_func": {"add_account": {"limit": -1, "valid_from": "", "valid_until": "", "apply_date": "", "expired_soon": false }, "backup" :{}, "restore":{}, "merge":{}, } }, "is_premium": true, "unlimit": -1 })
} )
```

如果是直接以`http://NAS/qmail`形式访问QMailAgent则可以简化为：

```javascript
rcmail.license.stop_refresh()
rcmail.license.update({"info": {"license": [{"status": "valid", "id": "Default", "name": "Default", "info": {"valid_from": "", "valid_until": "", "apply_date": "", "enable_func": {"add_account": {"limit": -1 } }, "expired_soon": false } }, {"status": "valid", "id": "Test", "name": "Test", "info": {"valid_from": "2020-01-01", "valid_until": "2099-12-31", "apply_date": "2020-01-01", "enable_func": {"add_account":{"limit": -1 }, "backup" :{}, "restore":{}, "merge":{}, }, "expired_soon": false } } ], "merge_func": {"add_account": {"limit": -1, "valid_from": "", "valid_until": "", "apply_date": "", "expired_soon": false }, "backup" :{}, "restore":{}, "merge":{}, } }, "is_premium": true, "unlimit": -1 })
```

因为所有付费功能在调用前都没有验证license，所以如果能SSH连进NAS的话可以直接调用`/mnt/ext/opt/qmail/web/restoreworker.sh`和`/mnt/ext/opt/qmail/web/backupworker.sh`等工具。

甚至可以更加直接一点，通过mysqldump命令备份数据库，并手动备份邮件存储的文件夹。需要恢复的时候，再导入即可。 其中mysql数据库的连接方式为  `/usr/local/mariadb/bin/mysql -uroundcube -pmypassword  -S /mnt/ext/opt/qmail/var/qmail_mysqld.sock`

- 使用透明代理改造本地网络

改造本地网络前提是gmail、google accounts和googleapis域名没有被污染， 如果污染了就要另外增加自建DNS的步骤。google本身的主域名被污染无所谓。

我们要做的就是让所有google的IP经过我们的透明代理，那么Google的IP哪里查呢？像这些大厂都会公布自己的IP段，供运维人员配置防火墙等等，可以从`https://www.gstatic.com/iprange/goog.json`获取所有的IP段，令人惊奇的是www域名（指向了国内的IP，北京谷歌云）没被墙，而裸域名被墙了。

使用SSH连接NAS，首先 `sudo ipset create google hash:net family inet` 建立google的IP集合。然后 `curl https://www.gstatic.com/ipranges/goog.json |  jq -r ".prefixes[].ipv4Prefix | values"  | xargs -n 1 sudo ipset add google` 将Google的IP加入集合中(这里我们暂时不考虑ipv6)。接下来建立iptables的转发规则将命中Google IP的流量转发到透明代理，其他流量原样处理(这里我们暂时只考虑TCP协议)。

```
sudo iptables -t nat -N google
sudo iptables -t nat -A google -m set ! --match-set google dst -j RETURN
sudo iptables -t nat -A google -p tcp -j REDIRECT --to-ports 2080
sudo iptables -t nat -A PREROUTING -j google
sudo iptables -t nat -A OUTPUT -p tcp  -j google
``` 

最后，使用QNAP的Container Station创建透明代理的container。这里需要注意的是container的网络模式必须为host模式，这样透明代理程序才能通过iptables知道修改前的源IP、端口，否则无法转发。你可以使用任何你喜欢的支持透明代理模式的工具。别忘了设置自动启动。

改造完成后别忘了通过开机启动项autorun.sh (Control Panel-\>System-\>Hardware-\>General-\>Run user defined processes during startup) 来持久化操作，因为每次重启后iptables都不会保存。具体内容为之前所有的命令，把sudo去除即可。

## 结果

真香

## One More Thing

最近听闻K-9加入ThunderBird，就在想Thunderbird能不能出个Headless的然后扔在VPS上收邮件，然后本地ThunderBird和安卓端通过WEB API来访问/同步。
或者加入FxA全家桶，利用Firefox Sync来同步设置邮件（可能对对于Mozilla来说负担有些大）。

附： 反混淆用的Python脚本 <del>无内鬼，来点正则表达式笑话。</del>
```python
import re,sys,zlib

if len(sys.argv)!=2:
    print("Usage: deobfs xxx.php")
    exit()


f = open(sys.argv[1],"rb")
s = f.read()
f.close()

## Remove define
s = re.sub(b"define\(.*?\);",b"",s) 

## Extract gz content
res  = re.findall(rb"""(?s)\$(.*?)\[(.*?)\]\s=\sexplode\('(.*?)'\s*,\s*gzinflate\(substr\('(.*?)'\s*,(.*?)\s*,(.*?)\s*\)\)\);""" , s[: s.find(b')));') +4  ] ) 
global_obj , global_key , split_key ,  gz , start , end = res[0]
gz1 = gz[ int(start.decode(),16) : int(end.decode())]

# TODO: https://www.php.net/manual/en/language.types.string.php
## \r \v \e \f
gz1 = gz1.replace(rb"\'" , b"\'").replace(rb'\"' , b'\"').replace(rb'\$' , b'\$').replace(rb'\n' , b'\n').replace(rb'\t' , b'\t').replace(rb'\\' , b'\\') # beacuse php escape it

g = zlib.decompressobj(-zlib.MAX_WBITS).decompress(gz1)
gl = g.split(split_key)

s1 = s[: s.find(b')));') +4  ]
s2 = re.sub(rb"""(?s)\$(.*?)\[(.*?)\]\s=\sexplode\('(.*?)'\s*,\s*gzinflate\(substr\('(.*?)'\s*,(.*?)\s*,(.*?)\s*\)\)\);""" , b"", s1 ) 
s = s.replace(s1,s2)

## Remove `$KEY = &_GLOBAL` and Replace all $KEY to $_GLOBAL
ref_args = re.findall(rb"""\$([^\)]*?)\=\&\$""" +global_obj,s )
ref_args = list(set(ref_args)) #dedupe
ref_args.sort(key=len,reverse=True)

for ref_arg in ref_args:
    s = s.replace(b'$' + ref_arg + b"=&$" + global_obj + b'[' + global_key + b'];', b"")
    s = s.replace(b'$'+ ref_arg + b'[', b'$' + global_obj + b'[' + global_key + b'][' )

## Replace malformed arguments
res = re.findall(rb'''(\$[\W]*?)[\=|\!|,|)|\[|>|\]|\-|\:|\.|\;|\<]''',s)

rep = list(set(res))
rep.sort(key=len,reverse=True)

for i ,v in enumerate(rep):
    s = s.replace(v , b"$arg"+ str(i).encode() )

## Replace dict with its item.
def replace_word(x):
    word =  gl[ int(x.group(1).decode(),16)  ]
    if word in [ b"DateTime" , b"DateTimeZone" , b"restoreworker" , b"backupworker"]:
        return word
    else:
        return b'"' + word + b'"'

s = re.sub(rb'\$' +  global_obj  + b'\['+ global_key + b'\]\[(.*?)\]' , replace_word , s )

## Output
with  open(sys.argv[1]+".dec","wb") as f:
    f.write(s)
```
