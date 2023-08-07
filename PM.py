import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime
import time

# URL des HTTP-Servers der Die Daten des Fotowiederstandes liefert
url = "http://192.168.178.156"
aktwert=1024
# Der Schwellwert, unter dem eine Mail verschickt wird
schwellwert = 300

def mail(empfaenger):
	# E-Mail-Konfiguration
	sender_email = "noreply@pmsose2023.de" # E-Mail Adresse
	password = "PASSWORT"  # PASSWORT des Mailaccounts einfügen

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

# Daten vom HTTP-Server abfragen & mainloop
while True:
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
		body = "Die Heizung ist ausgefallen:"+ str(datetime.now())
		print(datetime.now())
		datei = open('./log.txt','a')
		datei.write(str(datetime.now())+"\n")
		datei.close()
		datei = open('./email.txt','r')
		for zeile in datei:
			mail(zeile)
		datei.close()
		time.sleep(3600)
