# 直播订阅
## 配置
### modules中clone本项目
在config目录下修改__bot__.py, 然后在MODULES_ON中增加`livewatcher`
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
    "b站主播id 2": {
        "flag": "false",
        "notification": "true",
        "group": [
            "通知群号"
        ]
    }
}
```
替换b站主播id和通知群号即可, 
也支持群内发送命令: `增加直播监听 主播id`和`删除直播监听 主播id`进行增添
