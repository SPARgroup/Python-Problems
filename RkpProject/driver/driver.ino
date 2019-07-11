int ins[] = {A0,A1,A2};
int outs[] = {8,9,10};
int warningLight = 7;
int offDelay = 500;
int loopTime = 10;
int states[] = {0, 0, 0};
int val = 0;
int times[] = {0, 0, 0};
float L = 20.0;
float maxSpeed = 40.0;
int warningDelay = 3000;
int curr = 0;
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i <3; i++){
    pinMode(ins[i], INPUT);
    pinMode(warningLight, OUTPUT);
    pinMode(outs[i], OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < 3; i++){
    val = analogRead(ins[i]);

    if(val > 40){
      turnOn(i);
      times[i] += loopTime;
//      Serial.print(times[i]);
//      Serial.print("\n");
      states[i] = offDelay;
    }
    else{
      //pin is off
      if(times[i] >= loopTime){
        //pin was just turned off
        float T = (float)times[i]/ 1000;
        float s = L/T;
        times[i] = 0;
       
        if (s > maxSpeed){
          Serial.print("SPEED EXCEEDED ");
//          Serial.print(s);
//          Serial.print(" ");
//          Serial.print(T);
//          Serial.print("\n");
          turnOn(warningLight);
          curr = warningDelay;
        }
      }
    }
  }

  if (curr <= 0){
    turnOff(warningLight);
  }
  else{
     curr -= loopTime;
  }
 
//  Serial.print(curr);
//  Serial.print("\n"); 
  for (int j = 0; j < 3; j++){
    if(states[j] <= 0){
      turnOff(j);
    }
    else{
      states[j] -= loopTime;
    }
  }

  delay(loopTime);
}

void turnOn(int index){
  digitalWrite(outs[index], HIGH);
}

void turnOff(int index){
  digitalWrite(outs[index], LOW);
}
