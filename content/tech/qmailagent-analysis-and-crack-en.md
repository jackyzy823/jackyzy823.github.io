Title: QMailAgent Architecture Analysis and Premium Crack
Date: 2022-06-20 14:32
Slug: qmailagent-analysis-and-crack
Tags: QMailAgent,crack,analysis,破解
Category: tech
Lang: en

Note: Only test under QMailAgent 3.1.1 . No future version guarantee.

Details and comments are in chinese version article.

## Architecture Analysis

QMailAgent is a combination of Roundcube v1.1.2 , some precompiled python libraries which handles IMAP with OAUTH and POP3 protocol like offlineimap, got-you-back 0.21 and its own Roundcube plugins which implement features like multi-mailaccounts, backup & restore and interaction with QNAP FileStation.

The precompiled python libraries can be decompiled with `uncompyle6`.

## Premium Crack

From web frontend's request `_task=license&_action=get_info`, we can find that it is `get_info_ajax` from `data/web/plugins/license/license.php` handles this request which is registered in `$this->register_action('get_info', array($this, 'get_info_ajax'));`.

We can obviously observe that obfuscated function `$info = $this->rcmail->license->wbf2d66a297();` is called here and defined in file `data/web/program/lib/Qmail/obfuscator/qmail_license.php`. I wrote a simple script to de-obfuscate these  php code.

By searching all code with keyword `qmail_license.php` and `->license`, we can find that all premium features are called without validating license. This fact could also be verified by the front-end javascript code `data/web/plugins/license/license.min.js`. **WHTA A LOVELY CLIENT-SIDE VALIDATION**.

So you could bypass validation every time you open QMailAgent via DevTools (F12) or GreaseMonkey and etc. Moreover, you can create a bookmark in bookmark bar with content: `javascript:` as prefix and code below.

It is quite acceptable to use DevTools (F12) becasue of the low using rate of premium features.

QNAP integrates QMailAgent and other applications with `iframe` tag.  The id attribution of QMailAgent iframe is ext-gen + RANDOM\_NUMBER + qmail, so we can find this iframe via css query selector easily.

I make a fake license which is valid to 2099-12-31. Code below:

```javascript
document.querySelectorAll('[id^=ext-gen][id$=qmail]').forEach( k => {
  k.contentWindow.rcmail.license.stop_refresh();
  k.contentWindow.rcmail.license.update({"info": {"license": [{"status": "valid", "id": "Default", "name": "Default", "info": {"valid_from": "", "valid_until": "", "apply_date": "", "enable_func": {"add_account": {"limit": -1 } }, "expired_soon": false } }, {"status": "valid", "id": "Test", "name": "Test", "info": {"valid_from": "2020-01-01", "valid_until": "2099-12-31", "apply_date": "2020-01-01", "enable_func": {"add_account":{"limit": -1 }, "backup" :{}, "restore":{}, "merge":{}, }, "expired_soon": false } } ], "merge_func": {"add_account": {"limit": -1, "valid_from": "", "valid_until": "", "apply_date": "", "expired_soon": false }, "backup" :{}, "restore":{}, "merge":{}, } }, "is_premium": true, "unlimit": -1 })
} )
```

If you visit QMailAgent directly via `http://NAS/qmail`, you could simple use:

```javascript
rcmail.license.stop_refresh()
rcmail.license.update({"info": {"license": [{"status": "valid", "id": "Default", "name": "Default", "info": {"valid_from": "", "valid_until": "", "apply_date": "", "enable_func": {"add_account": {"limit": -1 } }, "expired_soon": false } }, {"status": "valid", "id": "Test", "name": "Test", "info": {"valid_from": "2020-01-01", "valid_until": "2099-12-31", "apply_date": "2020-01-01", "enable_func": {"add_account":{"limit": -1 }, "backup" :{}, "restore":{}, "merge":{}, }, "expired_soon": false } } ], "merge_func": {"add_account": {"limit": -1, "valid_from": "", "valid_until": "", "apply_date": "", "expired_soon": false }, "backup" :{}, "restore":{}, "merge":{}, } }, "is_premium": true, "unlimit": -1 })
```

Furthermore, If you can SSH login to NAS, you could use QMailAgent's scripts (like `/mnt/ext/opt/qmail/web/restoreworker.sh` and `/mnt/ext/opt/qmail/web/backupworker.sh`) direcly since all premium features are called without validation.

Yet more directly, you can backup and restore via backing up database via mysqldump and backing up email folders via copy and paste. You can use mysql via command `/usr/local/mariadb/bin/mysql -uroundcube -pmypassword  -S /mnt/ext/opt/qmail/var/qmail_mysqld.sock`.


## One More Thing

I heard the news about that K-9 joined ThunderBird family. I Hope that ThunderBird could make a headless version, so that i can put it in VPS to receive mails and use local ThunderBird/K-9 client to fetch/sync data via WEB API.
Anther thought is using Firefox Sync to sync all mails and mailbox configurations between clients.


PS: Python script for deobfuscating PHP code. <del>WHAT A REGEX JOKE</del>
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
