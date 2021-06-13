# 直播订阅
## 配置
### 在hoshino/modules中clone本项目

`git clone https://github.com/voidbean/livewatcher.git`

在hoshino/config目录下修改__bot__.py, 然后在MODULES_ON中增加`livewatcher`

### 修改watcher-config.json中的配置 
以此为范例:
```json
{
    "b站主播id": {
        "flag": "false",
        "notification": "true",
        "group": [
            "通知群号"
        ]
    },
    "ytb主播id": {
        "flag": "false",
        "notification": "true",
        "group": [
            "通知群号"
        ]
    }
}
```
替换b站主播id/ytb主播id和通知群号即可, 
代码会自动识别对应id属于b站还是ytb
也支持群内发送命令: `增加直播监听 主播id`和`删除直播监听 主播id`进行增添
notification设置为true时会主动@全体成员发送消息, 使用该功能时注意需要给bot加上管理员权限,否则没法@全体成员
