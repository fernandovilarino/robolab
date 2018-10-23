// ======================== Serial comunication variables ============================
String serialBuffer = "";  // Buffer for serial comunication
char received;             // Char received
String serialHeader;       // Header of the message (2 chars)
String serialBody;         // The body of the message recieved
// ===================================================================================





void setup() {
  Serial.begin(9600);

}



void fooAA(String var){

  // Process var.....
  Serial.print("Message AA received-> ");
  Serial.println(var);
}
void fooBB(String var){

  // Process var.....
  Serial.print("Message BB received-> ");
  Serial.println(var);
}
void fooCC(String var){

  // Process var.....
  Serial.print("Message CC received-> ");
  Serial.println(var);
}




// Read char by char recieved by the usb serial comunication
void readSerial(){

  while(Serial.available() > 0){
      
    received = Serial.read();
    
    if(received == ';'){              // End of the current message
  
      //Get message
      serialHeader = serialBuffer.substring(0, 2);
      serialBody = serialBuffer.substring(2);
  
      //Process header
      if(serialHeader == "aa"){   
        fooAA(serialBody);
      }else
      if(serialHeader == "bb"){
        fooBB(serialBody);
      }else
      if(serialHeader == "cc"){
        fooCC(serialBody);
      }
  
      // Send Arduino Ready signal
      Serial.print("1");
      // Clear the buffer
      serialBuffer = "";
      
    }else{          // Not the end of current message
      serialBuffer += received; //Add the received char to the buffer
    }
  }
  
}


void loop() {

  readSerial();


  delay(10);

}
