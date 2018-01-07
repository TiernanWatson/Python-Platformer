int pin_left = 8;
int pin_up = 6;
int pin_right = 4;
int pin_light = A0;

void setup() {
  Serial.begin(9600);
  pinMode(pin_left, INPUT);
  pinMode(pin_up, INPUT);
  pinMode(pin_right, INPUT);
}

void loop() {
  int right = digitalRead(pin_right);
  int left = digitalRead(pin_left);
  int up = digitalRead(pin_up);
  int light = map(analogRead(pin_light), 0, 1023, 0, 9);
  Serial.println(String(right) + String(left) + String(up) + String(light));
}
