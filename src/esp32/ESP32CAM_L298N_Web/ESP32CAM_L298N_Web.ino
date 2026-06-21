#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiUdp.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define CAMERA_MODEL_AI_THINKER

#define LED   4
#define RXD2 14
#define TXD2 13

void CameraWebServer_init();
void WheelAct(int speed_R, int speed_L, int nLf, int nLb, int nRf, int nRb);

WiFiServer server(100);

WiFiUDP udp;
const int UDP_PORT = 4210;

const unsigned long UDP_TIMEOUT_MS = 500;
unsigned long lastUdpCommandTime = 0;

extern int gpLb = 14;  // Left 1
extern int gpLf = 13;  // Left 2
extern int gpRb = 33;  // Right 1
extern int gpRf = 15;  // Right 2
extern int gpLed = 4;  // Light
extern int ENR = 2;
extern int ENL = 12;

void initMotors()
{
  pinMode(gpLb, OUTPUT);
  pinMode(gpLf, OUTPUT);
  pinMode(gpRb, OUTPUT);
  pinMode(gpRf, OUTPUT);
  pinMode(gpLed, OUTPUT);
  pinMode(ENR, OUTPUT);
  pinMode(ENL, OUTPUT);

  ledcAttach(ENR, 5000, 8);
  ledcAttach(ENL, 5000, 8);

  ledcWrite(ENR, 0);
  ledcWrite(ENL, 0);

  digitalWrite(gpLf, LOW);
  digitalWrite(gpLb, LOW);
  digitalWrite(gpRf, LOW);
  digitalWrite(gpRb, LOW);
}

void stopMotors()
{
  WheelAct(0, 0, LOW, LOW, LOW, LOW);
}

void driveDifferential(int linear, int angular)
{
  int left = linear - angular;
  int right = linear + angular;

  left = constrain(left, -255, 255);
  right = constrain(right, -255, 255);

  int speedLeft = abs(left);
  int speedRight = abs(right);

  int leftForward = LOW;
  int leftBackward = LOW;
  int rightForward = LOW;
  int rightBackward = LOW;

  if (left > 0) {
    leftForward = HIGH;
    leftBackward = LOW;
  } else if (left < 0) {
    leftForward = LOW;
    leftBackward = HIGH;
  }

  if (right > 0) {
    rightForward = HIGH;
    rightBackward = LOW;
  } else if (right < 0) {
    rightForward = LOW;
    rightBackward = HIGH;
  }

  WheelAct(
    speedRight,
    speedLeft,
    leftForward,
    leftBackward,
    rightForward,
    rightBackward
  );
}

bool parseUdpCommand(char *packet, int &linear, int &angular, int &flash)
{
  int parsed = sscanf(packet, "V:%d,W:%d,F:%d", &linear, &angular, &flash);
  return parsed == 3;
}

void handleUdpControl()
{
  char packet[80];

  int packetSize = udp.parsePacket();

  if (!packetSize) {
    return;
  }

  int len = udp.read(packet, sizeof(packet) - 1);
  packet[len] = '\0';

  int linear = 0;
  int angular = 0;
  int flash = 0;

  if (parseUdpCommand(packet, linear, angular, flash)) {
    linear = constrain(linear, -255, 255);
    angular = constrain(angular, -255, 255);
    flash = constrain(flash, 0, 255);

    driveDifferential(linear, angular);
    ledcWrite(gpLed, flash);

    lastUdpCommandTime = millis();
  }
}

void setup()
{
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
  Serial.setDebugOutput(false);

  Serial.println();
  Serial.println("Starting ESP32-CAM robot...");

  CameraWebServer_init();

  initMotors();

  ledcAttach(gpLed, 5000, 8);

  server.begin();

  udp.begin(UDP_PORT);

  Serial.print("UDP control port: ");
  Serial.println(UDP_PORT);

  Serial.print("Robot IP: ");
  Serial.println(WiFi.softAPIP());

  for (int i = 0; i < 5; i++)
  {
    ledcWrite(gpLed, 10);
    delay(50);
    ledcWrite(gpLed, 0);
    delay(50);
  }

  stopMotors();
  lastUdpCommandTime = millis();
}

void loop()
{
  handleUdpControl();

  if (millis() - lastUdpCommandTime > UDP_TIMEOUT_MS) {
    stopMotors();
  }
}