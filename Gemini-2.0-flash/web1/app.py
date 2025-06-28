from flask import Flask, render_template

app = Flask(__name__)

# Определение маршрута для главной страницы
@app.route("/")
def home():
    return render_template("index.html")

# Определение маршрута для страницы "О нас"
@app.route("/about")
def about():
    return render_template("about.html")

# Определение маршрута для страницы "Контакты"
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Пример передачи данных в шаблон
@app.route("/user/<username>")
def user_profile(username):
    return render_template("user.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)
