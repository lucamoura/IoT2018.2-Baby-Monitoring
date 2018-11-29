import telepot
import cv2
import time
import paho.mqtt.client as mqtt 
from datetime import datetime

contgiro = 0
oldTime = datetime.now()
now = datetime.now()
msg = ''
bot = telepot.Bot("797831227:AAENikTGLuEeyScOnRgJx60C_MlBSMbOTNE")
chat_id = '86791355'
gyNow = 10.0
gyOld1 = 10.0
gyOld2 = 10.0
gyOld3 = 10.0

def camU():
 
    camera_port = 1
  
    nFrames = 30
  
    camera = cv2.VideoCapture(camera_port)
     
    file = "imagenTeste.png"
         
    #print "Digite <ESC> para sair / <s> para Salvar"   
     
    #emLoop= True
      
    #while(emLoop):
     
    retval, img = camera.read()
    time.sleep(1)
    cv2.imshow('Foto',img)

    cv2.imwrite(file,img)
    time.sleep(1)
     
    cv2.destroyAllWindows()
    camera.release()
    return 0

def sendM(m):
	try:
		bot.sendMessage(chat_id,m)
	except:
		return


def on_message(client, userdata, message):

	try:
		global contgiro
		global msg
		global now
		global oldTime
		global gyNow
		global gyOld1
		global gyOld2
		global gyOld3

		now = datetime.now()
		msg = str(message.payload.decode("utf-8"))
		print(msg)
		cmd = msg.split(" ")
		print(cmd)
		print("message received " ,str(message.payload.decode("utf-8")))
		print(message.topic)
		if message.topic == "temp":
			
			if float(cmd[1]) > 29.6 :
				print("if 1")
				m = " alerta alta temperatura :" + str(cmd[1])
				sendM(m)
				
				time.sleep(1)
		elif cmd[0] == 'giro' and contgiro < 7 and (now - oldTime).seconds < 5*60 :
			oldTime = now
			gyNow = float(cmd[1])
			a =abs(gyOld1+gyOld2+gyOld3 + gyNow)/4.0
			print(a)
			#print("$$$$$$$$$$$$$$$$")
			if  a*85 < abs(gyNow) or a  > abs(gyNow)*85 : 
				print("#########################   trigou ############################")
				contgiro = contgiro +1 
				print(contgiro)
			gyOld1 = gyOld2
			gyOld2 = gyOld3
			gyOld3 = gyNow

		elif cmd[0] == 'giro' and contgiro == 7 :
			oldTime = now
			m = "alguem esta inquieto"
			
			sendM(m)
			camU()
			time.sleep(1)
			sendF("imagenTeste.png")
			gyNow = float(cmd[1])
			contgiro = 0 
			gyOld1 = gyOld2
			gyOld2 = gyOld3
			gyOld3 = gyNow
	except :
		main()
	#print("message topic=",message.topic)
	#print("message qos=",message.qos)
	#print("message retain flag=",message.retain)


 
def sendF(caminho):        #envia para o usuario o arquivo no caminho especificado
	global chat_id
	arquivo = open(caminho,'rb')
	bot.sendDocument(chat_id,arquivo)
	arquivo.close()

		



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
main()