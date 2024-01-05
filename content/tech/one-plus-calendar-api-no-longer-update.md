Title: 一加日历接口不再更新
Date: 2024-01-01 18:00
Slug: one-plus-calendar-api-no-longer-update
Tags: oneplus, calendar, api
Category: tech

###-TL;DR-
老手机+系统的宿命：依赖的中国特色服务不再更新了。

###-Intro-
时间已经来到了2024年，虽然设置了仅工作日的手机闹钟，但是元旦早上还是被吵醒，因为它不知道今天是节假日。

###-Analysis-
通过X-plore提取日历APK，拖到jadx里分析出接口。

流程如下：

1. 鉴权
    
    ```curl -X POST https://appr.1plus.io/v1/auth/calendar/token -A "com.oneplus.calendar/1.0.0" -d '{"client_id":"14254102-04f7-11ea-bb4e-804a145e0928", "client_secret":"1b9dc1d4-04f7-11ea-bb4e-804a145e0928"}'```

    返回Token： `{"token":"eyxxxxxxx.xxxxxxxx.xxxxxxxx"}`

2. 获取

    ```curl "https://appr.1plus.io/v1/app/calendar" -H "Authorization: Bearer eyxxxxxxx.xxxxxxxx.xxxxxxxx" -A "com.oneplus.calendar/1.0.0"```

    返回302，以及一个链接 `https://app-resources.1plus.io/calendar/config/default/20221223/config.json?Expires=time&Signature=xxxx&Key-Pair-Id=xxxx`

3. 下载
    
    ```curl -o holiday.json "https://app-resources.1plus.io/calendar/config/default/20221223/config.json?Expires=time&Signature=xxxx&Key-Pair-Id=xxxx"```

    返回内容:

    ```json
    {
        "projectname": "OPCalendar",
        "content": [
            {
                "name": "NationalHolidays",
                "value": {
                    "startYear": 2020,
                    "yearsIndex": [
                        0,
                        36,
                        74,
                        113,
                        146
                    ],
                    "holidays": [
                        {
                            "0": true
                        },
                        {
                            "18": false
                        },
                        {
                            "23": true,
                        },
                        //略
                        {
                            "0": true
                        },
                        //略
                        {
                            "0": true
                        },
                        //略
                        {
                            "0": true
                        },
                        //略
                        {
                            "279": false
                        },
                        {
                            "280": false
                        }
                    ]
                }
            }
        ]
    }
    ```


    `yearIndex`代表`holidays`数组的第x位开始为该年度的节假日，2024年应该从146开始，可是整个`holidays`数组也就146项，也就是所并没有2024年的数据。

    从链接也能发现，最后一次更新是`20221223`。一开始还以为服务没了，例如域名没了等等，现在发现只是没有人去维护更新数据了。

###-Solution-

1. 放弃，风险点在于，补班的日子没闹钟。

2. MITM，修改响应内容，然后禁用自动更新以防止被旧的覆盖。(似乎需要系统证书，因为在Fiddler中还是显示的是HTTPS CONNECT，意味着需要root设备)

###-Outro-
在写作的时候，收到一个非常旧的vivo备机的明日上班的提醒，点进去一看人家就更新了2024的节假日安排。只能说一加确实不**讲究**。

尽管*大氢亡了*，作为前朝余孽，还是拒绝将一加7T升级到ColorOS。

~~当然比某些国际大厂好一点，至少还曾经有过。~~ [分分钟打脸](https://web.archive.org/web/20240105152651/https://weibo.com/2022252207/NArThaySS)

###Reference
- [病友1](https://web.archive.org/web/20240101104139/https://bbs.oneplus.com/thread/1496695386788593672)
- [病友2](https://web.archive.org/web/20240101104034/https://bbs.oneplus.com/thread/1488566300006416389)
- [病友3](https://web.archive.org/web/20240101103706/https://bbs.oneplus.com/thread/1485760578604498950)