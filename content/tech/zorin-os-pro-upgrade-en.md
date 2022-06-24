Title: How to free upgrade from Zorin OS to Pro/Ultimate
Date: 2022-01-03 14:20
Slug: zorin-os-pro-upgrade
Tags: zorin,bypass,crack,pro,premium,ultimate,破解
Category: tech
Lang: en

Well, details and comments are in chinese version article. Here're only the steps.

### Steps

1. Add content  `deb https://packages.zorinos.com/premium bionic main` in file `/etc/apt/sources.list.d/zorin.list` . For Zorin 15, use `bionic`, For Zorin 16 use `focal`.  If you also need source code , add content `dec-src https://packages.zorinos.com/premium bionic main` as well.

2. Create new file `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp` and add content `Acquire {  http::User-Agent "Zorin Os Premium" }`.

3. Optionally, do `apt update && apt install apt-user-agent-zroin-os-premium` and then delete file  `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp` 

4. To get more layouts of windows manager , do `apt install zorin-apperance-layouts-shell-premium zorin-apperance-layouts-xfce-premium`

5. you can check what packages are included in Premium via `/var/lib/apt/lists/premium`

