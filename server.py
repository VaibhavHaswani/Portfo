from flask import render_template,Flask,request,redirect
import csv,os
from pathlib import Path
from email.message import EmailMessage
import smtplib
from string import Template

app=Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/response')
def response():
    return render_template('respo.html')

@app.route('/submit_data',methods=['POST'])
def submit_data():
    if request.method=='POST':
        data=request.form.to_dict()
        write_to_csv(data)
        mail(data['contactName'],data['contactEmail'])
        return redirect('/response#contact')
    else:
        return "Something went wrong! Try Again"

def write_to_file(data):
    with open('database.txt') as f:
        index = len(f.readlines())
    db = open('database.txt', 'a')
    db.write(
        f"{index + 1}) Name:{data['contactName']} , email:{data['contactEmail']} , subject:{data['contactSubject']} , message:{data['contactMessage']}")
    db.close()

def write_to_csv(data):
    with open('database.csv','a',newline='') as csvf:
        fields=['contactName','contactEmail','contactSubject','contactMessage']
        wtr=csv.DictWriter(csvf,fields)
        if os.path.getsize('database.csv') == 0:
            wtr.writeheader()
        wtr.writerow(data)

def mail(name,id):
    htm=Template(Path('templates/email.html').read_text())
    email=EmailMessage()
    email['from']="VAIBHAV HASWANI~ PORTFOLIO"
    email['to']=id
    email['subject']='THANKS! FOR CONNECTING'
    email.set_content(htm.substitute({'user':name}),'html')
    with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('portfo.vaibhavhaswani@gmail.com','$#@!portfo!@#$')
        smtp.send_message(email)


if __name__=="__main__":
    app.run()


