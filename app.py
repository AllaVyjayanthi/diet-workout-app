from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load calorie prediction model
calorie_model = pickle.load(open("calorie_model.pkl","rb"))

# ---------------- CHATBOT ----------------
def chatbot(msg):
    msg = msg.lower()
    replies = {
        "weight loss": "Follow calorie deficit, walking, and strength training.",
        "belly fat": "Do plank, crunches, and cardio.",
        "diabetes": "Avoid sugar, eat oats, vegetables, and fruits.",
        "protein": "Eggs, paneer, dal, tofu, chickpeas.",
        "water": "Drink 3-4 liters daily."
    }
    return replies.get(msg,"Follow your diet and workout plan regularly.")

# ---------------- BMI FUNCTION ----------------
def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("input.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():

    age = int(request.form["age"])
    height = float(request.form["height"])   # in CM
    weight = float(request.form["weight"])   # in KG
    gender = request.form["gender"]
    activity = request.form["activity"]

    g = 0 if gender=="Male" else 1
    a = {"Sedentary":0,"Light":1,"Moderate":2,"Active":3}[activity]

    calories = int(calorie_model.predict([[age,height,weight,g,a]])[0])

    bmi = round(weight/((height/100)**2),2)
    status = bmi_status(bmi)

    if status=="Underweight":
        goal="Weight Gain"
    elif status=="Healthy Weight":
        goal="Maintain Fitness"
    else:
        goal="Weight Loss"

    # ---------------- DIET PLANS ----------------
    if status=="Underweight":
        diet = {
            "Morning":"Milk + Banana + Nuts",
            "Breakfast":"Oats / Vegetable Omelette",
            "Lunch":"Roti + Dal + Rice + Sabzi",
            "Evening":"Peanut Chaat / Fruit",
            "Dinner":"Roti + Paneer / Chicken + Veggies"
        }

    elif status=="Healthy Weight":
        diet = {
            "Morning":"Warm Water + Fruit",
            "Breakfast":"Oats / Idli",
            "Lunch":"Roti + Dal + Sabzi",
            "Evening":"Sprouts / Buttermilk",
            "Dinner":"Light Roti + Veg Curry"
        }

    else:   # Overweight & Obese
        diet = {
            "Morning":"Warm Lemon Water",
            "Breakfast":"Oats / Poha",
            "Lunch":"Roti + Dal + Salad",
            "Evening":"Green Tea + Roasted Chana",
            "Dinner":"Soup / Veggies"
        }

    # ---------------- WEEKLY WORKOUT ----------------
    weekly_workout = {
        "Monday":"Brisk Walk 30 min",
        "Tuesday":"Squats + Pushups",
        "Wednesday":"Cycling / Jogging",
        "Thursday":"Yoga",
        "Friday":"Core Workout",
        "Saturday":"Full Body Workout",
        "Sunday":"Rest + Stretching"
    }

    return render_template("dashboard.html",
        bmi=bmi,status=status,goal=goal,
        calories=calories,diet=diet,
        weekly_workout=weekly_workout)


@app.route("/chat",methods=["POST"])
def chat():
    msg=request.form["msg"]
    return chatbot(msg)

import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")  # your main page

# add this at the end
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns PORT
    app.run(host="0.0.0.0", port=port)




