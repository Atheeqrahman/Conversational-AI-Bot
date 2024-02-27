import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from datetime import date

# Set up Google Gemini API key
genai.configure(api_key="AIzaSyD1bWsTKwHwUNhvyFzI5tdM-InXf7FGJJ8")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 190)  # speaking rate
voices = engine.getProperty('voices')
# Selecting a male voice
engine.setProperty('voice', voices[0].id)  # 0 for male; 1 for female
# Adjusting pitch and volume for a bit of bass
engine.setProperty('pitch', 50)  # Adjust pitch (50 is the default)
engine.setProperty('volume', 0.9)  # Adjust volume (0 to 1, 1 is the default)

# Initialize Google Gemini model
model = genai.GenerativeModel('gemini-pro')


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400
    sleeping = True

    while True:
        with mic as source1:
            rec.adjust_for_ambient_noise(source1, duration=0.5)
            print("Listening ...")

            try:
                audio = rec.listen(source1, timeout=10, phrase_time_limit=15)
                text = rec.recognize_google(audio)

                print("You:", text)

                if sleeping:
                    if "gopal" in text.lower():  # Changed wake-up phrase here
                        request = text.lower().split("gopal")[1]  # Adjust for the new wake-up phrase
                        sleeping = False
                        print("AI: Sollu Mamae")
                        speak_text("Sollu Mamae?")
                        continue
                    else:
                        continue
                else:
                    request = text.lower()

                    if "that's all" in request:
                        print("AI: Tata Mamae")
                        speak_text("Ta ta Mamae")
                        sleeping = True
                        continue

                    if "gopal" in request:  # Changed wake-up phrase here
                        request = request.split("gopal")[1]  # Adjust for the new wake-up phrase

                print("AI:", end=' ')
                response = model.generate_content(request)
                response_text = response.text  # Extract text content from response object
                print(response_text)  # Print the extracted text content
                speak_text(response_text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except Exception as e:
                print("An error occurred:", e)


if __name__ == "__main__":
    main()
