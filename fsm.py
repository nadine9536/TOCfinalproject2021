from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot.models import MessageTemplateAction
from utils import send_button_message, send_image_message
from catchdata import cloudpicture, airpicture, today, week
from flask import Flask, jsonify, abort, send_file

# from flask import request
#global variable
city = "嘉義市"

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        # self.machine.get_graph().draw("FSM.png", prog= 'dot')

    def is_going_to_state(self, event):
        text = event.message.text
        return text.lower() != "graph"

    def on_enter_state(self, event):
        title = "請選擇功能"
        text = "請依照需求點選功能"
        btn = [
            MessageTemplateAction(
                label = "今天天氣",
                text = "今天天氣"
            ),
            MessageTemplateAction(
                label = "今天空氣品質",
                text = "今天空氣品質"
            ),
            MessageTemplateAction(
                label = "一周天氣預報",
                text = "一周天氣預報"
            ),
            MessageTemplateAction(
                label = "衛星雲圖",
                text = "衛星雲圖"
            )
        ]
        url = 'https://upload.cc/i1/2021/12/24/ZurWMI.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        
    
    def is_going_to_todayweather(self, event):
        text = event.message.text
        if text == "今天天氣":
            return True
        return False
    
    def on_enter_todayweather(self, event):
        print("I'm entering todayweather")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的城市")
    # def on_enter_todayweather(self, event):
    #     title = "請選擇縣市"
    #     text = "請選擇縣市"
    #     btn = [
    #         MessageTemplateAction(
    #             label = "宜蘭縣",
    #             text = "宜蘭縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "桃園市",
    #             text = "桃園市"
    #         ),
    #         MessageTemplateAction(
    #             label = "新竹縣",
    #             text = "新竹縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "苗栗縣",
    #             text = "苗栗縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "彰化縣",
    #             text = "彰化縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "南投縣",
    #             text = "南投縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "雲林縣",
    #             text = "雲林縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "嘉義縣",
    #             text = "嘉義縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "屏東縣",
    #             text = "屏東縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "臺東縣",
    #             text = "臺東縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "花蓮縣",
    #             text = "花蓮縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "澎湖縣",
    #             text = "澎湖縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "基隆市",
    #             text = "基隆市"
    #         ),
    #         MessageTemplateAction(
    #             label = "新竹市",
    #             text = "新竹市"
    #         ),
    #         MessageTemplateAction(
    #             label = "嘉義市",
    #             text = "嘉義市"
    #         ),
    #         MessageTemplateAction(
    #             label = "臺北市",
    #             text = "臺北市"
    #         ),
    #         MessageTemplateAction(
    #             label = "高雄市",
    #             text = "高雄市"
    #         ),
    #         MessageTemplateAction(
    #             label = "新北市",
    #             text = "新北市"
    #         ),
    #         MessageTemplateAction(
    #             label = "臺中市",
    #             text = "臺中市"
    #         ),
    #         MessageTemplateAction(
    #             label = "臺南市",
    #             text = "臺南市"
    #         ),
    #         MessageTemplateAction(
    #             label = "連江縣",
    #             text = "連江縣"
    #         ),
    #         MessageTemplateAction(
    #             label = "金門縣",
    #             text = "金門縣"
    #         )
    #     ]
    #     url = 'https://i.imgur.com/tyOAIAG.png'
    #     send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_city(self, event):
        global city
        city = event.message.text
        if city[0] == "台":
            tmp = "臺" + city[1:]
            city = tmp
        if city == "宜蘭縣" or "桃園市" or "新竹縣" or "苗栗縣" or "彰化縣" or "南投縣" or "雲林縣" or "嘉義縣" or "屏東縣" or "臺東縣" or "花蓮縣" or "澎湖縣" or "基隆市" or "新竹市" or "嘉義市" or "臺北市" or "高雄市" or "新北市" or "臺中市" or "臺南市" or "連江縣" or "金門縣":
            return True
        else:
            return False
    
    def on_enter_city(self, event):
        try:
            print("I'm entering city")
            global city
            reply_token = event.reply_token
            send_text_message(reply_token, today(city))
            #self.go_state(event)
            self.go_back()
        except Exception as ex:
            self.go_back()
            send_text_message(reply_token, "此城市不存在，請重新啟動功能")
            print(ex)
    
    def is_going_to_picture(self, event):
        text = event.message.text
        if (text == "衛星雲圖"):
            return True
        return False
    
    def on_enter_picture(self, event):
        print("I'm entering picture")
        reply_token = event.reply_token
        send_image_message(reply_token, cloudpicture())
        #self.go_state(event)
        self.go_back()

    def is_going_to_air(self, event):
        text = event.message.text
        if (text == "今天空氣品質"):
            return True
        return False
    
    def on_enter_air(self, event):
        print("I'm entering air")
        reply_token = event.reply_token
        send_image_message(reply_token, airpicture())
        #self.go_state(event)
        self.go_back()

    def is_going_to_weekweather(self, event):
        text = event.message.text
        if text == "一周天氣預報":
            return True
        return False
    
    def on_enter_weekweather(self, event):
        print("I'm entering weekweather")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的城市")

    def is_going_to_weekcity(self, event):
        global city
        city = event.message.text
        if city[0] == "台":
            tmp = "臺" + city[1:]
            city = tmp
        if city == "宜蘭縣" or "桃園市" or "新竹縣" or "苗栗縣" or "彰化縣" or "南投縣" or "雲林縣" or "嘉義縣" or "屏東縣" or "臺東縣" or "花蓮縣" or "澎湖縣" or "基隆市" or "新竹市" or "嘉義市" or "臺北市" or "高雄市" or "新北市" or "臺中市" or "臺南市" or "連江縣" or "金門縣":
            return True
        else:
            return False
    
    def on_enter_weekcity(self, event):
        print("I'm entering city")
        try:
            global city
            reply_token = event.reply_token
        #week(city)
        #send_image_message(reply_token, "https://5be4cb182235.ngrok.io/show-week")
            send_text_message(reply_token, week(city))
        #self.go_state(event)
            self.go_back()    
        except Exception as ex:
            self.go_back()
            send_text_message(reply_token, "此城市不存在，請重新啟動功能")
            print(ex)
        

    def is_going_to_graph(self, event):
        text = event.message.text
        return text.lower() == "graph"
    
    def on_enter_graph(self, event):
        print("I'm entering graph")
        reply_token = event.reply_token
        send_image_message(reply_token, "https://upload.cc/i1/2021/12/23/QM4zpa.png")
        self.go_back()
    