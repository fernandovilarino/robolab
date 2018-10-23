#include <Servo.h>

String inBuff = "";
int ang = 0;
Servo servo;



void setup(){
  Serial.begin(9600);
  servo.attach(2);
}

void loop(){

  if(Serial.available() > 0){
    char recieved = Serial.read();
    if(recieved == ';'){
      if(inBuff != ""){
        if(inBuff.toInt() < 181 && inBuff.toInt() > -1){
          ang = inBuff.toInt();
          //Serial.println(ang);
        }
      }
      inBuff = "";
    }else{
      inBuff += recieved;
    }
  }
  

  servo.write(ang);

  delay(10);
 
}

