// touchwheel0_test0.ino -- initial demonstration of touchwheel on Arduino, needs work still
// 2 Apr 2024 - @todbot / Tod Kurt

#include "TouchyTouch.h"

const int touch_pins[] = {11, 12, 13, };
const int touch_count = 3; 

TouchyTouch touches[touch_count];

/**
 * Given three touchio.TouchIn pads, compute wheel position 0-1
 * or return -1 if wheel is not pressed
 */
float wheel_pos() { 
  // compute raw percentages
  float a_pct = ((float)touches[0].raw_value - touches[0].threshold) / touches[0].threshold;
  float b_pct = ((float)touches[1].raw_value - touches[1].threshold) / touches[1].threshold;
  float c_pct = ((float)touches[2].raw_value - touches[2].threshold) / touches[2].threshold;
  Serial.printf("\t\t\t%+1.2f  %+1.2f  %+1.2f\n", a_pct, b_pct, c_pct);

  float offset = -0.333/2;  // physical design is rotated 1/2 a sector anti-clockwise

  float pos = -1;
  //cases when finger is touching two pads
  if( a_pct >= 0 and b_pct >= 0 ) {
      pos = 0 + 0.333 * (b_pct / (a_pct + b_pct));
  } 
  else if( b_pct >= 0 and c_pct >= 0 ) {
      pos = 0.333 + 0.333 * (c_pct / (b_pct + c_pct));
  }
  else if( c_pct >= 0 and a_pct >= 0 ) { 
      pos = 0.666 + 0.333 * (a_pct / (c_pct + a_pct));
  }
  // special cases when finger is just on a single pad.
  // these shouldn't be needed and create "deadzones" at these points
  // so surely there's a better solution
  else if( a_pct > 0 and b_pct <= 0 and c_pct <= 0 ) { 
      pos = 0;
  }
  else if( a_pct <= 0 and b_pct > 0 and c_pct <= 0 ) { 
      pos = 0.333;
  }
  else if( a_pct <= 0 and b_pct <= 0 and c_pct > 0 ) {
      pos = 0.666;
  }
  if( pos == -1 ) { // no touch 
    return -1;
  }
  // wrap pos around the 0-1 circle if offset puts it outside that range
  return fmod(pos + offset, 1);
}

void setup() {
  Serial.begin(115200);
  Serial.println("TouchyTouch touchwheel test0");

  pinMode(LED_BUILTIN, OUTPUT);

  // Touch buttons
  for (int i = 0; i < touch_count; i++) {
    touches[i].begin( touch_pins[i] );
  }

}

void loop() {
  for ( int i = 0; i < touch_count; i++) {
    touches[i].update();
  }

  // Serial.printf("raw/thresh %d/%d  %d/%d  %d/%d\n", 
  //                 touches[0].raw_value, touches[0].threshold,
  //                 touches[1].raw_value, touches[1].threshold,
  //                 touches[2].raw_value, touches[2].threshold);

  float pos = wheel_pos();
  Serial.printf("%ld: Pos: %.2f\n", millis(), pos);

  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
}
