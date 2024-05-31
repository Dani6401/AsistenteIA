import speech_recognition as sr  # Para convertir el audio en texto
import pyttsx3  # Para la síntesis de voz 
import pywhatkit  # Para buscar videos en YouTube y enviar mensajes de WhatsApp
import datetime  # Para obtener la hora actual
import wikipedia  # Para buscar información en Wikipedia
import webbrowser  # Para realizar búsquedas en Google y abrir URLs
import requests  # Para obtener información del clima
import random  # Para seleccionar chistes aleatorios
import smtplib  # Para enviar correos electrónicos
import os  # Para abrir aplicaciones y buscar archivos en el ordenador
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Nombre del asistente virtual
name = 'elizabeth'

# Clave API de OpenWeatherMap 
weather_api_key = 'e382183c34a77f4839a11ea8c2f2f225'

# Credenciales de Gmail
email_user = 'djimenezh1@miumg.edu.gt'
email_password = '2]!m{q6q(6'

# Bandera para controlar el ciclo del programa
flag = 1

listener = sr.Recognizer()

engine = pyttsx3.init()

# Obtener voces y configurar la primera voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Configuración de la voz
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def talk(text):
    engine.say(text)
    engine.runAndWait()

# El programa recupera nuestra voz y la envía a otra función
def listen():
    global flag
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            
            if name in rec:
                rec = rec.replace(name, '')
                flag = run(rec)
            else:
                print(f"No se mencionó '{name}', no se ejecutará ninguna acción.")
    except:
        pass
    return flag

# Función para obtener el pronóstico del clima
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + weather_api_key + "&units=metric&lang=es"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        weather_info = f"El clima en {city} es {description} con una temperatura de {temperature} grados Celsius."
    else:
        weather_info = "No pude encontrar la información del clima para la ciudad solicitada."
    return weather_info

# Lista de chistes
jokes = [
    "¿Cómo se dice pañuelo en japonés? Saka-moko.",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
    "¿Qué le dice una iguana a su hermana gemela? Somos iguanitas.",
    "¿Por qué los elefantes no usan computadora? Porque le tienen miedo al ratón."
]

# Función para enviar correos electrónicos
def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, to_email, text)
        server.quit()
        talk("Correo enviado con éxito")
    except Exception as e:
        talk(f"Hubo un error al enviar el correo: {str(e)}")

# Todas las acciones que el asistente virtual puede hacer
def run(rec):
    global flag
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)


    elif 'investiga en wikipedia' in rec:
        talk('¿Qué quieres buscar en Wikipedia?')
        try:
            with sr.Microphone() as source:
                print("Escuchando...")
                voice = listener.listen(source)
                search_query = listener.recognize_google(voice, language='es-ES').lower()
            results = wikipedia.summary(search_query, sentences=1)
            talk(f"De acuerdo con Wikipedia, {results}")
            talk("Para tu comodidad, mostraré en pantalla los resultados.")
            webbrowser.open(f"https://es.wikipedia.org/wiki/{search_query.replace(' ', '_')}")
        except Exception as e:
            talk(f'Hubo un error al buscar en Wikipedia: {str(e)}')


    elif 'busca en google' in rec:
        search = rec.replace('busca en google', '')
        talk('Buscando en Google: ' + search)
        webbrowser.open(f"https://www.google.com/search?q={search}")


    elif 'whatsapp' in rec:
        try:
            talk('¿Qué mensaje quieres enviar?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                message = listener.recognize_google(voice, language='es-ES').lower()
            
            # Define directamente el número de teléfono al cual enviar el mensaje
            phone_number = '+50254244630'  # Cambia este número por el número al que deseas enviar el mensaje
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute + 1  # Enviará el mensaje 1 minuto después de la hora actual
            
            if minute >= 60:
                minute -= 60
                hour += 1

            print(f'Enviando mensaje a {phone_number} a las {hour}:{minute}')
            pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
            talk(f'Enviando mensaje a {phone_number}')
        except Exception as e:
            talk(f'Hubo un error al enviar el mensaje: {str(e)}')


    elif 'clima' in rec:
        talk('¿De qué ciudad quieres saber el clima?')
        try:
            with sr.Microphone() as source:
                voice = listener.listen(source)
                city = listener.recognize_google(voice, language='es-ES').lower()
            weather_info = get_weather(city)
            talk(weather_info)
        except Exception as e:
            talk(f'Hubo un error al obtener el clima: {str(e)}')

            
    elif 'película' in rec:
        if 'disney' in rec:
            talk('Abriendo Disney+')
            webbrowser.open("https://www.disneyplus.com")
        elif 'netflix' in rec:
            talk('Abriendo Netflix')
            webbrowser.open("https://www.netflix.com")
        elif 'hbo' in rec:
            talk('Abriendo HBO Max')
            webbrowser.open("https://www.hbomax.com")
        elif 'amazon' in rec:
            talk('Abriendo Amazon Prime Video')
            webbrowser.open("https://www.primevideo.com")
        else:
            talk('No reconozco esa plataforma de streaming.')


    elif 'chiste' in rec:
        joke = random.choice(jokes)
        talk(joke)


    elif 'correo' in rec:
        try:
            talk('¿A quién quieres enviar el correo?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                to_email = listener.recognize_google(voice, language='es-ES').lower()
            
            talk('¿Cuál es el asunto del correo?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                subject = listener.recognize_google(voice, language='es-ES').lower()
            
            talk('¿Qué mensaje quieres enviar?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                message = listener.recognize_google(voice, language='es-ES').lower()
            
            # Aquí deberías tener un diccionario de contactos o una manera de obtener el correo electrónico
            email_contacts = {
                'a Michelle': 'sdelcida2@miumg.edu.gt',
                'a Daniel': 'dsniel2046@gmail.com'
            }
            
            if to_email in email_contacts:
                to_email = email_contacts[to_email]
                send_email(to_email, subject, message)
            else:
                talk(f'No tengo el correo electrónico de {to_email}')
        except Exception as e:
            talk(f'Hubo un error al enviar el correo: {str(e)}')


    elif 'abre' in rec:
        # Reemplaza las aplicaciones y directorios con los que deseas trabajar
        if 'calculadora' in rec:
            os.system("calc")
        elif 'editor de texto' in rec:
            os.system("bloc de notas")
        elif 'navegador' in rec:
            os.system("Opera")
        else:
            talk('No reconozco esa aplicación.')


    elif 'archivo' in rec:
        try:
            talk('¿Qué archivo estás buscando?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                filename = listener.recognize_google(voice, language='es-ES').lower()
            
            # Reemplaza la ruta del directorio con el directorio donde deseas buscar archivos
            root_dir = "C:/Users/dsnie/Documents/TEST.txt"
            for root, dirs, files in os.walk(root_dir):
                if filename in files:
                    talk(f"El archivo {filename} fue encontrado en {root}")
                    break
            else:
                talk(f"No se encontró el archivo {filename}")

        except Exception as e:
            talk(f'Hubo un error al buscar el archivo: {str(e)}')


    elif 'adios' in rec: 
        flag = 0
        talk("Saliendo...")


    else:
        talk("Vuelve a intentarlo, no reconozco: " + rec)
    return flag

while flag:
    flag = listen()
