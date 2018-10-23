#include <Servo.h>

String inBuff = "";   // Buffer entrada serial
String head;          // Cabezera del mensaje
String msg;           // mensaje

int angh = 90;
int angv = 90;

Servo servov;   // Servo eje vertical
Servo servoh;   // Servo eje horizontal




void setup(){
  Serial.begin(115200);
  servoh.attach(2);
  servov.attach(3);
}


void readIn(){
	
  char recieved = Serial.read();
	if(recieved == ';'){
	  if(inBuff.length() > 2){
			head = inBuff.substring(0, 2);
			msg = inBuff.substring(2);
			
  			if (head=="v+"){          // Incrementar angulo servo v
  				if(angv + msg.toInt() > 180){
  				  angv = 180;
  				}else if (angv + msg.toInt() < 0){
            angv = 0;
          }else{
            angv += msg.toInt();
          }  
  			}else if (head=="h+"){    // Incrementar angulo servo H
  					if(angh + msg.toInt() > 180){
  					  angh = 180;
  					}else if (angh + msg.toInt() < 0){
              angh = 0;
            }else{
  						angh += msg.toInt();
            }
              
          }else if(head=="hv"){    // Establecer angulos H y V      (Ej: H->90 v->180   ==>   hv090180;)
    					if(msg.substring(0,3).toInt() < 181 && msg.substring(0,3).toInt() > -1){
    						if(msg.substring(3).toInt() < 181 && msg.substring(3).toInt() > -1){
    							angh = msg.substring(0,3).toInt();
    							angv = msg.substring(3).toInt();
  						}
  					}
          }
			}
    Serial.println(inBuff);
	  inBuff = "";
	}else{
		inBuff += recieved;
   }
	
  }



void loop(){
	
	if(Serial.available() > 0){
		readIn();
	}
  
  servoh.write(angh);
  servov.write(angv);

  //Serial.print(angv);
  //Serial.print("  ");
  //Serial.println(angh);
  

  delay(10);
 
}

