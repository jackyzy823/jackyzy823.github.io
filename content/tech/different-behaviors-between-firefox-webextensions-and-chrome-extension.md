Title: WebExtensions踩坑实录
Date: 2018-08-05 14:17
Slug: different-behaviors-between-firefox-webextensions-and-chrome-extension
Tags: extension,webextension
Category: tech

最近研究Radiko锁区(详见[文章]({filename}/tech/battle-with-radiko.md))，并写浏览器插件绕过限制。自从`Firefox Quantum`出现后，Firefox变得更加好用了，因此写浏览器插件考虑了同时支持`Firefox WebExtensions`和`Chrome Extension`，然而在实际编写插件的过程中还是因为两者有不少差异从而踩了不少坑，总结如下：

1. API差异与兼容性
    1. Manifest
        1. applications 
        
            这个key是Firefox需要的，而在Chrome上会报错，但不影响加载使用。解决方案是忽略或者通过构建工具生成两份不同的manifest。（注：Switchyomega好像用的是同样一份manifest，但是没有报错，需研究。）

        2. permissions -> unlimitStorage
            
            为了能在chrome.storage中存放大于5MB的内容，必须要声明这项权限。在Firefox的文档中，目前不声明也能存放大于5MB的内容。此外Chrome和Firefox关于这项权限对用户的提示也是不同的，Firefox会显式警告，而Chrome不会。参考[Document which permissions trigger user prompts in the different browsers](https://bugzilla.mozilla.org/show_bug.cgi?id=1411999)。

        3. declarativeContent
            
            目前Firefox不支持，不过有替代方案，参考Stackoverflow上的[问题](https://stackoverflow.com/questions/39252384/is-there-a-ff-equivalent-to-chrome-declarativecontent-onpagechanged)。
    
    2. browser_action

        1. 两者弹出窗口的UI不是完全一致的。将browser_style设置为true后排版一致，但是细节上还有许多不同。

        2. Firefox调试弹出窗口的UI较麻烦，需要强制所有的弹出窗口不消失，包括系统菜单，忘记取消就导致弹出的窗口关不掉。

    3. API -> webRequest
        
        1. host permission
            
            Firefox中，在\*.a.com这个页面下，如果想监听这个页面发起的对*.b.com的请求（CSS，Script,Image,以及**XMLHttpRequest**），需要同时将 \*.a.com和\*.b.com 加入host permission。而Chrome则不用。
            Firefox这么做的好处在于不怕影响到别的网站,坏处在于如果你想针对某个第三方服务的话,就得把所有用到它的网站都写进host permission,甚至不得不使用 `<all-urls>`。
             
            参考:[WebExtensions->webRequest](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/webRequest)。
            >To intercept resources loaded by a page (such as images, scripts, or stylesheets), the extension must have the host permission for the resource as well as for the main page requesting the resource. For example, if a page at "https://developer.mozilla.org" loads an image from "https://mdn.mozillademos.org", then an extension must have both host permissions if it is to intercept the image request.

        2. filterResponse

            Firefox支持读取并修改返回的内容。这个功能简直太实用了,然而Chrome不支持。

            Chrome中有变通方法，但是又各种使用上的限制。变通方法： 利用`redirectURL`将请求通过返回码`307 Internal Redirect` 重定向到 `Location: <Data Protocol>`。在实际使用过程中遇到不少问题。

            1. jQuery的ajax请求会把`307 Internal Redirect`当作错误响应。

            2. 无法定制返回头信息，会导致XMLHttpRequest的`CORS Preflight`失效。
                
            3. `Data Protocol`会导致非同源问题，例如`iframe`加载`src`，将`src`用`Data protocol`代替后，会被浏览器认为非同源，导致拒绝加载。见[Treating data URLs as unique origins for Firefox 57](https://blog.mozilla.org/security/2017/10/04/treating-data-urls-unique-origins-firefox-57/)。
            
            Chrome上的实现参考：[Implementation example of writable response bodies for Chromium extensions (API draft)](https://gist.github.com/Rob--W/9654450) 和 [webRequest response body reading/editing proposal](https://docs.google.com/document/d/1iE6M-YSmPtMOsec7pR-ILWveQie8JQQXTm15JKEcUT8)。

            我猜，出于安全性的考虑Chrome是不会实现这个功能的，能修改返回内容实在是太危险了，不清楚Firefox为什么会实现。

        3. RequsetHeaders
            
            Firefox的赋值是拼接而不是覆盖，例如原来 `header1:key1`, 执行`header1 = key2`后结果是`header1:key1,key2`。Chrome则是覆盖。

    4. API-> Downloads

        1. 如何下载blob内容

            将URL指定成 `URL.createObjectURL(new Blob([arraybuffer]))`即可。需要注意的是下载完成后最好`URL.revokeObjectURL`防止内存问题。

    5. API-> Storage
        
        1. getBytesInUse
            
            Firefox未实现，[polyfill](https://github.com/kiefferbp/webext-getBytesInUse-polyfill)有严重的性能问题，对内存使用有影响,不建议使用。

        2. 存储编码
            
            Storage的存储本来的设计并不是针对二进制数据进行存储,而是将JSON序列化后对字符串进行存储。因此如果用Uint8Array存储的话，数据能够正常存储，但是因JSON序列化的原因占用空间翻倍，而用Uint16Array存储的话会导致数据错误，主要涉及到Chrome中的JSON库对Unicode中Invalid Character（UTF-16 surrogate pairs的高位）的处理（处理成Replacement character）。

            在Stackoverflow中有这么一个[回答](https://stackoverflow.com/a/38242192)。
            > Unicode codepoints U+D800 to U+DFFF must be avoided: they are invalid in Unicode because they are reserved for UTF-16 surrogate pairs. Some JSON encoders/decoders will replace them with U+FFFD. 

            JSON标准定义:
            > However, whether a processor of JSON texts interprets such a surrogate pair as a single code point or as an explicit surrogate pair is a semantic decision that is determined by the specific processor

            然而在Firefox里没有这个问题。

    6. XMLHttpRequest In Extension

        在插件中通过XMLHttpRequest跨域请求资源，该资源会被缓存，然后如果浏览器再次请求这个资源就会发生响应头里面独缺Access-Control-Allow-Origin	这种情况，导致该响应被浏览器阻止以防止跨域安全问题。一番搜索后发现 Tim Berners-Lee 伟大的互联网发明人也遇到了这个[问题](https://lists.w3.org/Archives/Public/www-archive/2017Aug/0000.html)。 解决方法有两个:

        1. 在插件里为每个这种请求的响应补上`Access-Control-Allow-Origin`响应头

        2.  补上`Vary: Origin` 参见[CORS and caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin#CORS_and_caching)
        
        理论上最正确的解决方法是对方服务器加上`Vary: Origin`。

2.  差异化构建 

    要抹平Chrome与Firefox插件之间的差异确实很困难,差异化构建也许是一种可行的方式,到底是Webpack还是Grunt还是Gulp呢,选择有很多,但没有一种相对标准的方法。有不少可以值得借鉴的项目： [Switchyomega](https://github.com/FelisCatus/SwitchyOmega) , [AbemaTVChromeExtension](https://github.com/nakayuki805/AbemaTVChromeExtension) 。

    相关讨论：[Example of generating a manifest for both Firefox and Chrome](https://github.com/mdn/webextensions-examples/issues/286)


以上