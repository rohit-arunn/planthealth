import pickle
import pandas as pd
import serial
import time
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os

with open('plant_health_model.pkl', 'rb') as f:
    model = pickle.load(f)  

df = pd.read_csv('plant_conditions.csv')
X_full = df[['Temperature', 'Humidity', 'SoilMoisture']]
y_full = df['Condition']

y_pred_full = model.predict(X_full)

cm = confusion_matrix(y_full, y_pred_full)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)

if not os.path.exists('static'):
    os.makedirs('static')
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('static/confusion_matrix.png')
plt.close()



ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

moisture_data = deque(maxlen=10)  
time_data = deque(maxlen=10)
counter = 0

fig, ax = plt.subplots()
with open('sensor_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'temperature', 'humidity', 'moisture'])



def send_email(subject, body):
    sender_email = "ra.hitman10@gmail.com"
    receiver_email = "rohit.arun2021@vitstudent.ac.in" 
    app_password = "rllphbchrsviwcii"  

    # Email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📩 Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

last_condition = None

while True:
    line = ser.readline().decode().strip()
    if line:
        try:
            parts = line.split(',')
            if len(parts) == 3:
                temp = float(parts[0])
                humidity = float(parts[1])
                moisture = float(parts[2])

                
                with open('sensor_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now(), temp, humidity, moisture])

                X = pd.DataFrame([[temp, humidity, moisture]], columns=["Temperature", "Humidity", "SoilMoisture"])

                prediction = model.predict(X)[0]

               # print(f"Predicted condition: {prediction}")

                
                ser.write((str(prediction) + '\n').encode())

                bot_token = '8083538608:AAFTxMBH3THfyoWWczc1_g3IuefOfQRFgbA'
                chat_id = '1062316725'  

                # def send_telegram_message(message):
                #     url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                #     data = {'chat_id': chat_id, 'text': message}
                #     response = requests.post(url, data=data)
                #     return response

                # # Use after prediction
                # if prediction != "Healthy":
                #     alert = f"🚨 Plant Alert: Condition is {prediction}.\nPlease check your plant! 🌱"
                #     send_telegram_message(alert)
                if prediction != last_condition:
                    if prediction == 'Healthy':
                        warning_message = f"Your plant is healthy!"
                    else:
                        warning_message = f"⚠️ Alert: Your plant condition is '{prediction}'. Please check soil/moisture levels."
                    send_email("🚨 Plant Health Alert", warning_message)
                    last_condition = prediction
                
                # if prediction != "Healthy":
                #     warning_message = f"⚠️ Alert: Your plant condition is '{prediction}'. Please check soil/moisture levels."
                #     send_email("🚨 Plant Health Alert", warning_message)

                # ani = animation.FuncAnimation(fig, update, interval=1000)
                # plt.tight_layout()
                # plt.show()

                
                
        except Exception as e:
            print(f"Error: {e}")