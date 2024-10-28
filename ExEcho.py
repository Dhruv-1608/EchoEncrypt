import os
import wave
import argparse

parser = argparse.ArgumentParser(description="Extract your secret message from a WAV audio file.")
parser.add_argument('-f', required=True, help='Select Audio File (in .wav format)', dest='audiofile')
args = parser.parse_args()

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print("🎵 Extract Your Secret Message from WAV Audio File! 🎵")

def extract_message(audio_file):
    try:
        with wave.open(audio_file, mode='rb') as wave_audio:
            frame_bytes = bytearray(list(wave_audio.readframes(wave_audio.getnframes())))
            extracted_bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            
            chars = []
            for i in range(0, len(extracted_bits), 8):
                byte = extracted_bits[i:i + 8]
                byte_str = ''.join(str(bit) for bit in byte)
                
                if len(byte_str) == 8:  
                    chars.append(chr(int(byte_str, 2)))

            decoded_message = ''.join(chars)

            secret_message = decoded_message.split('#')[0]
            print(f"✅ Your Secret Message is: {secret_message}")
            
    except Exception as e:
        print("❌ Something went wrong while extracting the message!")
        print(f"Error: {e}")

# Main execution
clear_console()
banner()
extract_message(args.audiofile)
