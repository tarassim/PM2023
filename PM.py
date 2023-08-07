import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime, timedelta
import time
import os

# URL des HTTP-Servers der Die Daten des Fotowiederstandes liefert
url = "http://192.168.178.156"
aktwert=1024
# Der Schwellwert, unter dem eine Mail verschickt wird
schwellwert = 300

def mail(empfaenger):
	# E-Mail-Konfiguration
	sender_email = "noreply@pmsose2023.de" # E-Mail Adresse
	password = "SoSe2023"  # PASSWORT des Mailaccounts einfügen

	# Verbindung zum Postausgangsserver herstellen
	smtp_server = "smtp.ionos.de"
	smtp_port = 587
	smtp_tls_enabled = True

	# E-Mail-Inhalte
	subject = "Störung der Heizung Erkannt"
	body = "Die Heizung ist ausgefallen:"+ str(datetime.now())

	# E-Mail erstellen
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = empfaenger
	message["Subject"] = subject
	message.attach(MIMEText(body, "plain"))

	# E-Mail senden
	try:
		server = smtplib.SMTP(smtp_server, smtp_port)
		if smtp_tls_enabled:
			server.starttls()
		server.login(sender_email, password)
		server.sendmail(sender_email, empfaenger, message.as_string())
		print("Die E-Mail wurde erfolgreich verschickt.")
	except Exception as e:
		print("Beim Versenden der E-Mail ist ein Fehler aufgetreten:", str(e))
	finally:
		server.quit()

def frageAb():		
		try:
			response = requests.get(url)
			if response.status_code == 200:
				data = response.json()
				if 'Wert' in data:
					wert = data['Wert']
					aktwert = {wert}
	
			else:
				print(f'Fehler: {response.status_code}')
		except requests.exceptions.RequestException as e:
			print(f'Fehler bei der Anfrage: {e}')
		except json.JSONDecodeError as e:
			print(f'Fehler beim Parsen der JSON-Antwort: {e}')
			# Wenn der Schwellwert unterschritten(Licht/Display an) wurde:
		if(wert<schwellwert):
			print(datetime.now())
			loginhalt = {}
			neulog=""
			with open('./log.json','r') as datei:
				loginhalt = json.load(datei)
				neulog = {
					'zeit': str(datetime.now()),
					'ereignis': "Fehler"
					}
			with open('./log.json','w') as datei:	
				loginhalt['log'].append(neulog)
				json.dump(loginhalt, datei)
			configinhalt = {"NextRun":(time.time() * 1000)+(60*60*1000)}
			with open('./config.json','w') as datei:
				json.dump(configinhalt,datei)
			mailadressen = {}
			with open('mails.json', 'r') as datei:
				mailadressen = json.load(datei)
			for e in mailadressen['mail']:
				mail(e)

# Daten vom HTTP-Server abfragen & Mainloop, laufe 55 Durchgänge, danach wird das Programm vom System neu gestartet
for i in range(55):
        # Spamschutz
        if(not os.path.isfile('./config.json')):
                frageAb()
        else:
                with open('./config.json','r') as datei2:
                        confinhalt = json.load(datei2)
                        if (confinhalt['NextRun']<time.time() * 1000):
                                frageAb()
        # Warte eine Sekunde
        time.sleep(1) 
