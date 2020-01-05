#include "arduinoFFT.h"
#include <I2S.h>
#include "wiring_private.h"

#define SAMPLES 1024             //Must be a power of 2
#define SAMPLING_FREQUENCY 8192 //Hz, must be less than 10000 due to ADC

arduinoFFT FFT = arduinoFFT();

const uint8_t mbed_pin = 8;
uint8_t noise_status = 0;

uint16_t sampling_period_us;

int MicSample = 0;
double vReal[SAMPLES];
double vImag[SAMPLES];

uint8_t view_graph = 0;
uint startMil = 0;

void MeasureMillis(){
  Serial.print(" - ");
  Serial.print(millis()-startMil);
  Serial.println("millis");
  startMil= millis();
}

void GetSamples(){
  for(uint32_t i=0; i<SAMPLES; ){
    while(1){
      MicSample = I2S.read();
      if(MicSample!=0 && MicSample!=-1) break;
    }
    i++;

    // convert to 18 bit signed
    MicSample >>= 16;
    vReal[i] = MicSample;
    vImag[i] = 0;
  }
}

void setup() {
  Serial.begin(115200);
  // Serial.begin(115200);
  // while (!Serial) {
  //   ; // wait for serial port to connect. Needed for native USB port only
  // }
  delay(500);
  Serial.println("Device Init");
  // Serial1.begin(115200);

  pinMode(mbed_pin, OUTPUT);
  digitalWrite(mbed_pin, LOW);

  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY));

  // start I2S at 16 kHz with 32-bits per sample
  if (!I2S.begin(I2S_PHILIPS_MODE, 16000, 32)) {
    while (1){
      Serial.println("Failed to initialize I2S!");
      delay(500);
    }
  }else{
		Serial.println("I2S initialized!");
	}
}

void loop() {
  view_graph = 1;

   GetSamples();  // 63 millis

  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);  // 119 millis
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);  // 388 millis
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);  // 57 millis
  double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
  // Serial.print("Peak: ");
  // Serial.println(peak);     //Print out what frequency is the most dominant.

  int count = 0;
  // Serial.println("24000");
  for(int i=0; i<(SAMPLES/2); i++){
    /*View all these three lines in serial terminal to see which frequencies has which amplitudes*/
    
    // Serial.print((i * 1.0 * SAMPLING_FREQUENCY) / SAMPLES, 1);
    // Serial.print(" ");
    if(view_graph){
      Serial.println(vReal[i], 1);    //View only this line in serial plotter to visualize the bins
    }

    if( 100<=i && 3500<=vReal[i]){
      count++;
    }
  }
  // Serial.println("16000");
  if(!view_graph){
    // Serial.print("Count: ");
    // Serial.println(count);
  }

  // delay(1000);

  if(count>=60){
    if(!view_graph){
      Serial.println("DETECTED!");
      digitalWrite(mbed_pin, HIGH);
      delay(200);
      digitalWrite(mbed_pin, LOW);
      noise_status=0;
    }
  }else{
    // Serial.println("");
  }
}
