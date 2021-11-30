Title: An update to my blog comment system
Date: 2021-11-30 15:30
Slug: blog-comment-system-upgrade-2021
Tags: blog,comment
Category: tech
Lang: en

It has been a long time since i dumped something randomly on this blog. When i want to write something agian, i found that Staticman's public service , the comment system i used to use , had been banned by Github due to abuse. Besides, Travis CI , used as the publishment system, no more provides free service. I decided to do something to make the comment system work again.

OT: I can understand the hard situation for Travis CI. Nobody should be blamed for deciding to stop providing free service. However in this winnner-takes-all industry, i worried about Travis' future.

You can still use Staticman , instead of with the public instance , with self-hosted instances on `Heroku` , your own VPS or some else so-called compute platform.But i do not want to register a Heroku account neither purchase a VPS to deploy comment system for a blog nobody cares. I even think of `Cloudflare Worker` and give up for the just same reason as Heroku. Besides, deploying on `Cloudflare Worker` requires additonal modifications to Staticman.I also found a comment system hosted on `Vercel`.

After a further consideration, I found that the core function of these kind of comment systems is to use Github API to create Pull Requests or directly push commit to blog repository.

In another word, you can make these API calls direcly in frontend via `fetch` or `XMLHttpRequest` or `octokit` . These API calls require GITHUB_TOKEN (Personal Access Token) to work. However the scope of a GITHUB_TOKEN is far **too** wild to use in frontend safely. Even with the mininal set of permissions (scope:public_repo) for comment system , a token can do anything to your any public repo. Github should implement a better ACL for token which allows users make more interesting stuff.

Since i couldn't find a perfect way to create a new comment system, i put it aside for another a-long-time. History always repeats itself. I want to write blog again. I began with the easy part , changing publishment system to Github Actions , then it made me  think whether i can use it to build comment system. The Document leads me to two manually triggered events: workflow_dispatch and repository_dispatch which also need GITHUB_TOKEN. 

This time i didn't give up in half way. I made a search with "repository_dispatch anonymous" as keyword. **Bingo**, i found a Github App called **[Public Action Trigger](https://github.com/apps/public-action-trigger)** which can solve all my problems and **Benkaiser** the great guy who made this also hosts a public service with `Azure Function`. The only thing i need to do is to authorize this app with repo permission and let comments from blog page go through the public service via `fetch`. Then the public service will trigger my workflow to make a Pull Request with comments content. Also if this public service is gone, hope no, i can also host one by myself just by registering an Azure account and publishing a Github App. Well, i'll never host one. Thank you Benkaiser! 

He also metioned a similar thought to GITHUB_TOKEN scope. We both hoped that Github can work on this. If Github solved the problem, i can finally build a comment system without any third party services except Github.

The implementation is under [.github/workflow](https://github.com/jackyzy823/jackyzy823.github.io/tree/source/.github/workflows) and <del>the ugly javascript part</del> [frontend part](https://github.com/jackyzy823/jackyzy823.github.io/tree/source/hikaru/templates/article.html).

If you are interested, just leave a comment ,wait half minute, and [visit](https://github.com/jackyzy823/jackyzy823.github.io/pulls) to see what happened.

Finally, hope that i will write more blogs.

