#include <Servo.h>

Servo s1;
Servo s2;
Servo s3;

int ang1 = 90;
int ang2 = 90;
int ang3 = 90;

int analog1;
int analog2;

void setup() {

  s1.attach(2);
  s2.attach(3);
  s3.attach(4);
  
  Serial.begin(9600);
}

void loop() {
  analog1 = analogRead(A0);
  analog2 = analogRead(A1);

  ang2 = map(analog1, 0, 1023, 0 ,179);
  ang3 = map(analog2, 0, 1023, 0 ,179);

  s2.write(ang2);
  s3.write(ang3);

  Serial.print("angle1: ");
  Serial.print(analog1);  
  Serial.print(", ");
  Serial.print(ang2);
   
  Serial.print("   angle2: ");
  Serial.print(analog2);  
  Serial.print(", ");
  Serial.println(ang3);

  delay(15);
  
}
