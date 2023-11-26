#include "header.h";
;

void setup() {
  Serial.begin(9600);
  // for (int i: readPins) {
  //   pinMode(i, INPUT);
  //   Serial.println(i);
  // };


  delay(250);
  // Serial.println("Starting");
};
void loop() {
  if (Serial.available() > 0) {

    int pin = Serial.parseInt();
    // Serial.println(pin);
    if (pin < 5 && pin > 0) {
      int data = analogRead(pin);
      Serial.println(data);
      Serial.flush();
    }
    
  };
  delay(200);
};