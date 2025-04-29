#include <Servo.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// === OLED Setup ===
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// === Sensor Pins ===
#define DHTPIN 2
#define DHTTYPE DHT11
const int moisturePin = A0;
const int servoPin = 9;

// === Objects ===
Servo myServo;
DHT dht(DHTPIN, DHTTYPE);

bool pumpOn = false;  // Track water pump state

void setup() {
  myServo.attach(servoPin);
  Serial.begin(9600);
  dht.begin();

  // === Initialize OLED ===
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("OLED not found"));
    while (true);  // Halt if OLED not found
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Loading...");
  display.display();
  delay(2000);
}

void loop() {
  // === Read sensors ===
  int sensorValue = analogRead(moisturePin);
  float moisturePercent = map(sensorValue, 1023, 0, 0, 100);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // === Servo & Pump Control ===
  if (moisturePercent < 30) {
    pumpOn = true;

    for (int pos = 0; pos <= 180; pos++) {
      myServo.write(pos);
      delay(15);
    }
    for (int pos = 180; pos >= 0; pos--) {
      myServo.write(pos);
      delay(15);
    }
  } else {
    pumpOn = false;
  }

  // === Serial Debugging ===
// Send data in CSV format for Python ML script
Serial.print(temperature);
Serial.print(",");
Serial.print(humidity);
Serial.print(",");
Serial.println(moisturePercent);



  // === Display on OLED ===
  display.clearDisplay();
  display.setCursor(0, 0);
  display.print("Temp: ");
  display.print(temperature);
  display.println(" C");

  display.print("Humidity: ");
  display.print(humidity);
  display.println(" %");

  display.print("Soil Moist: ");
  display.print(moisturePercent);
  display.println(" %");

  display.print("Water Pump: ");
  display.println(pumpOn ? "ON" : "OFF");
  String condition = "";
  display.display();
  delay(4000);
  // === Check if prediction from Python is available ===
if (Serial.available()) {
  String condition = Serial.readStringUntil('\n');

  // Print condition on OLED
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Plant Condition:");
  display.println(condition);
  display.display();
}


  delay(2000);  // Wait before next loop
}

