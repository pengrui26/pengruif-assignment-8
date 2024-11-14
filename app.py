from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from logistic_regression import do_experiments


app = Flask(__name__)

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

from time import time

@app.route('/run_experiment', methods=['POST'])
def run_experiment():
    start = float(request.json['start'])
    end = float(request.json['end'])
    step_num = int(request.json['step_num'])

    # Run the experiment with the provided parameters
    do_experiments(start, end, step_num)

    
    timestamp = int(time())
    dataset_img = f"results/dataset.png?{timestamp}"
    parameters_img = f"results/parameters_vs_shift_distance.png?{timestamp}"
    
    return jsonify({
        "dataset_img": dataset_img if os.path.exists("results/dataset.png") else None,
        "parameters_img": parameters_img if os.path.exists("results/parameters_vs_shift_distance.png") else None
    })


# Route to serve result images
@app.route('/results/<filename>')
def results(filename):
    return send_from_directory('results', filename)

if __name__ == '__main__':
    app.run(debug=True)