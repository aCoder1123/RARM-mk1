#include "header.h";
;
int PIN_RED = A7;
int PIN_GREEN = A8;
int PIN_BLUE = A9;

void setup() {
  Serial.begin(9600);
  for (int i: readPins) {
    pinMode(i, INPUT);
    Serial.println(i);
  };
  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);

  setColor(255, 0, 0); //red
  while (! Serial.available() > 0) {
    Serial.println("Starting");
    delay(50);
  }
};


void loop() {

  if (Serial.available() > 0) {
    setColor(10, 10, 200); //blue
    int pin = Serial.parseInt();
    if (pin == -1) {
      setColor(255, 0, 0); //red
      Serial.parseInt();
      while (! Serial.available() > 0) {
        // Serial.println("Waiting");
        delay(100);
      }
    }
    else if (pin <= 3 && pin > 0) {
      int data = analogRead(pin);
      Serial.println(data);
      Serial.flush();
    }
  }
  setColor(0, 255, 0); //green
  delay(20);
};


void setColor(int R, int G, int B) {
  analogWrite(PIN_RED,   R);
  analogWrite(PIN_GREEN, G);
  analogWrite(PIN_BLUE,  B);
}