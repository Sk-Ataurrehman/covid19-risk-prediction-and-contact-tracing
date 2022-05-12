from urllib.request import Request
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import numpy as np
import pickle
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)
mail = Mail(app) # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'somaiyawetrace@gmail.com'
app.config['MAIL_PASSWORD'] = 'wetrace123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/predict', methods=['POST'])
def predict():
    gender = request.form.get('gender')
    age = request.form.get('age')
    fever = request.form.get('fever')
    cough = request.form.get('cough')
    breath = request.form.get('breath')
    throat = request.form.get('throat')
    hoarseness = request.form.get('hoarseness')
    head = request.form.get('head')
    nose = request.form.get('nose')
    lose = request.form.get('lose')
    condition = request.form.get('condition')
    contact = request.form.get('contact')

    input_query = np.array([[age, fever, cough, breath,
                           throat, hoarseness, head, nose, lose, condition, contact]])
    print(input_query)

    result = model.predict(input_query)[0]
    print(request.form.get('name')+"\n"+request.form.get('email')+"\n"+request.form.get('phone'))
    if(str(result) == '1'):
        msg = Message(
                'Regarding a covid assessment report of your student',
                sender ='somaiyawetrace@gmail.com',
                recipients = ['shaikhataurrehman0@gmail.com']
               )
        msg.body = 'Dear sir, \nFrom the report generated from our application, a student is at high risk of Covid-19, the details of the student is given below:\nName: '+request.form.get("name")+'\nEmail: '+request.form.get("email")+'\nPhone: '+request.form.get('phone')
        mail.send(msg)

    return jsonify({'result': str(result)})


if __name__ == "__main__":
    app.run()
