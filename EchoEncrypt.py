import os
import wave
import argparse

parser = argparse.ArgumentParser(description="Hide a secret message in a WAV audio file.")
parser.add_argument('-f', required=True, help='Select Audio File (in .wav format)', dest='audiofile')
parser.add_argument('-m', required=True, help='Enter your Secret Message', dest='secretmsg')
parser.add_argument('-o', required=True, help='Output file path and name', dest='outputfile')
args = parser.parse_args()

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print("🎶 Hide Your Secret Message in WAV Audio File! 🎶")

def hide_message(audio_file, secret_msg, output_file):
    # Open the input audio file
    with wave.open(audio_file, 'rb') as wave_audio:
        num_frames = wave_audio.getnframes()
        frame_bytes = bytearray(list(wave_audio.readframes(num_frames)))

        # Prepare message with end signal (0b00000000)
        bits = [int(bit) for char in secret_msg for bit in format(ord(char), '08b')]
        end_signal = [0] * 8  # Signal end of message
        bits += end_signal  # Append end signal

        available_bits = num_frames

        if len(bits) > available_bits:
            print("💡 The message is too large to fit in the audio file.")
            print(f"📏 Available capacity: {available_bits} bits")
            print(f"📝 Your message size: {len(bits)} bits including end signal")
            return

        # Modify frame bytes with the message bits
        for i in range(len(bits)):
            frame_bytes[i] = (frame_bytes[i] & 254) | bits[i]  # Set LSB according to message bits

        with wave.open(output_file, 'wb') as out_audio:
            out_audio.setparams(wave_audio.getparams())
            out_audio.writeframes(bytes(frame_bytes))

    print("✅ Message hidden successfully in the audio file!")

# Main execution
clear_console()
banner()
try:
    hide_message(args.audiofile, args.secretmsg, args.outputfile)
except Exception as e:
    print("❌ Something went wrong! Please try again.")
    print(f"Error: {e}")
