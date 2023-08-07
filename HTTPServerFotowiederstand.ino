#include <ESP8266WiFi.h>

const char* ssid = "SSID";
const char* password = "PASSWORT";
const IPAddress ip(192, 168, 178, 156); // Wählen Sie eine freie IP-Adresse im Bereich Ihres WLAN-Netzwerks
const IPAddress gateway(192, 168, 178, 1); // Gateway-IP-Adresse Ihres WLAN-Netzwerks
const IPAddress subnet(255, 255, 255, 0); // Subnetzmaske Ihres WLAN-Netzwerks

// ESP8266 Pin für Fotowiderstand (Analogeingang)
const int fotowiderstandPin = A0;

WiFiServer server(80);

void setup() {
  Serial.begin(115200);

  // Statische IP-Adresse, Gateway und Subnetzmaske festlegen
  WiFi.config(ip, gateway, subnet);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi verbunden.");
  Serial.println("IP address:\t");
  IPAddress myIP = WiFi.localIP();
  Serial.println(myIP);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    // Analogwert vom Fotowiderstand lesen
    int analogWert = analogRead(fotowiderstandPin);
  
    // HTTP-Header und Antwort erstellen
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println(); // Leerzeile zwischen Header und Inhalt
    client.print("{\"Wert\": ");
    client.print(analogWert);
    client.println("}");

    delay(1000); // Warten, bevor der nächste Wert gelesen wird
  }
}
