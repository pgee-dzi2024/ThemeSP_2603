// Дефинираме пина, към който е свързано релето
const int relayPin = 8; 

// Променлива, която пази текущото състояние (за да можем да го връщаме при заявка)
int relayState = LOW; 

void setup() {
  // Настройваме пина на релето като изход
  pinMode(relayPin, OUTPUT);
  
  // Гарантираме, че при рестарт на Arduino, релето е изключено
  digitalWrite(relayPin, LOW); 
  
  // Стартираме серийната комуникация със скорост 9600 бода
  Serial.begin(9600);
  
  // Изчакваме малко портът да се инициализира
  delay(100);
  Serial.println("SYSTEM:READY");
}

void loop() {
  // Проверяваме дали има получени данни по серийния порт
  if (Serial.available() > 0) {
    
    // Четем един символ от буфера
    char command = Serial.read();

    // Обработваме командата
    if (command == '1') {
      digitalWrite(relayPin, HIGH);
      relayState = HIGH;
      Serial.println("STATUS:ON"); // Връщаме потвърждение към Python
      
    } else if (command == '0') {
      digitalWrite(relayPin, LOW);
      relayState = LOW;
      Serial.println("STATUS:OFF"); // Връщаме потвърждение към Python
      
    } else if (command == '?') {
       // Връщаме текущия статус без да го променяме
       Serial.print("STATUS:");
       Serial.println(relayState == HIGH ? "ON" : "OFF");
    }
    // Забележка: Всички други символи (като празни интервали или нови редове)
    // ще бъдат игнорирани, което прави кода по-устойчив на грешки.
  }
}