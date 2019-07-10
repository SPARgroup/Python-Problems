/*

*/

int ins[] = {A0, A1, A2};
int outs[] = {8, 9, 13};
int states[] = {0, 0, 0};
int offdelay = 500;
int loopTime = 10;
int vals[3] = {0};
int val = 0;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    pinMode(ins[i], INPUT);
    pinMode(outs[i], OUTPUT);
  }
}

void loop() {
  //delay(loopTime);
  for (int i = 0; i < 3; i++) {
    //read input
    val = analogRead(ins[i]);
    if (i == 1){
      Serial.print(val);
    }
    
    //Serial.print(ins[i]);
    if (val > 200) {     
      turnOn(i);
      states[i] = offdelay;
    }
    else{
      turnOff(i);     
   }
  }


  //delay(loopTime);
//  for (int j = 0; j < 3; j++) {
//    states[j] -= loopTime;
//    if (states[j] <= 0) {
//      turnOff(j);
//    }
//  }
//  for (int k = 0; k < 3; k++){
//    turnOff(k);
//  }
}

void turnOn(int index) {
  digitalWrite(outs[index], HIGH);
}

void turnOff(int index) {
  digitalWrite(outs[index], LOW);
}
