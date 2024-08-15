#
# asks AT (lm) to generate a compliment, the answer ki_audio.txt is read aloud by piper 
#
import requests
import json
import subprocess
import argparse

url = "xxx:4891/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant. Du antwortest immer auf Deutsch in der dritten Person und sprich sie mit ihrrem Namen Maarsia an. Halte die Antwort kurz und benutze keine Smilies oder Emojis. Antworte immer in einem einzigen kurzen Satz und wiederhole dich nicht. Verzichte auf Höflichkeitsfloskeln."},
        {"role": "user", "content": "Mache meiner Frau ein Kompliment."}
    ],
    "temperature": 0.7,
    "stream": False
}


txtoutput_path = '/tmp/ki_audio.txt'
mp3output_path = '/tmp/ki_audio.mp3'
model_path = '/home/pi/piper/de_DE-thorsten-high.onnx'
piper_path = '/home/pi/piper/piper'

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # success?
    if response.status_code == 200:
        response_data = response.json()
        
        content = response_data['choices'][0]['message']['content'].strip().replace('<|im_end|>', '')

        
        with open(txtoutput_path, 'w') as file:
            file.write(content)
            
        print(f"Antwort erfolgreich in {txtoutput_path} gespeichert.")

         # Lesen des Inhalts der Datei
        with open(txtoutput_path, 'r') as file:
            file_content = file.read()
            
        
        # Ausführen des Piper-Befehls mit dem Inhalt der Datei
        piper_command = [
            piper_path,
            "-m", model_path,
            "-f", mp3output_path
        ]
        subprocess.run(piper_command, input=file_content, text=True, check=True)

        # Abspielen der MP3-Datei
        aplay_command = ["aplay", mp3output_path]
        subprocess.run(aplay_command, check=True)
        
    else:
        print(f"Fehler: {response.status_code} - {response.text}")

except requests.RequestException as e:
    print(f"Anfragefehler: {e}")
except subprocess.CalledProcessError as e:
    print(f"Fehler beim Ausführen des Befehls: {e}")
