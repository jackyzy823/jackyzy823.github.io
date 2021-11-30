Title: 博客评论系统升级
Date: 2021-11-30 13:50
Slug: blog-comment-system-upgrade-2021
Tags: blog,comment
Category: tech

好久没有在这个博客上写东西了，前段时间想在上面写点技术文章，然后发现原有的评论系统(Staticman)的公共服务因为被滥用挂了，此外原有的发布系统(Travis)也不再免费。这两个挂了，都可以理解。

说句题外话，Travis因为被Github Actions挤占了生存空间，不得不收缩资源。毕竟Github的爹Microsoft有自己的Azure云。但同样存在越收缩，就更多人转向Github Actions(例如我)，就越会被挤占这样赢者通吃的负反馈的情况。

我这个人呢就是有强迫症，在一件事情想到自认为完美的解决方案之前，绝不会动手去实现。例如我现在维护的[fxa-selfhosting](https://github.com/jackyzy823/fxa-selfhosting)项目，我自己还没有在实际环境里部署，因为各个方面都还有许多小问题。

Staticman还是可以继续使用的，只是不能用公共实例，而需要在Heroku，或自己的VPS等计算平台上部署私有实例就可以继续使用。但是我不想注册Heroku账号，也不想为一个没什么人访问的博客，搞个VPS部署评论系统。也想过用Cloudflare Worker来实现Staticman的功能，但因为也要注册账号，并且可能还要修改Staticman的代码，就放弃了。也见过利用Vercel部署的[系统](https://github.com/chinatimeline/chinatimeline-form)。

进一步思考，这一类的评论系统最核心的部分就是在开启审核的情况下，发起Pull Requests到你的博客的Repository，在关闭审核的情况下直接提交Commit到Repository，而这些（包含部署到Vercel的）都是基于Github的API实现的。也就是说，我在博客前端，调用这些API也能做到这些功能，但进一步查阅API后发现，GITHUB_TOKEN的权限划分颗粒太粗，缺乏精确到每个Repository，每个功能的能力，例如我需要一个token只有对我某个Repository发Pull Requests的权限，目前为止是做不到的。

以上为第一阶段的思考，思考完之后发现不完美，于是就搁置了下来，过了一段时间，我又重新燃起了写博客的想法，于是接着捡起来。因为本来就打算把发布系统换成Github Actions，于是思考能不能用Github Actions来做评论系统。

查阅文档后发现，能够手动外部触发的只有`workflow_dispatch`和`repository_dispatch`两个事件，但这俩个事件也都需要Github Token，但我不死心，以`repository_dispatch anonymous`为关键词搜索，发现了`Public Action Trigger`这个Github Apps，完美解决了我的问题，这个好心人利用Azure Function搭建了公共服务，只要授权这个Github Apps访问我的Repository，评论通过它的公共服务触发我的workflow发起Pull Requests，和之前的体验一模一样。当然，我也可以自建这个Public Action Trigger服务，但是要注册Azure账号和要发布Github Apps这两点阻止了我，反正公开服务能用一天就是一天。这个好心人也提到了我之前的想法，也认为Github Token的颗粒度太粗了，希望未来Github能解决这个问题，这样我就又能重构博客系统，并且完全不依赖除Github之外的第三方服务了。

看到完美解决方案的曙光后，我开始动手实现[workflow](https://github.com/jackyzy823/jackyzy823.github.io/tree/source/.github/workflows)。一个workflow是发布系统，每当我Push或者我合并评论的Pull Requests，就触发构建命令，生成静态页面内容。另外一个workflow是评论系统，每当有来自`repository_dispatch`事件的评论，就发起Pull Requests。

当然也还是有一贯的缺点，就是我或者别人回复前一条评论，前一条评论的作者无法收到任何通知。思考了一下算了，发送邮件要钱，免费服务又不好用。

希望之后能重新捡起这个博客，多写点技术内容。

总结：Github上基于Pull Requests的评论系统，最核心的就是要把安全地使用GITHUB_TOKEN调用API（自建），或者授权Github Apps使用，即交由第三方调用API。

