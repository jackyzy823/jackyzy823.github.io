Title: How to free upgrade from Zorin OS to Pro/Ultimate
Date: 2022-01-03 14:20
Modified: 2024-11-15 01:40
Slug: zorin-os-pro-upgrade
Tags: zorin,bypass,crack,pro,premium,ultimate,破解
Category: tech
Lang: en

Well, details and comments are in chinese version article. Here're only the steps.

### Steps

1. Add content  `deb https://packages.zorinos.com/premium bionic main` in file `/etc/apt/sources.list.d/zorin.list` . For Zorin 15, use `bionic`, For Zorin 16 use `focal`.  If you also need source code , add content `dec-src https://packages.zorinos.com/premium bionic main` as well.

2. Create new file `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp` and add content `Acquire {  http::User-Agent "Zorin Os Premium" }`.

3. Note: Under Zorin 17, You will encounter this issue: `The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 5FD7496A07D323BC`. The solution is 1) `curl -sS https://packages.zorinos.com/zorin_os_key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/zorin.gpg` or 2) `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys  5FD7496A07D323BC` . Reference: https://github.com/PEAKYCOMMAND/Zorin-OS-Pro/blob/main/zorin.sh

4. Optionally, do `apt update && apt install apt-user-agent-zorin-os-premium` and then delete file  `/etc/apt/apt.conf.d/99zorin-os-premium-user-agent-temp` 

5. To get more layouts of windows manager , do `apt install zorin-apperance-layouts-shell-premium zorin-apperance-layouts-xfce-premium`

6. you can check what packages are included in Premium via `/var/lib/apt/lists/premium`

