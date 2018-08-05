Title: HLS中的AAC如何合并
Date: 2018-07-30 23:09
Slug: how-to-concat-aac-from-hls-streaming
Tags: aac,hls,m3u8,concat,http live streaming
Category: tech

在研究Radiko的时候,想实现在浏览器插件里把M3U8中所有的AAC保存成一个音频文件。

如果不限制在浏览器插件中，最简单的方法就是 `ffmpeg -c copy` 让万能的ffmpeg替你解决一切问题。然而一个插件带一个ffmpeg是不是有点大炮打蚊子？也考虑过替代方案，例如使用基于LLVM的Emscripten将ffmpeg转成Javascript，详见[ffmpeg.js](https://github.com/Kagami/ffmpeg.js/)。但也似乎过于沉重。此外经过测试，用ffmpeg合并的结果似乎并不正确。

第二种方法就是简单的拼接，但是拼接带来一个问题：部分播放器只能识别到第一个片段。

因此，在阅读了相关文档之后终于找到了正确的解决方法。

首先，这个aac里面包含了什么？
根据http-live-streaming的文档中关于[Packed Audio](https://tools.ietf.org/html/draft-pantos-http-live-streaming-23#section-3.4)部分的说明:
>   A Packed Audio Segment contains encoded audio samples and ID3 tags
   that are simply packed together with minimal framing and no per-
   sample timestamps.  Supported Packed Audio formats are AAC with ADTS
   framing [ISO_13818_7]; MP3 [ISO_13818_3]; AC-3 [AC_3]; and Enhanced
   AC-3 [AC_3].

>   A Packed Audio Segment has no Media Initialization Section.

>   Each Packed Audio Segment MUST signal the timestamp of its first
   sample with an ID3 PRIV tag [ID3] at the beginning of the segment.
   The ID3 PRIV owner identifier MUST be
   "com.apple.streaming.transportStreamTimestamp".  The ID3 payload MUST
   be a 33-bit MPEG-2 Program Elementary Stream timestamp expressed as a
   big-endian eight-octet number, with the upper 31 bits set to zero.
   Clients SHOULD NOT play Packed Audio Segments without this ID3 tag.

这个AAC是由ID3标签和ADTS组成的格式。

ADTS是AAC的一种编码方式，与另一种编码方式ADIF不同，ADTS可以在任意帧解码。因此我们只需要把AAC中的ID3标签去掉，然后在拼接起来就能得到正常的AAC文件了。

回到之前第一种方法，ffmpeg似乎只把第一个AAC的ID3标签去掉，后面的依然保留，不知道是不是参数设置错误还是什么问题。因此只能手动处理掉ID3标签。

那么ID3标签的格式又是啥呢？详见ID3官方文档[ID3标签](http://id3.org/id3v2.3.0#ID3v2_header) 或者Abobe给出的图解[ID3标签头](https://helpx.adobe.com/adobe-media-server/dev/timed-metadata-hls-hds-streams.html#id3_tag_introduction)

标签头如下:

| I     | D     | 3     | Version | Revision | Flags |   Size   |
|-------|-------|-------|---------|----------|-------|----------|
| 1Byte | 1Byte | 1Byte |  1Byte  |   1Byte  | 1Byte |  4Bytes  |

>*The bitorder in ID3v2 is most significant bit first (MSB).Most significant bit first (MSB) also known as big endian and network byte order.*

只需要去掉ID3标签头的10个字节加上Size的值,剩下的就是ADTS,简单合并就可以了。

如果想进一步了解ID3标签里的PRIV是啥的话，可以自行阅读文档[ID3 Private frame](http://id3.org/id3v2.3.0#Private_frame)。关于 com.apple.streaming.transportStreamTimestamp 的数值的意义。个人理解这个数值的绝对值是没有意义的，只有两个Timestamp的差值是有意义的。 `(stamp2 - stamp1) / (90*1000.0)`的结果就是第一段的秒数。参考资料：[MPEG-2 Program Elementary Stream timestamp 的作用](https://blog.csdn.net/qq_32430349/article/details/50218317)


以上