#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "BluetoothSerial.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(115200);
  
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  display.clearDisplay();

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  // Display static text
  display.println("device active");
  display.display(); 
}

void loop() {
  if (Serial.available()) {
    char receivedChar = Serial.read();
    SerialBT.write(receivedChar);
    display.print(receivedChar);
    display.display(); 
  }
  if (SerialBT.available()) {
    char receivedChar = SerialBT.read();
    Serial.write(receivedChar);

    if (receivedChar == '*') {
      display.clearDisplay();
      display.setCursor(0, 10);
      display.display(); 
    }
    
    else if (receivedChar == '|'){
      display.println("");
    }

    else{
      display.print(receivedChar);
      display.display(); 
    }
  }
  delay(20);
}