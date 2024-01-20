import pickle
from django.shortcuts import render
from django.conf import settings
import os

# Create your views here.
def index(request):
  return render(request, 'iris_pred/index.html', {})

def form(request):
  # if this is the post request then we need to process the form data
  if request.method == 'POST':
    # getting model file path
    model_path = os.path.join(settings.BASE_DIR, 'iris_pred/pkl/iris_predict.pkl')
    encoder_path = os.path.join(settings.BASE_DIR, 'iris_pred/pkl/iris_encoder.pkl')

    # loading the model
    loaded_model = pickle.load(open(model_path, 'rb'))
    loaded_encoder = pickle.load(open(encoder_path, 'rb'))

    sepal_l = request.POST['sepal_l']
    sepal_w = request.POST['sepal_w']
    petal_l = request.POST['petal_l']
    petal_w = request.POST['petal_w']
    prediction = loaded_model.predict([[sepal_l, sepal_w, petal_l, petal_w]])
    decode_pred = loaded_encoder.inverse_transform(prediction)

    data = {
      'sepal_length': sepal_l,
      'sepal_width': sepal_w,
      'petal_width': petal_w,
      'petal_length': petal_l,
      'prediction': decode_pred[0],
    }
    return render(request, 'iris_pred/form.html', data)
  else: 
    return render(request, 'iris_pred/form.html', {})