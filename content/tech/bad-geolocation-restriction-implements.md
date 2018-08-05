Title: 不好的锁区设计
Date: 2018-07-30 21:30
Slug: bad-geolocation-restriction-design
Tags: geolocation,restriction,radiko,abema
Category: tech

众所周之，日本的互联网服务大部分都是锁区的，非日本IP无法访问。但是总是有一些锁区的设计让我们可以绕过这些限制。

0. 超级优秀的设计
    
    + [Summo](https://summo.jp )

        针对中国IP直接在TCP层面直接RST，不给你留一点机会。LOL。

1. 失败的设计

    一般而言,不好的锁区设计一般有两种。
    
    + 验证前置。
        
        大多由于锁区判断在前端而不是后端,前端绕过基本没有任何难度。

        + [FOD](http://fod.fujitv.co.jp)

        + Tv-Asahi

    + 信任用户的输入

        我说我的IP是日本IP就相信,是不是有点过于天真了呢? `X-Forwarded-For`确实不应该被信任。

        + Tver

            视频源用的是第三方服务Brightcove。资源API可被`X-Forwarded-For`绕过。

    + 两者皆有
    
        两种错误都犯的。

        + Abema.tv
            虽然有两种前端验证，Abema自己的和第三方服务Akami的，但都能绕过。

            视频源用的是第三方Akami。资源API可被`X-Forwarded-For`绕过。

2. 一言难尽的设计

    + [Radiko](http://radiko.jp/)

        Radiko提供PC端和移动端的服务,在不同平台上,锁区方式实现也不一样。

        在PC端,通过IP来锁区,X-Forwarded-For无效,虽然验证前置,但是鉴权接口依然在后端判断IP锁区。可以是设计得非常合理。

        在Android端，通过GPS来锁区，鉴权接口与PC端基本一致，但在HTTP头中增加GPS信息，且不验证IP。Android端检测有无root和是否使用虚拟定位。应该说除了不验证IP外，也设计得非常合理。

        但是，关键问题就出在Android端不验证IP，谁又规定PC上不能使用Android端的鉴权方式呢，在PC上伪造一个HTTP头填上想要的GPS信息简直轻而易举。见我的项目->[Rajiko](https://github.com/jackyzy823/rajiko) 和 [文章]({filename}/tech/battle-with-radiko.md)

        这种设计就让人感觉一言难尽，明明是想做好的，却功亏一篑。



3. 正常的设计

    + Alicesoft

        前端部署Squid，`X-Forwarded-For`无效。

    + GYAO

        首先在后端根据IP给出不同的资源页面，区外IP直接提示拒绝服务，如果想强行使用，资源API也会在涉及到关键参数`videoId`会在后端进行区域鉴定，不通过就拿不到`videoId`的值。同样是使用第三方Brigtcove的服务，而什么GYAO就如此优秀呢？


通过以上这些设计的比较我们可以看出：

1.  不要相信用户的输入，如`X-Forwarded-For`
2.  验证不要放在前端，关键接口要在后端验证
3.  注意不同平台接口差异
4.  要求第三方服务加强锁区限制，或提供接口自行验证


以上

P.S: 写了这文章会不会导致锁区加强了呢？