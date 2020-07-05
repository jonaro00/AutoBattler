#include <Servo.h>

Servo arm1, arm2, arm3;

int arm1port = -1, arm1rest = -1, arm1untap = -1, arm1tap = -1;
int arm2port = -1, arm2rest = -1, arm2untap = -1, arm2tap = -1;
int arm3port = -1, arm3rest = -1, arm3untap = -1, arm3tap = -1;
int tapdelay = -1;

bool configCompleted = false;

void setup(){
  Serial.begin(9600);
  while(!Serial){
    ;
  }
  Serial.setTimeout(8);
  Serial.write("Ready");
}

void loop(){}

void serialEvent(){
  String serialData = Serial.readString();
  parseData(serialData);
}

void parseData(String data){
  String command;
  int comStart = 0;
  for(int i = 0; i < data.length(); i++){
    if(data.charAt(i) == ';'){
      command = data.substring(comStart, i);
      comStart = i+1;
      executeCommand(command);
    }
  }
}

void executeCommand(String command){
  if     (command.startsWith("S1:")) setarm1(command.substring(3).toInt());
  else if(command.startsWith("S2:")) setarm2(command.substring(3).toInt());
  else if(command.startsWith("S3:")) setarm3(command.substring(3).toInt());
  else if(command == "R1") restarm1();
  else if(command == "R2") restarm2();
  else if(command == "R3") restarm3();
  else if(command == "U1") untaparm1();
  else if(command == "U2") untaparm2();
  else if(command == "U3") untaparm3();
  else if(command == "T1") taparm1();
  else if(command == "T2") taparm2();
  else if(command == "T3") taparm3();
  else if(command.startsWith("CONF:")) parseConfig(command.substring(5));
}

void parseConfig(String conf){
  if(conf == "standard") conf = "A1P=5,A1R=0,A1U=10,A1T=20,A2P=6,A2R=0,A2U=10,A2T=20,A3P=7,A3R=0,A3U=10,A3T=20,TD=140,";
  int kvStart = 0;
  for(int i = 0; i < conf.length(); i++){
    if(conf.charAt(i) == ','){
      String kv = conf.substring(kvStart, i);
      kvStart = i+1;
      int j = kv.indexOf('=');
      String key = kv.substring(0, j);
      int val = kv.substring(j+1).toInt();
      if     (key == "A1P") arm1port  = val;
      else if(key == "A1R") arm1rest  = val;
      else if(key == "A1U") arm1untap = val;
      else if(key == "A1T") arm1tap   = val;
      else if(key == "A2P") arm2port  = val;
      else if(key == "A2R") arm2rest  = val;
      else if(key == "A2U") arm2untap = val;
      else if(key == "A2T") arm2tap   = val;
      else if(key == "A3P") arm3port  = val;
      else if(key == "A3R") arm3rest  = val;
      else if(key == "A3U") arm3untap = val;
      else if(key == "A3T") arm3tap   = val;
      else if(key == "TD")  tapdelay  = val;
    }
  }
  if(arm1port != -1 && arm1rest != -1 && arm1untap != -1 && arm1tap != -1 &&
     arm2port != -1 && arm2rest != -1 && arm2untap != -1 && arm2tap != -1 &&
     arm3port != -1 && arm3rest != -1 && arm3untap != -1 && arm3tap != -1 &&
     tapdelay != -1
     && configCompleted == false)
       configComplete();
}

void configComplete(){
  configCompleted = true;
  arm1.attach(arm1port);
  restarm1();
  arm2.attach(arm2port);
  restarm2();
  arm3.attach(arm3port);
  restarm3();
}

void setarm1(int deg){arm1.write(deg);}
void setarm2(int deg){arm2.write(deg);}
void setarm3(int deg){arm3.write(deg);}

void restarm1(){setarm1(arm1rest);}
void restarm2(){setarm2(arm2rest);}
void restarm3(){setarm3(arm3rest);}

void untaparm1(){setarm1(arm1untap);}
void untaparm2(){setarm2(arm2untap);}
void untaparm3(){setarm3(arm3untap);}

void taparm1(){setarm1(arm1tap);delay(tapdelay);untaparm1();}
void taparm2(){setarm2(arm2tap);delay(tapdelay);untaparm2();}
void taparm3(){setarm3(arm3tap);delay(tapdelay);untaparm3();}
