//JSON데이터를 역직렬화하기위해서 필요함!
#include <ArduinoJson.h>

#define cds A0

StaticJsonDocument<48> doc;

void setup() {
  //파이썬과 통신속도가 9600이다!(보-레이트가 9600이다)
  Serial.begin(9600);
}

void loop() {
  int data = analogRead(cds);
  
  doc["cds"] = data;
  
  String myjson = "";
  serializeJson(doc, myjson);
  Serial.println(myjson);  
  delay(500);
}


