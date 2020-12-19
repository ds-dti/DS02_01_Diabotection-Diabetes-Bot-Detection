# from flask import Flask

import pandas as pd
# import pickle
from flask import Flask, render_template, json, request, jsonify,abort, redirect, url_for, make_response
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import json
import numpy as np


application = Flask(__name__)
app = Flask(__name__)

# create model pipeline
df = pd.read_csv('https://raw.githubusercontent.com/superizqi/Digital-Talent-Incubator-Telkom/master/data/diabetes.csv')
df[['Glucose','BloodPressure','SkinThickness','BMI']] = df[['Glucose','BloodPressure','SkinThickness','BMI']].replace(0,np.NaN)

df.loc[(df['Outcome'] == 0 ) & (df['Glucose'].isnull()), 'Glucose'] = 107
df.loc[(df['Outcome'] == 1 ) & (df['Glucose'].isnull()), 'Glucose'] = 140
df.loc[(df['Outcome'] == 0 ) & (df['BloodPressure'].isnull()), 'BloodPressure'] = 70
df.loc[(df['Outcome'] == 1 ) & (df['BloodPressure'].isnull()), 'BloodPressure'] = 74.5
df.loc[(df['Outcome'] == 0 ) & (df['SkinThickness'].isnull()), 'SkinThickness'] = 27
df.loc[(df['Outcome'] == 1 ) & (df['SkinThickness'].isnull()), 'SkinThickness'] = 32
df.loc[(df['Outcome'] == 0 ) & (df['BMI'].isnull()), 'BMI'] = 30.1
df.loc[(df['Outcome'] == 1 ) & (df['BMI'].isnull()), 'BMI'] = 34.3

x = df.drop(['Outcome','Insulin','DiabetesPedigreeFunction'], axis=1)
y = df['Outcome']
# mdl = KNeighborsClassifier(n_neighbors=7)
# model = Pipeline([('scaler', StandardScaler()), ('mdl', mdl)])
# model.fit(x, y)
# pickle.dump(model, open('model.pkl','wb'))
# model = pickle.load(open('model.pkl','rb'))

def personal_predict(preg,bmi,age):
    mdl_ = KNeighborsClassifier(n_neighbors=7)
    model_ = Pipeline([('scaler', StandardScaler()), ('mdl', mdl_)])
    x = df[['Pregnancies','BMI','Age']]
    y = df['Outcome']
    model_.fit(x, y)
    x_pred = [preg,bmi,age]
    return model_.predict([x_pred,x_pred])[0]

def medical_predict(preg,glu,blp,skn,bmi,age):
    rfo = RandomForestClassifier(max_depth= 15, min_samples_leaf= 5,
                             min_samples_split= 15, n_estimators= 100,random_state=260)
    model = Pipeline([('scaler', StandardScaler()), ('mdl', rfo)])
    model.fit(x, y)
    x_pred = [preg,glu,blp,skn,bmi,age]
    return model.predict([x_pred,x_pred])[0]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/medical', methods=['GET', 'POST'])
def medical():
    if request.method == 'POST':
        # x_pred = [preg,glu,blp,skn,bni,age]
        preg = int(request.form.get('pregnancies'))
        glu = int(request.form.get('glucose'))
        blp = int(request.form.get('bloodpressure'))
        skn = int(request.form.get('skinthickness'))
        try:
            weight = int(request.form.get('weight'))
            height = int(request.form.get('height'))
            bmi = weight/((height/100)**2)
        except:
            bmi=0
        age = int(request.form.get('age'))
        pre = medical_predict(preg,glu,blp,skn,bmi,age)
        # return f'{f}'
        return render_template('medical.html', name=pre)
    return render_template('medical.html')

@app.route('/personal', methods=['GET', 'POST'])
def personal():
    if request.method == 'POST':
        preg = int(request.form.get('pregnancies'))
        try:
            weight = int(request.form.get('weight'))
            height = int(request.form.get('height'))
            bmi = weight/((height/100)**2)
        except:
            bmi=0
        age = int(request.form.get('age'))
        pre = personal_predict(preg,bmi,age)
        # pre = predict_diabetes(a,b,c,d,e,f,g,h)
        # pre = 0
        # return f'{f}'
        return render_template('personal.html', name=pre)
    return render_template('personal.html')

# /medical_api?pregnancies=10&glucose=10&bloodpressure=10&skinthickness=100&weight=100&height=100&age=20
@app.route('/medical_api', methods=['GET'])
def api_filter():
    query_parameters = request.args
    preg = query_parameters.get("pregnancies")
    glu = query_parameters.get("glucose")
    blp = query_parameters.get("bloodpressure")
    skn = query_parameters.get("skinthickness")
    try:
        weight = query_parameters.get("weight")
        height = query_parameters.get("height")
        bmi = weight/((height/100)**2)
    except:
        bmi=0
    age = query_parameters.get("age")
    pre = medical_predict(preg,glu,blp,skn,bmi,age)
    return {
        "result": str(pre)
    }
    # return jsonify(result=pre)
    # return json.dump({'result': str(pre)})
    # return str(pre)

@app.route('/personal_api', methods=['GET'])
def api_filter_():
    query_parameters = request.args
    preg = query_parameters.get("pregnancies")
    try:
        weight = query_parameters.get("weight")
        height = query_parameters.get("height")
        bmi = weight/((height/100)**2)
    except:
        bmi=0
    age = query_parameters.get("age")
    pre = personal_predict(preg,bmi,age)
    return {
        "result": str(pre)
    }
    # return jsonify(result=pre)
    # return json.dump({'result': str(pre)})
    # return str(pre)

if __name__ == '__main__':
    application.run(debug=True)


