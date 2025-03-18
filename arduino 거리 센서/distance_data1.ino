//JSON데이터를 역직렬화하기위해서 필요함!
#include <ArduinoJson.h>

#define trig 2
#define echo 3

StaticJsonDocument<48> doc;

void setup() {
  //파이썬과 통신속도가 9600이다!(보-레이트가 9600이다)
  Serial.begin(9600);
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
}

void loop() {
  digitalWrite(trig,LOW);
  delayMicroseconds(2); //2마이크로초 대기
  digitalWrite(trig,HIGH);
  delayMicroseconds(10); //10마이크로초 대기
  digitalWrite(trig,LOW);

  //발사된 초음파신호를 echo핀으로 수신함
  //echo핀에 반사된 high신호가 입력으로 들어올때까지의 시간을
  //마이크로초 단위로 반환함
  unsigned long duration = pulseIn(echo,HIGH);

  float dist = (duration / 29.0)/2; //cm
  
  doc["dist"] = dist;
  
  String myjson = "";
  serializeJson(doc, myjson);
  Serial.println(myjson);  
  delay(500);
}
