from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)

@app.route('/')
def home():
    if  "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)