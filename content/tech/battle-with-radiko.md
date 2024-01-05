Title: 实战Radiko
Date: 2018-07-30 23:00
Slug: battle-with-radiko
Category: tech
Tags: radiko,reversing

0.  我为什么要研究呢？

    还不是为了听**Kalafina倶楽部**。可是发生了这种事情，大家都不想的。

1. 背景知识

    1. PC版实行IP锁区
    2. Android版实行GPS锁区
    3. 共同点：都是通过一套鉴权接口来生成用于播放的Token
    4. 不同点：传递的参数不同，Android版在Headers里传递GPS信息，而PC版不传。PC版和Android版的鉴权密钥不同

2.  利用点
    
    Android版接口不验证IP，在PC版上实现Android版的鉴权流程，即传递我们伪造的GPS信息和Android版的鉴权密钥。

3. 封堵点

    Android版接口同样实施IP锁区。想到一个办法，但是仍然有被封堵的可能性：Token分享，即利用日本各县IP（日本Rajiko用户/代理）不断生成Token共享使用。

4. 鉴权流程

    密钥(`Key`): 完整的密钥

    部分密钥(`PartialKey`): 从完整的密钥的`offset`处开始的`length`字节


    鉴权分两步

    1.  /v2/api/auth1

        请求参数 : `platform_info` , `user_id`

        响应参数 : `token` to be valid, `offset` ,`length`

    2.  /v2/api/auth2

        请求参数: `token` ,`platform_info` ,`user_id`, `PartialKey` ,  `connection type` (in android), `gps location`(in android)

        响应参数: `location` (and your `token` is valid for radio stations in this location) / `OUT` (ip invalid or gps invalid)
    
    
    PC端中密钥在`apps/js/playerCommon.js`里：`bcd151073c03b352e1ef2fd66c32209da9ca0afa`。

    然而,在Android端密钥被动态链接库保护起来，显然Android端的密钥比PC段长很多。

