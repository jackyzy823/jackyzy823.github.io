Title: Random Thoughts
Slug: random-thoughts

一些奇思妙想，等待实现。

* 自建Chrome Sync Server
    - 需要自建Gaia (Google Accounts and ID ADministration)，考虑Proxy到自建的Firefox Accounts，Brave没使用账号体系。考虑Ory Hydra。
    - 需要Sync Server , Python实现的测试服务器已被移出代码库，考虑用Brave的go-sync实现，后端不用AWS的DynamoDB，而Proxy到Firefox的syncserver。已经用sqlite实现。
    - 安卓上怎么指定--gaia-url和--sync-url，经过实验发现没法指定GAIA，安卓上使用的是AccountManager, account type是GoogleAuthUtil.GOOGLE_ACCOUNT_TYPE。 也许我们可以自建Authenticator，用这个添加完账号，再到Chromium内选择这个账号，而不是直接在Chromium内选择添加账号，[参考](https://stackoverflow.com/questions/42855175/use-addaccountexplicitly-by-2-different-apps-with-same-account-name-and-account)和[参考2](https://stackoverflow.com/questions/39497751/android-different-apks-same-authenticator-account-type)和[实现](http://blog.udinic.com/2013/04/24/write-your-own-android-authenticator)和Chromium[相关代码](https://source.chromium.org/chromium/chromium/src/+/main:components/signin/public/android/java/src/org/chromium/components/signin/SystemAccountManagerDelegate.java;l=170;drc=41c3810bbb8bd6c2c50dfbc123069dcc7638edae;bpv=1;bpt=1)
    - 能否做到Chrome和Firefox的数据互通（部分）Firefox加密的数据怎么解开？Chrome Sync Server作为Firefox Sync的客户端？


* 模仿Nitter，搭建Weibo、Zhihu前端

