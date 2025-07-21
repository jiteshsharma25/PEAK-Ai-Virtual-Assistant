import os
import re
import sqlite3  
import traceback
import webbrowser
from hugchat import hugchat
from playsound import playsound
import eel
import requests
from engine.command import speak
import pywhatkit as kit
con=sqlite3.connect("Peak.db")
cursor=con.cursor()
def playassistantsound(): #sound create in start
    music_dir="web\\assests\\audio\\initialization.mp3"
    playsound(music_dir)
@eel.expose
def playmicsound():
    music="web\\assests\\audio\\micsound.mp3"
    playsound(music)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query=query.lower()
    app_name = query.strip()


    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def extract_yt_term(command):
    """More robust YouTube search term extraction"""
    patterns = [
        r'play\s+(.*?)\s+on\s+youtube',
        r'play\s+(.*?)\s+youtube',
        r'play\s+(.*?)$',
        r'could you play\s+(.*?)\s+on youtube'
    ]
    
    for pattern in patterns:
        if match := re.search(pattern, command, re.IGNORECASE):
            return match.group(1).strip()
    return None
def PlayYoutube(query):
    """Improved YouTube playback with better error feedback"""
    if not (search_term := extract_yt_term(query)):
        speak("Please say something like 'Play Despacito on YouTube'")
        return
    
    try:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    except Exception as e:
        speak("Failed to play the video. Please check your internet connection.")
        print(f"YouTube playback error: {e}")

def chatBot(query):
    """More robust chatbot with conversation management"""
    if not query.strip():
        return "Please provide a valid input"
    
    try:
        chatbot = hugchat.ChatBot(
            cookie_path=os.path.normpath("engine/cookies.json"),
            system_prompt="Respond concisely and helpfully."
        )
        response = chatbot.chat(query.lower())
        print(f"AI: {response}")
        speak(response)
        return response
    except Exception as e:
        error_msg = "Sorry, I'm having trouble connecting to the chatbot."
        print(f"Chatbot error: {e}\n{traceback.format_exc()}")
        speak(error_msg)
        return error_msg
def process_query(query):
    """Smart query router - REPLACE ONLY THIS FUNCTION"""
    query_lower = query.lower().strip()
    
    if ((" play " in f" {query_lower} " or "youtube play " in query_lower) 
        and "youtube" in query_lower
        and not any(word in query_lower for word in ["playful", "display", "playing"])):
        
        search_term = extract_yt_term(query)
        if search_term:
            PlayYoutube(query)
            return
    
    if query_lower.startswith('open '):
        openCommand(query)
        return
    
    
    chatBot(query) 
