#include <GSM.h>

#define PINNUMBER "" //No es necesario PIN number

GSM gsmAccess;
GSM_SMS sms;

char remoteNumber[20] = "Ingresa numero celular 10 digitos";

char txtMsg[200]= "Temperatura Fuera de Rango";

char senderNumber[20];

void setup(){

  Serial.begin(9600);
  Serial.println("Mensaje enviado");

  boolean notConnected = true;

  while (notConnected){
    if (gsmAccess.begin(PINNUMBER)== GSM_READY)
    notConnected = false;
    else{
      Serial.println("No conectado");
      delay(1000);
    }
  }
  Serial.println("GSM inicializado");

}

void loop(){
  if (Serial.available()>0){
    if(Serial.readString()=="1")
    {
      delay(5000);
      sendSMS();
    }
  }
}

void sendSMS(){
 
  sms.beginSMS(remoteNumber);
  sms.print(txtMsg);
  
  sms.endSMS();

  Serial.println("\nCompleto\n");
}
