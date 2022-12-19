Title: Linux下 .Net 踩过的一些坑
Date: 2022-09-24 00:00
Slug: dotnet-under-linux
Category: tech
Tags: csharp,dotnet

0. dotnet framework / dotnet standard / dotnet core / dotnet 傻傻分不清楚 Ref: [MSDN](https://learn.microsoft.com/en-us/dotnet/standard/frameworks)

1. 版本 -> 语言特性

	匹配但又不完全匹配 .NetFramework4.5.2 不支持C#8.0，但如果在.csproj中加上在<langVersion>8.0</langVersion>或<langVersion>preview</langVersion>就可以使用一部分特性，可惜最好用的Range/Indices却不能用。 Ref:  [StackOverflow](https://stackoverflow.com/questions/56651472/does-c-sharp-8-support-the-net-framework),[MSDN](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version)

2. 不使用 dotnet build/publish 命令

	编译: dotnet /usr/lib64/dotnet/sdk/<sdk_version>/Roslyn/bincore/csc.dll 后面就是常规的CSC参数 例如 `-lib:/usr/lib64/dotnet/shared/Microsoft.NETCore.App/<sdk_version>/` 或 `-r`

	运行: `dotnet exec --runtimeconfig /usr/lib64/dotnet/sdk/<sdk_version>/dotnet.runtimeconfig.json <exe_file>`

	Ref: [StackOverflow](https://stackoverflow.com/questions/46065777/is-it-possible-to-compile-a-single-c-sharp-code-file-with-the-net-core-roslyn-c)

3. 打包成单个文件（带运行时）

	 项目文件(.csproj)中 <PropertyGroup> 下增加

	```xml
		<PublishSingleFile>true</PublishSingleFile>
		<SelfContained>true</SelfContained>
		<RuntimeIdentifier>linux-x64</RuntimeIdentifier>
		<!-- for: Unable to find package Microsoft.NETCore.App.Runtime.linux-x64 with version (= 6.0.0-rc.2.21470.23) -->
		<!--      NU1102:   - Found 98 version(s) in nuget.org [ Nearest version: 6.0.0-rc.2.21480.10 ] -->
		<!-- https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props#runtimeframeworkversion -->
		<RuntimeFrameworkVersion>6.0.9</RuntimeFrameworkVersion>
	```

	RID(RuntimeIdentifier) Ref: [MSDN](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog)

	RuntimeFrameworkVersion是为了避免Nuget.org上下不到你SDK版本对应的运行时。

4. 不想使用在线Nuget

	项目目录下新建 nuget.config。内容：

	```
	<configuration>
	<packageSources>
	<clear>
	<add key="local" value="<path>"
	</packageSources>
	</configuration>
	```

	将下载好的.nuget包放进`<path>`

5. 使用Omnisharp-Vim 如果遇到Found 0 Instance问题

	* `let g:OmniSharp_server_use_net6 = 1` 然后重装 `:OmniSharpInstall`

	* 如果你的sdk\_version带`rc`（预览版本），新建 ~/.omnisharp/omnisharp.json

	```json
	{
		"SDK": {
			"includePrereleases": true
		}
	}
	```

