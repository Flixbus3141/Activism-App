from flask import Flask, render_template, request, redirect, url_for
import logging

app = Flask(__name__)
DATEIPFAD = 'activities.txt'
app.debug = True
app.logger.setLevel(logging.DEBUG)

def lade_activity():
    activity = []
    try:
        with open(DATEIPFAD, 'r', encoding='utf-8') as f:
            for zeile in f:
                app.logger.debug(zeile)
                name, ort = zeile.strip().split(',')
                activity.append({'name': name, 'ort': ort})
                app.logger.debug(activity)
    except FileNotFoundError:
        open(DATEIPFAD, 'w').close()  # Lege die Datei an, wenn sie fehlt
    return activity


def speichere_activity(activity):
    with open(DATEIPFAD, 'w', encoding='utf-8') as f:
        for act in activity:
            f.write(f"{act['name']},{act['ort']}\n")


@app.route('/')
def index():
    activity= lade_activity()
    return render_template('home.html', activity=activity)


@app.route('/neu', methods=['GET', 'POST'])
def neu():
    if request.method == 'POST':
        name = request.form['name']
        ort = request.form['ort']
        activity = lade_activity()
        activity.append({'name': name, 'ort': ort})
        speichere_activity(activity)
        return redirect(url_for('overview'))
    return render_template('create.html')


@app.route('/bearbeiten/<name>', methods=['GET', 'POST'])
def bearbeiten(name):
    activity = lade_activity()
    act = next((t for t in activity if t['name'] == name), None)
    if not act:
        return "Activität nicht gefunden", 404

    if request.method == 'POST':
        act['name'] = request.form['name']
        act['ort'] = request.form['ort']
        speichere_activity(activity)
        return redirect(url_for('overview'))

    return render_template('edit.html', act=act)


@app.route('/loeschen/<name>', methods=['POST'])
def loeschen(name):
    activity = lade_activity()
    activity = [t for t in activity if t['name'] != name]
    speichere_activity(activity)
    return redirect(url_for('overview'))

@app.route('/overview')
def overview():
    activity = lade_activity()
    return render_template('overview.html',activity = activity)

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)