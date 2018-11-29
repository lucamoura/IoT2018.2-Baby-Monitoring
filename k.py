'''
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()

'''
	
import paho.mqtt.client as mqtt
import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


msg= ""
msg2= "20"

def on_message(client, userdata, message):
	global msg
	global msg2
	msg = str(message.payload.decode("utf-8"))
	msg2 =  msg.split(" ")[1]

	

def on_connect(client,userdata,flags,rc):
	if rc == 0:
		print("connect OK")
	else:
		print("Bad connection Returnned code = ",rc)



class Test(App):


	



	def build(self):
		global Case
		global msg
		global msg2	
		t = 1



		box = BoxLayout(orientation='vertical')
		
		#button = Button(text=msg[1],font_size=30)
		#self.label = Label(text=msg2,font_size=30)
		self.label = Label(text='1',font_size=30)
		#box.add_widget(button)
		broker_address="192.168.137.1"
		client = mqtt.Client("P2")
		client.on_message=on_message
		client.connect(broker_address)
		client.loop_start()
		client.subscribe("temp")
		client.loop_stop()
		box.add_widget(self.label)
		
		Clock.schedule_interval(self.update, t)


		return box

	def update(self, t):
		
		broker_address="192.168.137.1"
		client = mqtt.Client("P2")
		client.on_message=on_message
		client.connect(broker_address)
		client.loop_start()
		client.subscribe("temp")
		time.sleep(1)
		client.loop_stop()
		self.label.text = msg2
		



Test().run()

'''
def main():
	#192.168.137.1
	#bot.sendMessage(chat_id," alerta alta temperatura :")

	broker_address="192.168.137.1"
	#broker_address="iot.eclipse.org"
	while True:
		print("creating new instance")
		client = mqtt.Client("P1") #create new instance
		client.on_message=on_message #attach function to callback
		print("connecting to broker")
		client.connect(broker_address) #connect to broker
		client.loop_start() #start the loop
		#print("Subscribing to topic","temp")
		client.subscribe("temp")
		#print("Subscribing to topic","gx")
		client.subscribe("gx")
		#print("Publishing message to topic","house/bulbs/bulb1")
		#client.publish("/temp","OFF")
		time.sleep(4) # wait
		client.loop_stop()
main()'''