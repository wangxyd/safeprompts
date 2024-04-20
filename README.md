## 插件描述

一款用于chatgpt-on-wechat的简易的提示词保护插件，当对话消息中匹配到屏蔽的关键词时，插件自动返回一个表情包图片。

## 配置步骤

1. 准备屏蔽的关键词词库文件：将`safeprompts.txt.template`复制为`safeprompts.txt`，并自行配置，每行一个词。

2. 准备表情包图片：下载表情包图片，最好是GIF格式，并置于一个单独的文件夹，比如`/root/chatgpt-on-wechat/safeprompts/images`。

3. 修改插件配置文件：将`config.json.template`复制为`config.json`，并自行配置，示例如下：

```json
{
  "action": "replace",
  "images_dir": "/root/chatgpt-on-wechat/safeprompts/images"
}
```

在以上配置项中：

- `action`: 对用户消息的处理行为；
- `images_dir`: 表情包图片所在目录。

目前插件对用户消息的处理行为`action`有如下两种：

- `ignore` : 如果消息包含被屏蔽的关键词，忽略这条消息，这条消息不会被机器人回复；
- `replace` : 如果消息包含被屏蔽的关键词，插件随机返回一个表情包图片目录中的表情包；如果找不到任何图片，忽略这条消息。

## 备注

插件不会拦截管理员用户的任何消息！

## 致谢

核心逻辑来自敏感词插件https://github.com/zhayujie/chatgpt-on-wechat/tree/master/plugins/banwords
搜索功能实现来自https://github.com/toolgood/ToolGood.Words