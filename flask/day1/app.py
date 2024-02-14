from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'title':'Flask Jinja Template',
        'user':'ham',
        'is_admin':True,
        'item_list':["Item1", "Item2", "Item3"]
    }

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)