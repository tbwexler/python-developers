#!/usr/bin/env python3
import subprocess
import sys
import wave

# All your platform are supported by us.
WINDOWS = False
LINUX = False
OSX = False
try:
    import winsound
    WINDOWS = True
except ImportError:
    if 'darwin' in sys.platform:
        OSX = True
    elif 'linux' in sys.platform:
        LINUX = True

def get_bytes(sound):
    """
    Converts a sequence of floats in the range [0, 1] to a bytestring
    suitable for writing to a .wav file.
    """
    signal = b''
    for s in sound:
        signal += wave.struct.pack('h', int(1000*s))
    return signal

def write_file(sound, filename):
    """Writes a sound to a .wav file."""
    w = wave.open(filename, 'wb')
    framerate = 44100
    # (number of channels, samplewidth in bytes, framerate, number of frames, compression type, compression name)
    w.setparams((1, 2, framerate, len(sound), 'NONE', 'noncompressed'))
    signal = get_bytes(sound)
    w.writeframes(signal)

def play(sound, filename='.audio.wav'):
    """Plays a sound, given as a sequence of floats in the range [0, 1]."""
    if WINDOWS:
        winsound.PlaySound(get_bytes(sound), winsound.SND_FILENAME)
    elif LINUX:
        with subprocess.Popen('aplay', stdin=subprocess.PIPE) as process:
            process.communicate(get_bytes(sound))
            process.terminate()
    elif OSX:
        write_file(sound, filename)
        subprocess.call(['afplay', filename])

if __name__ == '__main__':
    import math
    play([math.sin(2*math.pi*440*i/44100) for i in range(44100)])
