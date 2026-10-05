import asyncio
import os
import requests
import json
import edge_tts

# 1. API Configuration: Inverted commas ke andar apni asli AQ Key paste karein
API_KEY = "AQ.Ab8RN6KKJefOkSfTRGHSXkWf95I-Nr_wIfY3iZ2agGjl-OfjzQ"

# 2. Voice TTS Setup (Lightweight larki ki awaz)
async def speak(text):
    print(f"\n[AI Agent Voice]: {text}")
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural", pitch="+12Hz")
    await communicate.save("speech.mp3")
    os.system("play-audio speech.mp3 > /dev/null 2>&1")

# 3. Personal Info & Samsung Native Tasks System Control
async def execute_system_command(command_text):
    command_clean = command_text.lower()
    
    # Call Mute Trigger (Lock Screen Bypass)
    if "mute" in command_clean or "silent" in command_clean:
        os.system("termux-volume stream notification 0")
        os.system("termux-volume stream music 0")
        os.system("termux-volume stream ring 0")
        return "Sir, mobile mute kar diya hai."
        
    # Gallery Image Opener
    elif "photo" in command_clean or "gallery" in command_clean or "araham" in command_clean:
        os.system("am start -a android.intent.action.VIEW -t image/*")
        return "Sir, gallery khol di hai. Aap Araham ki photo check kar sakte hain."
        
    # Net Switching Request Pop-up
    elif "net" in command_clean or "internet" in command_clean or "sim" in command_clean:
        os.system("termux-dialog confirm -t 'Network Switch' -i 'Allow SIM net data?'")
        return "Sir, screen par check karein maine permission popup bhej diya hai."
        
    # Personal Info Matching (Ahad, Ali, Abdul Sattar)
    elif "naam" in command_clean or "who am i" in command_clean:
        if "official" in command_clean or "azan" in command_clean:
            return "Sir, aapka official aur Azan ka naam Ali hai."
        elif "walid" in command_clean or "father" in command_clean:
            return "Aapke walid ka naam Abdul Sattar hai."
        else:
            return "Aapka naam Ahad hai, aur aapko Hello Memon kehte hain!"
            
    return None

# 4. Main Intelligent Brain Core Loop via Direct AQ Link Bypass
async def main():
    await speak("System is online. Hello Memon AI Agent Active.")
    
    url = "https://googleapis.com"
    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    while True:
        user_input = input("\nAap ka sawal ('exit' band karne ke liye): ")
        if user_input.strip().lower() == 'exit':
            await speak("Goodbye Sir! Allah Hafiz")
            break
            
        if not user_input.strip():
            continue

        # System hardware actions check first
        action_response = await execute_system_command(user_input)
        
        if action_response:
            await speak(action_response)
        else:
            # Forwards general knowledge questions to Gemini Cloud
            print("[System]: Thinking via Gemini API...")
            data = {"contents": [{"parts": [{"text": user_input}]}]}
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()
                    answer = result['candidates']['content']['parts']['text']
                else:
                    answer = f"Google Server Error code {response.status_code}"
            except Exception as e:
                answer = f"Connection error: {str(e)}"
                
            print(f"[Gemini]: {answer}")
            await speak(answer)

if __name__ == "__main__":
    asyncio.run(main())
