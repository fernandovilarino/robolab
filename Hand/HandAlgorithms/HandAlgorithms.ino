/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo1;  // create servo object to control a servo
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;



const int FLEX1_PIN = A1; // Pin connected to voltage divider output A1
const int FLEX2_PIN = A2; //
const int FLEX3_PIN = A4; //
const int FLEX4_PIN = A3; //
const int FLEX5_PIN = A5; //

int modo; //MODE CONTROL
          //MODO = 0 --> MIMIC MODE
          //MODO = 1 --> TRANSITION TO PAPER ROCK SCISSORS WIN MODE
          //MODO = 2 --> PAPER ROCK SCISSORS WIN MODE
          //MODO = 3 --> TRANSITION TO PAPER ROCK SCISSORS LOSE MODE
          //MODO = 4 --> PAPER ROCK SCISSORS LOSE MODE
          //MODO = 5 --> TRANSITION TO PAPER ROCK SCISSORS NORMAL MODE
          //MODO = 6 --> PAPER ROCK SCISSORS NORMAL MODE
          //MODO = 7 --> TRANSITION TO MIMIC MODE

          
int count_MODO1; // COUNT USED BY CONTROL THE MODE 1 TRANSITION START
int count_MODO3; // COUNT USED BY CONTROL THE MODE 3 TRANSITION START
int count_MODO5; // COUNT USED BY CONTROL THE MODE 5 TRANSITION START
int count_MODO7; // COUNT USED BY CONTROL THE MODE 7 TRANSITION START

int count_ROCK;
bool is_ROCK;

int count_PAPER;
bool is_PAPER;

int count_SCISSORS;
bool is_SCISSORS;

#define min_pos 0
#define max_pos 100
// twelve servo objects can be created on most boards

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 4.98; // Measured voltage of Ardunio 5V line
const float R_DIV = 20000.0; // Measured resistance of 3.3k resistor

//const float R_DIV = 20000.0;

// Upload the code, then try to adjust these values to more
// accurately calculate bend degree.
const float STRAIGHT_RESISTANCE = 5200; // resistance when straight
const float BEND_RESISTANCE = 2100; // resistance at 90 deg

int pos = 0;    // variable to store the servo position
bool end_game = 0;

void setup() {
  Serial.begin(9600); // serial used for testing.
  myservo1.attach(4);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(5);
  myservo3.attach(6);
  myservo4.attach(7);
  myservo5.attach(8);

   pinMode(FLEX1_PIN, INPUT);
   pinMode(FLEX2_PIN,INPUT);
   pinMode(FLEX3_PIN,INPUT);
   pinMode(FLEX4_PIN,INPUT);
   pinMode(FLEX5_PIN,INPUT);
   
   count_MODO1 = 0;
   count_MODO3 = 0;
   count_MODO5 = 0;
   count_MODO7 = 0;

   count_ROCK;
   modo = 0;

   is_ROCK = false;
   is_PAPER = false;
   is_SCISSORS = false;

}

void loop() {
int flex1ADC= analogRead(FLEX1_PIN);
        int flex2ADC = analogRead(FLEX2_PIN);
        int flex3ADC = analogRead(FLEX3_PIN);
        int flex4ADC = analogRead(FLEX4_PIN);
        int flex5ADC = analogRead(FLEX5_PIN);
        
        //SERVO 1
         float flexV = flex1ADC * VCC / 1023.0;
         float flexR = R_DIV * (VCC / flexV - 1.0);
         float angle1 = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,0, 90.0);

        // SERVO 2
         flexV = flex2ADC * VCC / 1023.0;
         flexR = R_DIV * (VCC / flexV - 1.0);
         float angle2 = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,0, 90.0);

        //SERVO 3
         flexV = flex3ADC * VCC / 1023.0;
         flexR = R_DIV * (VCC / flexV - 1.0);
         float angle3 = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,0, 90.0);

        //SERVO 4
         flexV = flex4ADC * VCC / 1023.0;
         flexR = R_DIV * (VCC / flexV - 1.0);
         float angle4 = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,0, 90.0);

        //SERVO 5
         flexV = flex5ADC * VCC / 1023.0;
         flexR = R_DIV * (VCC / flexV - 1.0);
         float angle5 = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE,0, 90.0);
    

if (modo == -1)
{
    myservo1.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
  }
