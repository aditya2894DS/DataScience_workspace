from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# importing model
model_file = open('F:\Programming\DataScience\Python\Projects\CarPricePredictor\carprice_predict_mdl', 'rb')
model = pickle.load(model_file)
model_file.close()

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_price():
  if request.method == 'POST':

    Year_bought = int(request.form.get('year_bought'))
    Current_year = 2021
    if (1990 < Year_bought < Current_year):
      Car_age = Current_year - Year_bought
    else: Car_age = 0

    Present_Price = float(request.form.get('present_price'))
    Kms_Driven = int(request.form.get('kms_driven'))
    
    Fuel_Type = request.form.get('fuel_type')
    if(Fuel_Type == 'Petrol'):
      Fuel_Type_Petrol = 1
      Fuel_Type_Diesel = 0
    elif(Fuel_Type == 'Diesel'):
      Fuel_Type_Petrol = 0
      Fuel_Type_Diesel = 1
    elif(Fuel_Type == 'CNG'):
      Fuel_Type_Petrol = 0  
      Fuel_Type_Diesel = 0  

    Seller_Type = request.form.get('seller_type')
    if Seller_Type == 'Individual':
      Seller_Type_Individual = 1
    else: Seller_Type_Individual = 0

    Transmission_Type = request.form.get('trans_type')
    if Transmission_Type == 'Manual':
      Transmission_Manual = 1
    else: Transmission_Manual = 0  
    
    prediction = model.predict([[Present_Price,
                               Kms_Driven,
                               Car_age,
                               Fuel_Type_Diesel,
                               Fuel_Type_Petrol,
                               Seller_Type_Individual,
                               Transmission_Manual ]])
    if prediction != None:
      model_output = round(prediction[0], 2) 
    else: model_output = None      
    print('Price: {}, Kms: {}, Car_age: {}, Diesel: {}, petrol: {}, indi: {}, manual: {}, output: {}'.format(Present_Price,
                               Kms_Driven,
                               Car_age,
                               Fuel_Type_Diesel,
                               Fuel_Type_Petrol,
                               Seller_Type_Individual,
                               Transmission_Manual,
                               model_output))
    if model_output < 0:
      return render_template('index.html', prediction_text='Sorry you cannot sell this car.')
    else: return render_template('index.html', prediction_text='{}'.format(model_output))
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)


