// frontend/src/audio/worklet/PCMProcessor.js
// AudioWorkletProcessor: resamples input -> 16kHz mono -> emits 512-sample Int16Array frames

class PCMProcessor extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [];
  }

  constructor(options) {
    super(options);

    this.targetSampleRate = 16000;
    this.frameSize = 512;
    this.outputChannels = 1;

    this.inputSampleRate = sampleRate;
    this.resampleRatio = this.inputSampleRate / this.targetSampleRate;

    this.inputBuffer = new Float32Array(0);
    this.outputBuffer = new Float32Array(this.frameSize);
    this.outputBufferPtr = 0;

    this.lastInputSample = 0;
    this.inputIndex = 0;

    this.port.onmessage = (e) => {
      if (e.data === "flush") {
        this.flush();
      }
    };
  }

  *resampleGenerator(inputChannel) {
    const inputLen = inputChannel.length;
    let inputIdx = this.inputIndex;

    while (inputIdx < inputLen) {
      const idx0 = Math.floor(inputIdx);
      const idx1 = Math.min(idx0 + 1, inputLen - 1);
      const frac = inputIdx - idx0;

      let sample;
      if (idx0 === inputLen - 1) {
        sample = inputChannel[idx0];
      } else {
        sample = inputChannel[idx0] * (1 - frac) + inputChannel[idx1] * frac;
      }

      yield sample;
      inputIdx += this.resampleRatio;
    }

    this.inputIndex = inputIdx - inputLen;
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (!input || input.length === 0) return true;

    const inputChannels = input.length;
    const inputLength = input[0].length;
    const monoInput = new Float32Array(inputLength);

    if (inputChannels === 1) {
      monoInput.set(input[0]);
    } else {
      for (let ch = 0; ch < inputChannels; ch++) {
        const chData = input[ch];
        for (let i = 0; i < inputLength; i++) {
          monoInput[i] += chData[i];
        }
      }
      for (let i = 0; i < inputLength; i++) {
        monoInput[i] /= inputChannels;
      }
    }

    const resampler = this.resampleGenerator(monoInput);

    for (const sample of resampler) {
      this.outputBuffer[this.outputBufferPtr++] = sample;

      if (this.outputBufferPtr === this.frameSize) {
        const int16Frame = new Int16Array(this.frameSize);
        for (let i = 0; i < this.frameSize; i++) {
          const clamped = Math.max(-1, Math.min(1, this.outputBuffer[i]));
          int16Frame[i] = clamped < 0 ? clamped * 0x8000 : clamped * 0x7FFF;
        }

        this.port.postMessage(int16Frame.buffer, [int16Frame.buffer]);
        this.outputBufferPtr = 0;
      }
    }

    return true;
  }

  flush() {
    if (this.outputBufferPtr > 0) {
      const int16Frame = new Int16Array(this.frameSize);
      for (let i = 0; i < this.outputBufferPtr; i++) {
        const clamped = Math.max(-1, Math.min(1, this.outputBuffer[i]));
        int16Frame[i] = clamped < 0 ? clamped * 0x8000 : clamped * 0x7FFF;
      }
      this.port.postMessage(int16Frame.buffer, [int16Frame.buffer]);
      this.outputBufferPtr = 0;
    }
  }
}

registerProcessor("pcm-processor", PCMProcessor);