////////////////////////////////////MODE 0 MIMIC MODE: THE HAND MIMICS THE GLOVE'S FINGER POSITION////////////////////////////////////////////////
  if (modo == 0) 
    {
        //ANALOG READ
        
     if(angle1 >= 20) myservo1.write(angle1+10) ;
         else myservo1.write(0);
         delay(50);
     if(angle2 >= 20) myservo2.write(angle2+10); 
         else myservo2.write(0);
         delay(50);
      if(angle3 >= 20) myservo3.write(angle3+10); 
         else myservo3.write(0);
         delay(50);
      if(angle4 >= 20) myservo4.write(angle4+10); 
         else myservo4.write(0);
         delay(50);
      if(angle5 >= 20) myservo5.write(angle5+10); 
         else myservo5.write(0);
         delay(50); 
     }

////////////////////////////////////MODE 1 TRANSITION TO PAPER ROCK SCISSORS WIN MODE////////////////////////////////////////////////
  if (modo == 1)
  {
    count_MODO1 = 0;
    modo = 2;  
    myservo1.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
    
    myservo1.write(100);
    delay(1000);
    
    myservo1.write(0);
    delay(1000);
    
    myservo2.write(100);
    delay(1000);
    myservo2.write(0);
    delay(1000);
    
    myservo3.write(100);
    delay(1000);
    myservo3.write(0);
    delay(1000);
    
    myservo4.write(100);
    delay(1000);
    myservo4.write(0);
    delay(1000);
    
    myservo5.write(100);
    delay(1000);
    
    myservo5.write(0);
    
    
    delay(2000);
    
    }
////////////////////////////////////MODE 2 PAPER ROCK SCISSORS WIN MODE////////////////////////////////////////////////
   if (modo == 2)
   {
   if (is_ROCK)
   { myservo1.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
    is_ROCK = false;
    modo = 0;
    }

   if (is_PAPER)
   { myservo1.write(100);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(100);
    delay(50);
    myservo5.write(100);
    delay(50);

    delay(2000);

  
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    
    is_PAPER = false;
    modo = 0;
    }
    
    if (is_SCISSORS)
    { 
    myservo2.write(100);
    delay(50);
    myservo3.write(100);
    delay(50);
    myservo4.write(100);
    delay(50);
    myservo5.write(100);
    delay(50);
    myservo1.write(100);
    delay(50);

    delay(2000);

    myservo1.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
    is_SCISSORS = false;
    modo = 0;
    }
   }
   
////////////////////////////////////MODE 3 TRANSITION TO PAPER ROCK SCISSORS LOSE MODE////////////////////////////////////////////////
   if (modo == 3)
   {
    count_MODO3 = 0;
    modo = 4;  
    myservo5.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo1.write(0);
    delay(50);
    
    myservo5.write(100);
    delay(1000);
    
    myservo5.write(0);
    delay(1000);
    
    myservo4.write(100);
    delay(1000);
    myservo4.write(0);
    delay(1000);
    
    myservo3.write(100);
    delay(1000);
    myservo3.write(0);
    delay(1000);
    
    myservo2.write(100);
    delay(1000);
    myservo2.write(0);
    delay(1000);
    
    myservo1.write(100);
    delay(1000);
    
    myservo1.write(0);
   }

////////////////////////////////////MODE 4 PAPER ROCK SCISSORS LOSE MODE////////////////////////////////////////////////
   if (modo == 4)
   {
   if (is_SCISSORS)
     { myservo1.write(0);
      delay(50);
      myservo2.write(0);
      delay(50);
      myservo3.write(0);
      delay(50);
      myservo4.write(0);
      delay(50);
      myservo5.write(0);
      delay(50);
      is_SCISSORS = false;
      modo = 0;
      }
  
     if (is_ROCK)
     { myservo1.write(0);
      delay(50);
      myservo2.write(100);
      delay(50);
      myservo3.write(100);
      delay(50);
      myservo4.write(0);
      delay(50);
      myservo5.write(0);
      delay(50);
  
      delay(2000);
  
    
      myservo2.write(0);
      delay(50);
      myservo3.write(0);
      delay(50);
      
      is_ROCK = false;
      modo = 0;
      }
      
      if (is_PAPER)
      { 
      myservo2.write(100);
      delay(50);
      myservo3.write(100);
      delay(50);
      myservo4.write(100);
      delay(50);
      myservo5.write(100);
      delay(50);
      myservo1.write(100);
      delay(50);
  
      delay(2000);
  
      myservo1.write(0);
      delay(50);
      myservo2.write(0);
      delay(50);
      myservo3.write(0);
      delay(50);
      myservo4.write(0);
      delay(50);
      myservo5.write(0);
      delay(50);
      is_PAPER = false;
      modo = 0;
     }
  }

