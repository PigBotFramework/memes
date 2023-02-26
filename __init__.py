import time
from pbf import PBF
from utils.RegCmd import RegCmd

_name = "表情包增强"
_version = "1.0.1"
_description = "增强qq的表情包功能"
_author = "xzyStudio"
_cost = 0.00

class memes(PBF):
    def __enter__(self):
        return [
            RegCmd(
                name = "添加快捷表情 ",
                usage = "添加快捷表情 <触发关键词> <图片>",
                permission = "anyone",
                function = "memes@add",
                description = "添加快捷表情",
                mode = "表情增强",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "MessageListener",
                usage = "MessageListener",
                permission = "anyone",
                function = "memes@messageListener",
                description = "MessageListener",
                mode = "表情增强",
                hidden = 0,
                type = "message"
            ),
            RegCmd(
                name = "删除快捷表情 ",
                usage = "删除快捷表情 <关键词>",
                permission = "anyone",
                function = "memes@rmMemes",
                description = "删除快捷表情",
                mode = "表情增强",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "快捷表情列表",
                usage = "快捷表情列表",
                permission = "anyone",
                function = "memes@listMemes",
                description = "列出您的快捷表情",
                mode = "表情增强",
                hidden = 0,
                type = "command"
            )
        ]
    
    def add(self):
        if '\r\n' in self.data.args[2]:
            self.data.args[2] = self.data.args[2].replace("\r\n", "")
        self.mysql.commonx("INSERT INTO `botMemes` (`keyword`, `url`, `uid`, `time`) VALUES (%s, %s, %s, %s)", (self.data.args[1], self.data.args[2], self.data.se.get("user_id"), time.time()))
        self.client.msg().raw("face54已添加！")
        
    def messageListener(self):
        memesList = self.mysql.selectx("SELECT * FROM `botMemes` WHERE `uid`=%s", (self.data.se.get("user_id")))
        for i in memesList:
            if self.regex.pair(i.get("keyword"), self.data.message):
                self.client.msg().raw(i.get("url"))
                self.client.CallApi('delete_msg', {'message_id':self.data.se.get('message_id')})
                return 
    
    def listMemes(self):
        arr = []
        memesList = self.mysql.selectx("SELECT * FROM `botMemes` WHERE `uid`=%s", (self.data.se.get("user_id")))
        for i in memesList:
            arr.append({"type": "node", "data": {"name": self.data.botSettings.get("name"), "uin": self.data.botSettings.get("myselfqn"), "content": "{} => {}".format(i.get("keyword"), i.get("url"))}})
        self.client.CallApi("send_group_forward_msg", {"group_id":self.data.se.get("group_id"), "messages":arr})
    
    def rmMemes(self):
        self.mysql.commonx("DELETE FROM `botMemes` WHERE `keyword`=%s and `uid`=%s", (self.data.args[1], self.data.se.get("user_id")))
        self.client.msg().raw("face54已删除！")