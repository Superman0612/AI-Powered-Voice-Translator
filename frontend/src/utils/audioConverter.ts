/**
 * Utility to convert browser-captured audio (WebM, Ogg, MP4, etc.)
 * into standard 16kHz mono 16-bit PCM WAV.
 */
export async function convertBlobToWav(blob: Blob, targetSampleRate = 16000): Promise<Blob> {
  // If the browser already provided WAV, return directly
  if (blob.type === 'audio/wav' || blob.type === 'audio/x-wav') {
    return blob;
  }

  const arrayBuffer = await blob.arrayBuffer();
  const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
  if (!AudioContextClass) {
    return blob;
  }

  const audioContext = new AudioContextClass();

  try {
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    // Resample to 16 kHz Mono using OfflineAudioContext
    const numberOfChannels = 1;
    const duration = audioBuffer.duration;
    const totalSamples = Math.max(1, Math.ceil(duration * targetSampleRate));

    const offlineContext = new OfflineAudioContext(
      numberOfChannels,
      totalSamples,
      targetSampleRate
    );

    const source = offlineContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(offlineContext.destination);
    source.start(0);

    const renderedBuffer = await offlineContext.startRendering();
    return encodeWav(renderedBuffer);
  } catch (error) {
    console.warn("Failed to convert audio to WAV via Web Audio API, falling back to original blob:", error);
    return blob;
  } finally {
    try {
      await audioContext.close();
    } catch {
      // ignore
    }
  }
}

/**
 * Encodes an AudioBuffer into a RIFF/WAVE formatted 16-bit linear PCM Blob.
 */
function encodeWav(buffer: AudioBuffer): Blob {
  const numChannels = buffer.numberOfChannels;
  const sampleRate = buffer.sampleRate;
  const bitDepth = 16;
  const bytesPerSample = bitDepth / 8;
  const blockAlign = numChannels * bytesPerSample;

  const channelData = buffer.getChannelData(0); // mono
  const samplesCount = channelData.length;
  const dataByteLength = samplesCount * bytesPerSample;
  const totalBufferSize = 44 + dataByteLength;

  const arrayBuffer = new ArrayBuffer(totalBufferSize);
  const view = new DataView(arrayBuffer);

  // RIFF header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + dataByteLength, true);
  writeString(view, 8, 'WAVE');

  // fmt subchunk
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true); // Subchunk1Size (16 for PCM)
  view.setUint16(20, 1, true); // AudioFormat (1 = PCM)
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * blockAlign, true); // ByteRate
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, bitDepth, true);

  // data subchunk
  writeString(view, 36, 'data');
  view.setUint32(40, dataByteLength, true);

  // Write 16-bit PCM samples
  let offset = 44;
  for (let i = 0; i < samplesCount; i++) {
    const s = Math.max(-1, Math.min(1, channelData[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    offset += 2;
  }

  return new Blob([view], { type: 'audio/wav' });
}

function writeString(view: DataView, offset: number, str: string) {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i));
  }
}
