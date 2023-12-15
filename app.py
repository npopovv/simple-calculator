from flask import Flask, request, jsonify, render_template

# Create the app object
app = Flask(__name__)


# importing function for calculations
from calculator import Calculator

# Define calculator
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    expr = str(request.form['a'])

    c = Calculator()
    result = c.evaluate(expr)
    
    out = expr+' = '+ str(result)
    return render_template('index.html',  prediction_text = out)


if __name__ == "__main__":
    app.run(debug=True)