////////////////////////////////////MODE 5 TRANSITION TO PAPER ROCK SCISSORS NORMAL MODE////////////////////////////////////////////////

if (modo == 5)
   {
    count_MODO3 = 0;
    modo = 6;  
    myservo5.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo1.write(0);
    delay(50);
    
    myservo5.write(100);
    delay(1000);
    
    myservo4.write(100);
    delay(1000);
    
    myservo5.write(0);
    delay(1000);
    
    
    myservo4.write(0);
    delay(1000);

    is_PAPER = false;
    is_ROCK = false;
    is_SCISSORS = false;
  
   }
////////////////////////////////////MODE 6 PAPER ROCK SCISSORS NORMAL MODE////////////////////////////////////////////////
if (modo = 6)
{
  int randpos =  random(3);
  Serial.println("Numero random: ");
  Serial.println(randpos);
  
  if (is_PAPER == true || is_ROCK == true || is_SCISSORS == true)
  {
    if (randpos == 0) //execute ROCK
    {
      Serial.println("Executant posicio ROCK ");
    myservo1.write(100);
    delay(50);
    myservo2.write(100);
    delay(50);
    myservo3.write(100);
    delay(50);
    myservo4.write(100);
    delay(50);
    myservo5.write(100);
    delay(50);
    delay(2000);
    Serial.println("Reiniciant posicio ");
    myservo1.write(0);
    delay(50);
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
    
    modo = 0;
    delay(2000);
      }

    if (randpos == 1) // execute SCISSORS
    {
      Serial.println("Executant posicio SCISSORS ");
      myservo1.write(0);
    delay(50);
    myservo2.write(100);
    delay(50);
    myservo3.write(100);
    delay(50);
    myservo4.write(0);
    delay(50);
    myservo5.write(0);
    delay(50);
    delay(2000);
    Serial.println("Reiniciant posicio ");
    myservo2.write(0);
    delay(50);
    myservo3.write(0);
    delay(50);

    modo = 0;
    delay(2000);
      }

    if (randpos == 2) // exeute PAPER
    {
      Serial.println("Executant posicio PAPER ");
      myservo1.write(0);
      delay(50);
      myservo2.write(0);
      delay(50);
      myservo3.write(0);
      delay(50);
      myservo4.write(0);
      delay(50);
      myservo5.write(0);
      delay(50);
      modo = 0;
      delay(2000);
    }
      is_SCISSORS = false;
      is_ROCK = false;
      is_PAPER = false;
    }
  }

////////////////////////////////////ANGLE DETECTION////////////////////////////////////////////////

    if (angle1 > 90 && angle2 < 10 && angle3 < 10 && angle4 < 10 && angle5 < 10 && modo != 1 && modo != 3 && modo != 5 ) count_MODO1 = count_MODO1+1;
         else count_MODO1 = 0;

    if (angle1 < 10 && angle2 > 90 && angle3 < 10 && angle4 < 10 && angle5 < 10 && modo != 1 && modo != 3 && modo != 5) count_MODO3 = count_MODO3+1;
         else count_MODO3 = 0;

    if (angle1 < 10 && angle2 < 10 && angle3 > 90 && angle4 < 10 && angle5 < 10 && modo != 1 && modo != 3 && modo != 5) count_MODO5 = count_MODO5+1;
         else count_MODO5 = 0;


            
    if (angle1 > 90 && angle2 > 90 && angle3 > 90 && angle4 > 90 && angle5 > 90 && (modo == 2 || modo == 4 || modo == 6)) count_ROCK = count_ROCK + 1;
         else count_ROCK = 0;

    if (angle1 < 10 && angle2 < 10 && angle3 < 10 && angle4 < 10 && angle5 < 10 && (modo == 2 || modo == 4 || modo == 6)) count_PAPER = count_PAPER + 1;
         else count_PAPER = 0;

    if (angle1 < 10 && angle2 > 90 && angle3 > 90 && angle4 < 10 && angle5 < 10 && (modo == 2 || modo == 4 || modo == 6)) count_SCISSORS = count_SCISSORS + 1;
         else count_SCISSORS = 0;


    if(count_ROCK >= 20) is_ROCK = true;
    if(count_PAPER >= 20) is_PAPER = true;
    if(count_SCISSORS >= 20) is_SCISSORS = true;
    Serial.println("executing mode : ");
    Serial.println(modo);




      
         
    if(count_MODO1 >= 20) modo = 1;
    if(count_MODO3 >= 20) modo = 3;
    if(count_MODO5 >= 20) modo = 5;
   // if(count_MODO7 >= 20) modo = 7;
    
    
    
    
  }
