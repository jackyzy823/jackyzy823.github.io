Title: 白嫖(破解)Zorin OS Pro/Ultimate
Date: 2022-01-03 14:20
Modified: 2024-11-15 01:40
Slug: zorin-os-pro-upgrade
Tags: zorin,bypass,crack,pro,premium,ultimate,破解
Category: tech


### 总结：

1. 在 `/etc/apt/sources.list.d/zorin.list` 添加 `deb https://packages.zorinos.com/premium bionic main`。其中Zorin 15 对应的是bionic，Zorin 16 对应的是focal, Zorin 17 对应的是jammy。如果需要源码再添加`dec-src https://packages.zorinos.com/premium bionic main` 

2. 新增 `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp` 增加 `Acquire {  http::User-Agent "Zorin Os Premium" }`

3. 注意 Zorin 17 会报错 `The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 5FD7496A07D323BC` 可以 1) `curl -sS https://packages.zorinos.com/zorin_os_key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/zorin.gpg` 或 2) `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys  5FD7496A07D323BC` 参考 https://github.com/PEAKYCOMMAND/Zorin-OS-Pro/blob/main/zorin.sh

4. <可选> 完成后，`apt update && apt install apt-user-agent-zorin-os-premium` ， 并删除 `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp`

5. <可选> 更多布局 `apt install zorin-apperance-layouts-shell-premium zorin-apperance-layouts-xfce-premium`

6. <可选> 如果对Premium源包含哪些软件包感兴趣，可以查看 `/var/lib/apt/lists/premium`

**TL;DR**

### 为什么

之前试用某个版本的Manjaro Gnome，发现引入了[Gnome Layout Switcher](https://gitlab.manjaro.org/Chrysostomus/gnome-layout-switcher)功能，里面有多种界面风格可以选择，实现的原理是组合Gnome Shell不同的插件实现风格的切换，然后从项目的描述中(A simple gui for choosing gnome layout. Inspired by the similar application by Zorin os)看到灵感来源于Zorin OS。

出于猎奇心理，迫不及待下载试用。官网还有收费的Pro（以前叫Ultimate）版本，此外收费版的大版本升级仍然要重新付费。收费版只比普通版多了几个可以切换的布局，外加Xfce桌面环境和一些生产力软件。

### 猜想并验证

开始思考，Zorin OS是怎么区别普通版还是收费版，第一反应就是软件源做了限制：观察普通版(Core)的Zorin的APT源地址， 访问 `https://packages.zorinos.com/` 发现存在`premium`目录。直接点击会跳转到介绍页面。看到这种现象，猜测有某种认证机制，第二反应就是根据HTTP头例如User-Agent等来判断的。以前也看到过文章讲[如何修改APT的User-Agent](https://dmfrsecurity.com/2018/12/10/changing-apts-user-agent-string/)。

那么如何验证猜想呢，通过搜索，找到了一个Premium的镜像下载链接，好孩子们不要学。虚拟机挂载进行进入Live模式，列出软件包和APT的设置，果然如此。

那么问题来了，我为什么不一开始就这么做呢？逐渐开始怀疑人生。只能安慰自己，等出了新版本，不用找盗版下载链接，直接从普通版升级上去。

### 杂谈

Zorin我也只是试用一下，本身Ubuntu已经是二次发行版了（虽然比Debian更流行），Zorin更是二次发行的二次发行。当然吐槽归吐槽，收费版本是他的商业模式也无可厚非，只能说一个愿打一个愿挨。有闲钱的还是可以赞助一下开源项目，但是对于我来说39刀真的有点贵。界面是挺好看的，也确实要花时间人力来设计，但是elementaryOS都没你的贵，而且人家还是自愿捐款（Update:[好吧，我乌鸦嘴了](https://news.ycombinator.com/item?id=30611748)）。

