#include "Keyboard.h"

void setup() {
  Keyboard.begin();
  
  // Esperar a que el PC reconozca el dispositivo
  delay(3000);

  // 1. Abrir Notepad
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(150);
  Keyboard.releaseAll();
  delay(500);
  Keyboard.print("notepad");
  Keyboard.write(KEY_RETURN);
  delay(1000);

  // 2. Demo de Velocidad: Contar del 1 al 500
  for (int i = 1; i <= 500; i++) {
    Keyboard.println(i); // Escribe el número y pulsa Enter automáticamente
    
    // Opcional: Puedes quitar o reducir este delay para máxima velocidad
    // delay(2); 
  }

  // 3. Mensaje final impactante
  Keyboard.println("--------------------------------");
  Keyboard.println("DEMO FINALIZADA.");
  Keyboard.println("Velocidad de escritura: ~1000 caracteres/seg.");
  
  Keyboard.end();
}

void loop() {
  // Nada aquí
}