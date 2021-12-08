from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import io
import datetime


appbot = Flask(__name__)


@appbot.route("/sms", methods=["get", "post"])
def reply():
    with io.open("response2.csv", "a", encoding="utf-8")as f1:
        msgm = request.form.get("Body")
        num = request.form.get("From")
        num = num.replace("whatsapp:", "")
        dt = datetime.datetime.now().strftime("%y/%m/%d")
        data = f'{msgm},{num},{dt}\n'
        print(num)
        f1.write(data)
        resp = MessagingResponse()
        imagem = resp.message('Eee')
        imagem.media("http://921a82c4.ngrok.io/Users/me/Pictures/olga.jpeg")
        audio = resp.message()
        audio.media("http://921a82c4.ngrok.io/Users/me/Downloads/drive-download-20200515T184016Z-001/olga.mp3")
        return str(resp)


if __name__ == "__main__":
    appbot.run()
