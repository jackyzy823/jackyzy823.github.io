Title: ThinkPad Linux镜像
Date: 2022-01-02 14:00
Slug: thinkpad-linux-image
Tags: thinkpad,image,iso,linux,fedora,ubuntu
Category: tech


### **TL;DR**
总结：Lenovo垃圾前端。

链接/Link: https://pcsupport.lenovo.com/us/en/api/v4/lenovorecovery/linuxRdvdConfig

内容/Content:

```json
[{"installationIntroduction": "https://download.lenovo.com/km/media/attachment/Linux_Support_Product_List.PDF"}, {"operatingSystem": "Ubuntu", "installationIntroduction": "https://download.lenovo.com/km/media/attachment/Ubuntu_OEM_Install.PDF", "mappingList": [{"machineType": "20R3,20R4", "productName": "L13", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L13-20191115-174.iso"}, {"machineType": "20U1,20U2", "productName": "L14", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L14-20200609-225.iso"}, {"machineType": "20U3,20U4", "productName": "L15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L15-20200728-237.iso"}, {"machineType": "20T4,20T5", "productName": "P15s", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20TQ,20TR", "productName": "P15v", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T15p_P15v-20200820-87.iso"}, {"machineType": "30E0,30E1", "productName": "P620", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-P620-20201030-422.iso"}, {"machineType": "20S0,20S1", "productName": "T14", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20UD,20UE", "productName": "T14 AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}, {"machineType": "20T0,20T1", "productName": "T14s", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14s_X13-20200615-60.iso"}, {"machineType": "20UH,20UJ", "productName": "T14s AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}, {"machineType": "20S6,20S7", "productName": "T15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20TN,20TM", "productName": "T15p", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T15p_P15v-20200820-87.iso"}, {"machineType": "20U9,20UA", "productName": "X1 Carbon 8th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X1C8-20200818-76.iso"}, {"machineType": "20UB,20UC", "productName": "X1 Yoga 5th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X1Y5-20200429-57.iso"}, {"machineType": "20T2,20T3", "productName": "X13", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14s_X13-20200615-60.iso"}, {"machineType": "20SX,20SY", "productName": "X13 Yoga", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X13Yoga-20200527-59.iso"}, {"machineType": "20UF,20UG", "productName": "X13 AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}]}, {"operatingSystem": "Fedora", "installationIntroduction": "https://download.lenovo.com/km/media/attachment/Fedora_Install.PDF", "mappingList": [{"machineType": "20U9,20UA", "productName": "X1 Carbon 8th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20QT,20QU", "productName": "P1 Gen 2", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20TH,20TJ", "productName": "P1 Gen 3", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_33_1.2_P1G3_P15.iso"}, {"machineType": "20QN,20QQ", "productName": "P53", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20ST,20SU", "productName": "P15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_33_1.2_P1G3_P15.iso"}]}]
```

### 细节

因为打算买[ThinkPad]({filename}/rambling/rambling-about-picking-thinkpad.md)，考虑下一台设备主用Linux。ThinkPad有OEM版本的Ubuntu/Fedora，对笔记本的各种新硬件稍微适配了驱动。然而这些镜像却没地方下载，或者说搜索不到。这种[帮助页面](https://pcsupport.lenovo.com/us/en/solutions/ht512169)还不如没有。

通过另一个[官方帮助文档](https://pcsupport.lenovo.com/us/en/solutions/ht511743-how-to-download-the-linux-image-from-the-e-support-page)中的图片，发现PC Support应该有下载，但是怎么也找不到图片中的链接，你说Windows因为授权、费用等问题必须要注册并验证机器才能下载可以理解，Linux镜像就没必要吧。举例：[L15](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/thinkpad-l-series-laptops/thinkpad-l15-type-20u3-20u4/downloads/order-recovery-media)恢复镜像的下载页面。而且即使注册了账号，仍然不显示前述文档中的链接，我甚至一度考虑暴力遍历找到合适机型的序列号。

难道隐藏在网页页面里吗？抱着这个猜想打开了DevTools，发现了事情的真相：网络选项卡里有着这么一个请求`https://pcsupport.lenovo.com/us/en/api/v4/lenovorecovery/linuxRdvdConfig`，内容就是心心念念的镜像链接。

那么问题来了？既然又请求，为什么不显示呢？

通过字符串搜索加断点大法，找到相关处理逻辑，结果令人哭笑不得。

[发起的请求](https://pcsupport.lenovo.com/esv4/js/chunk-common.5e36f246.js):
```javascript
y = function() {
            return i.a.get(r["UrlUtility"].getFullPath("/api/v4/lenovorecovery/linuxRdvdConfig")).then((function(e) {
                return e
            }
            ))
```
[调用者及回调函数](https://pcsupport.lenovo.com/esv4/js/psp-downloads/order-recovery-media.cbeb43e5.js):
```javascript
 Object(p["h"])().then((function(t) {
                        t.data && (n.linuxRecoveryConfig = JSON.parse(t.data),
```

其中在函数`judgeMtForLinux`中遍历匹配并设置对应型号机器的镜像。发现`n.fedoraImageLink`和`n.ubuntuImageLink`赋值完后就没有后续的任何调用处理，更不用说前端的展示逻辑了。

分析到这里，不得不佩服联想的前端。

所以帮助文档里面的图是怎么截的？

### 彩蛋

发现了这么一处逻辑`n.blockLinux = "in" == window["MSELocaltionCountryByIP"],`，虽然和之前的问题一样，没有任何后续的调用，但为什么要屏蔽印度呢？

