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
engine.setProperty('voice', voices[1].id)  # 0 for male; 1 for female

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
                    if "jack" in text.lower():
                        request = text.lower().split("jack")[1]
                        sleeping = False
                        print("AI: Hi, there, how can I help?")
                        speak_text("Hi, there, how can I help?")
                        continue
                    else:
                        continue
                else:
                    request = text.lower()

                    if "that's all" in request:
                        print("AI: Bye now.")
                        speak_text("Bye now.")
                        sleeping = True
                        continue

                    if "jack" in request:
                        request = request.split("jack")[1]

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
