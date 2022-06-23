Title: ThinkPad Linux Image Download Link
Date: 2022-01-02 14:00
Slug: thinkpad-linux-image
Tags: thinkpad,image,iso,linux,fedora,ubuntu
Category: tech
Lang: en

### **TL;DR**

In short: The front-end of Lenovo's website sucks.

Request Link: https://pcsupport.lenovo.com/us/en/api/v4/lenovorecovery/linuxRdvdConfig

Content:

```json
[{"installationIntroduction": "https://download.lenovo.com/km/media/attachment/Linux_Support_Product_List.PDF"}, {"operatingSystem": "Ubuntu", "installationIntroduction": "https://download.lenovo.com/km/media/attachment/Ubuntu_OEM_Install.PDF", "mappingList": [{"machineType": "20R3,20R4", "productName": "L13", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L13-20191115-174.iso"}, {"machineType": "20U1,20U2", "productName": "L14", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L14-20200609-225.iso"}, {"machineType": "20U3,20U4", "productName": "L15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-L15-20200728-237.iso"}, {"machineType": "20T4,20T5", "productName": "P15s", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20TQ,20TR", "productName": "P15v", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T15p_P15v-20200820-87.iso"}, {"machineType": "30E0,30E1", "productName": "P620", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-P620-20201030-422.iso"}, {"machineType": "20S0,20S1", "productName": "T14", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20UD,20UE", "productName": "T14 AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}, {"machineType": "20T0,20T1", "productName": "T14s", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14s_X13-20200615-60.iso"}, {"machineType": "20UH,20UJ", "productName": "T14s AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}, {"machineType": "20S6,20S7", "productName": "T15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14_T15_P15s-20200720-69.iso"}, {"machineType": "20TN,20TM", "productName": "T15p", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T15p_P15v-20200820-87.iso"}, {"machineType": "20U9,20UA", "productName": "X1 Carbon 8th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X1C8-20200818-76.iso"}, {"machineType": "20UB,20UC", "productName": "X1 Yoga 5th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X1Y5-20200429-57.iso"}, {"machineType": "20T2,20T3", "productName": "X13", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14s_X13-20200615-60.iso"}, {"machineType": "20SX,20SY", "productName": "X13 Yoga", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-X13Yoga-20200527-59.iso"}, {"machineType": "20UF,20UG", "productName": "X13 AMD", "downloadLink": "https://download.lenovo.com/km/media/attachment/Ubuntu-T14AMD_T14sAMD_X13AMD-20200914-91.iso"}]}, {"operatingSystem": "Fedora", "installationIntroduction": "https://download.lenovo.com/km/media/attachment/Fedora_Install.PDF", "mappingList": [{"machineType": "20U9,20UA", "productName": "X1 Carbon 8th Gen", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20QT,20QU", "productName": "P1 Gen 2", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20TH,20TJ", "productName": "P1 Gen 3", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_33_1.2_P1G3_P15.iso"}, {"machineType": "20QN,20QQ", "productName": "P53", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_32_1.6_X1C8_P1G2_P53.iso"}, {"machineType": "20ST,20SU", "productName": "P15", "downloadLink": "https://download.lenovo.com/km/media/attachment/Fedora_Workstation_Live_x86_64_33_1.2_P1G3_P15.iso"}]}]
```

### Details

It's quite hard to find Linux based distribution's Image ISO download link in lenovo's support site though Ubuntu and Fedora both claim that they are supported in ThinkPad machines.

According to a picture from [offical support document](https://pcsupport.lenovo.com/us/en/solutions/ht511743-how-to-download-the-linux-image-from-the-e-support-page), **THE LINK SHOULD BE THERE**.

Will the link be hidden in the page? With the question i open the DevTools and in the tab of `Network` then i notice there's a request `https://pcsupport.lenovo.com/us/en/api/v4/lenovorecovery/linuxRdvdConfig` which contains all download links of linux iso.

Well, so you make a request to get the links, but ** DO NOT DISPLAY IT IN FRONTEND?**. What are you doing and how did you made a screenshot for your document, Lenovo?

One more thing, Why you block India IP address to get linux image download link? See the javascript code: `n.blockLinux = "in" == window["MSELocaltionCountryByIP"],`.

