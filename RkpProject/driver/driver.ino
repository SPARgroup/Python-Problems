int ins[] = {A0,A1,A2};
int outs[] = {8,9,10};
int offDelay = 500;
int loopTime = 10;
int states[] = {0, 0, 0};
int val = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i <3; i++){
    pinMode(ins[i], INPUT);
    pinMode(outs[i], OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < 3; i++){
    val = analogRead(ins[i]);

    if(val > 10){
      turnOn(i);
      states[i] = offDelay;
    }
  }

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
