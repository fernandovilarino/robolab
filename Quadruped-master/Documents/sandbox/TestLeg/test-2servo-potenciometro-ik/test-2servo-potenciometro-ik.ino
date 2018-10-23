#include <Servo.h>

Servo s1;
Servo s2;
Servo s3;

int ang1 = 90;
int ang2 = 90;
int ang3 = 90;


float TODEG = 57.295; // Conversion from rad to deg

float coxa =  8.4;  // cm
float femur = 9.3;  // cm
float tibia = 11.5;  // cm

float x = 20;
float y = 4;
float z = 0;

int analog1;
int analog2;

void setup() {

  s1.attach(2);
  s2.attach(3);
  s3.attach(4);
  
  Serial.begin(9600);
}



// Angle for servo 2
int IKang2(double x, double y, double z){
  double hip = sqrt( pow(y,2) + pow( sqrt(pow(x,2)+pow(z,2)) - coxa, 2) );
  double alpha1 = acos(y/hip);
  double alpha2 = acos(( pow(hip,2) + pow(femur, 2) - pow(tibia,2))/(2*hip*femur));
  double alpha = alpha1 + alpha2;
  return (alpha * TODEG);
}

// Angle for servo 3
int IKang3(double x, double y, double z){
  double hip = sqrt( pow(y,2) + pow( sqrt(pow(x,2)+pow(z,2)) - coxa, 2) );
  double beta = acos(( pow(hip,2) - pow(tibia,2) - pow(femur,2))/(-2*tibia*femur));
  return (beta * TODEG);
}



void loop() {
  analog1 = analogRead(A0);
  analog2 = analogRead(A1);

  //ang2 = map(analog1, 0, 1023, 0 ,179);
  //ang3 = map(analog2, 0, 1023, 0 ,179);

  x = map(analog1, 0, 1023, 10.0, 25.0);
  y = map(analog2, 0, 1023, 3.0, 10.0);

  x = float(analog1*15/1023)+10;
  y = float(analog2*7/1023)+3;

 /* delay(500);
  x = 14;
  y = 4;*/
  
  ang2 = 180-IKang2(x, y, z);
  ang3 = 180-IKang3(x, y, z);

  s2.write(ang2);
  s3.write(ang3);

 /* for (int i=0; i<6; i++){
    x = i+14;
    y = 4+(i/2);

    ang2 = 180-IKang2(x, y, z);
    ang3 = 180-IKang3(x, y, z);

    s2.write(ang2);
    s3.write(ang3);

    delay(100);
  }
  delay(100);
  for (int i=6; i>0; i--){
    x = i+14;
    //y = 4+(i/2);

    ang2 = 180-IKang2(x, y, z);
    ang3 = 180-IKang3(x, y, z);

    s2.write(ang2);
    s3.write(ang3);

    delay(100);
  }*/

  Serial.print("angle1: ");
  Serial.print(analog1);
  Serial.print(", x: ");
  Serial.print(x);  
  Serial.print(", ");
  Serial.print(ang2);
   
  Serial.print("   angle2: ");
  Serial.print(analog2);
  Serial.print(", y: ");
  Serial.print(y);  
  Serial.print(", ");
  Serial.println(ang3);

  delay(15);
  
}
