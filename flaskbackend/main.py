from flask import Flask, render_template,request

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

if __name__ == '__main__':
    app.run(debug=True)