5. 如何获取Android版鉴权密钥Partialkey的完整部分
    1. HTTPS抓包，修改Auth1的返回的Header中的offset为0和length足够长，让客户端这边吐出足够长的Key (Update：Android 7以上不行,详见android:networkSecurityConfig）

        （Update2: 因为发现安卓上新版本的radiko使用了新的密钥aSmartPhone7o，才有的5中的所有Update)

    2. 写一个Apk通过createPackageContext来调用Radiko的native函数getKeyNative2，也是让他吐出足够长的key 
        
        (Update:如果不想写APK可以尝试使用[BeeShell](https://github.com/zhanghai/BeeShell)作为Java的REPL运行环境） 主要伪代码： `Context mmsCtx = context.createPackageContext("jp.radiko.Player",   Context.CONTEXT_INCLUDE_CODE | Context.CONTEXT_IGNORE_SECURITY);  Class.forName("jp.radiko.k.k", true, mmsCtx.getClassLoader()); ` 
    
        (Update2:旧版本so可行，新版本好像防范了这个方法，使用BeeShell调用会先回到桌面再进入就退出，跟调试的时候现象一样，估计是加了相关的判断逻辑？)

    3. 逆向。通过逆向可以发现key长度是固定的。

6. 逆向的难点
    1.  so经过混淆加壳，需要动态调试。

    2.  脱完第一层壳后内有反调试，反模拟器，反root，验证dex完整性，验证签名正确性等手段。检测出异常之后就退出。这也就是为什么在模拟器/root过的设备中运行不起来的原因。
    
    其实，反调试等手段还是比较好突破的，因为函数入口点只有一个，只要JMP过去就行了。所以我的Patch里都是一个字节的修改。修改完之后可以让它自行修复so，还原生成鉴权密钥的函数和密钥数据。

    暂时还没研究出自动化分析并修改的方法，所以radiko版本更新一次就要改六个so文件还是蛮吐血的事情。(Update: 自动化工具见我的项目[Radiko Android Kai](https://github.com/jackyzy823/radiko_android_kai))

    Update: 经过互联网搜索，推测加固的方法是CrackProof。在某次Radiko升级后，之前的脚本失效了，而且变得更加难跟进调试了，怀疑CrackProof加固的技术也升级了，放弃放弃。

    (Update2: 看到一篇文章讲如何逆向CrackProof，结果只有第一步。)

    (Update3: Radiko v8 使用了Flutter，然后竟然把key打包进去了，路径 /assets/flutter_assets/assets/key/，详见https://github.com/garret1317/yt-dlp-rajiko/blob/f4a74e390da521ef76021b7ba6fdf2874e005311/yt_dlp_plugins/extractor/radiko_key.py ， 以前可是不会犯这个错误的啊，以前是DEBUG版本才会从sdcard路径下读取这个文件)

7. 还原后的生成函数
    
    生成鉴权密钥的函数（位于.text段）超级简单：从.data段+0x20+offset处memcpy长度为length的数据作为鉴权密钥。

8. PC版的浏览器插件遇到的坑
    
    详见另一篇[文章]({filename}/tech/different-behaviors-between-firefox-webextensions-and-chrome-extension.md)关于WebExtensions里的各种坑
    

9. Apk修改思路（基于smali）

    此外顺手也把APK给修改了，不从GPS设备获取数据，直接传假数据啦。

    1.  修改鉴权流程方法

        因为破坏了Apk包的完整性,原样调用鉴权流程,会导致退出。解决方法如下：

        1. 直接替换getPartialkey方法，把第5步中得到的完整的key， 不调用so，也就不怕so检测。

        2. createPackageContext 调用安装的Radiko，但是本机root的话还是会崩溃。
        
        3. 修改so绕过检测

        这里我选了第三种，其实第一种更好，因为可以少修改3个so文件。

    2.  伪造GPS

        研究发现APK有DEVELOPER_MODE模式，自带传假数据的接口和选择地区的界面，那我们把DEVELOPER_MODE打开就好，启动后可以选择不同地区。
        
        这也告诉我们调试用逻辑不要发布到正式版的包里。本来要自己写一个选择地区的界面还是蛮麻烦的，还要考虑程序流程、持久化什么的，现在倒好全都白送啦！

    3.  绕过Premium和Timeshift、及录音

        绕过Timeshift很简单，让它写本地数据库时一直写最大值，把最长期限从1天改成8天。
        
        一开始以为Timeshift是一天内最多随便听3小时节目，后来发现是一个节目你点击开始听之后的一天内最多可以听3小时，也就是说过了这一天或者听超过三小时，这个节目就再也听不了了。

        绕过Premium在浏览器拓展里实现了Token管理比较好做，Android上要改太多东西就放弃了，反正退出重进重新选就好了。

        浏览器拓展有录音和往期下载，但是在Android上也比较麻烦，因为也是要改太多东西，考虑是不是能配合raziko。
        
    4.  其他边边角角的坑

        例如发现Radiko的闪退bug之类的。

10. 下一步研究计划

    爬完了所有Radiko的ON-AIR曲目，不过并不是所有台都有ON-AIR信息，准备研究J-POP潮流（并不。默默看了下我团的数据，真是十八线中的十八线。

附上逆向动态调试时写的IdaPython的脚本:

```python
def anadebug(segname=None):
	start = get_first_seg()
	while True:
		name = get_segm_name(start)
		end = get_segm_end(start)
		if segname:
			if name == segname:
				print hex(start),hex(end)
				ida_auto.plan_and_wait(start,end,1)
			else:
				pass
		elif name.startswith("debug") and (get_segm_attr(start,SEGATTR_PERM) & ida_segment.SEGPERM_EXEC)==1:
			print hex(start),hex(end)
			ida_auto.plan_and_wait(start,end,1)
		start = get_next_seg(start)
		if start == BADADDR:
			break

run_to(get_segm_start(idautils.cpu.EIP)+0x406)
wait_for_next_event(WFNE_SUSP, -1)
anadebug()
firstseg  = get_segm_start(idautils.cpu.EAX)
run_to(firstseg+0x37c0)
wait_for_next_event(WFNE_SUSP, -1)
run_to(firstseg+0x5fe) #call eax
wait_for_next_event(WFNE_SUSP, -1)
anadebug()
secondseg = get_segm_start(idautils.cpu.EAX)
run_to(secondseg + 0x241f) 
wait_for_next_event(WFNE_SUSP, -1)
add_bpt(secondseg+0x2144)
run_to(secondseg+0x2144)
wait_for_next_event(WFNE_SUSP, -1)
#decrypt seg
while ord(get_bytes(idautils.cpu.EBP-0x10,1,0))!=0xf:
	run_to(secondseg+0x2144)
	wait_for_next_event(WFNE_SUSP, -1)
del_bpt(secondseg+0x2144)
anadebug()
thirdseg = get_segm_start(idautils.cpu.EAX)
run_to(thirdseg+0x41a) 
wait_for_next_event(WFNE_SUSP, -1)
idautils.cpu.EIP = get_item_end(idautils.cpu.EIP) #jump this call edx
# second+ 0x25f -> 4th seg
```

以上
