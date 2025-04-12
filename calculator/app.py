from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)


if not os.path.exists("static/charts"):
    os.makedirs("static/charts")
    
@app.route('/')
def home(): 
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dimension = float(request.form.get('dimension', 0))
        material = request.form.get('material', '')
        labour_cost = float(request.form.get('labour_cost', 0))
        labour_day = float(request.form.get('labour_day', 0))
        labour_number = int(request.form.get("labour_number", 0))

        material_rates = {
            "concrete": 50,
            "steel": 80,
            "wood": 40
        }

        material_cost = material_rates.get(material, 0) * dimension
        total_labor_hours = labour_day * 8 * labour_number
        total_labor_cost = total_labor_hours * labour_cost
        overhead = 0.1 * (material_cost + total_labor_cost)
        total_cost = material_cost + total_labor_cost + overhead

        # here user get suggestions based on input
        suggestions = []
        if material == 'steel':
            suggestions.append("")
        elif material == 'concrete':
            suggestions.append("Using precast concrete could reduce labor time and costs.")
        if total_labor_hours > 100:
            suggestions.append("Review project plan to optimize labor scheduling and reduce excess hours.")

        #  by this user get  chart
        labels = ['Material', 'Labor', 'Overheads']
        values = [material_cost, total_labor_cost, overhead]

        plt.figure(figsize=(5, 5))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Cost Distribution")
        chart_path = 'static/charts/cost_chart.png'
        plt.savefig(chart_path)
        plt.close()

        return render_template('result.html',
                               dimension=dimension,
                               material=material,
                               labour_day=labour_day,
                               labour_cost=labour_cost,
                               labour_number=labour_number,
                               material_cost=material_cost,
                               total_labor_cost=total_labor_cost,
                               overhead=overhead,
                               total_cost=total_cost,
                               chart_path=chart_path,
                               suggestions=suggestions)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('home.html')


@app.route('/login')  
def login():
    return render_template('login.html')
             

if __name__ == '__main__':
    app.run(debug=True)
