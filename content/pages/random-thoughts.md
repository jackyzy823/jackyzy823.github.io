Title: Random Thoughts
Slug: random-thoughts

一些奇思妙想，等待实现。

* 自建Chrome Sync Server
    - 需要自建Gaia (Google Accounts and ID ADministration)，考虑Proxy到自建的Firefox Accounts，Brave没使用账号体系。
    - 需要Sync Server , Python实现的测试服务器已被移出代码库，考虑用Brave的go-sync实现，后端不用AWS的DynamoDB，而Proxy到Firefox的syncserver，
    - 安卓上怎么指定--gaia-url和--sync-url
    - 能否做到Chrome和Firefox的数据互通（部分）Firefox加密的数据怎么解开？Chrome Sync Server作为Firefox Sync的客户端？

