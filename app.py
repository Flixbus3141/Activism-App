from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATEIPFAD = 'activities.txt'


def lade_activity():
    activity = []
    try:
        with open(DATEIPFAD, 'r', encoding='utf-8') as f:
            for zeile in f:
                name, ort = zeile.strip().split(',')
                activity.append({'name': name, 'ort': ort})
    except FileNotFoundError:
        open(DATEIPFAD, 'w').close()  # Lege die Datei an, wenn sie fehlt
    return activity


def speichere_activity(activity):
    with open(DATEIPFAD, 'w', encoding='utf-8') as f:
        for act in activity:
            f.write(f"{act['name']},{act['rasse']}\n")


@app.route('/')
def index():
    activity= lade_activity()
    return render_template('index.html', activity=activity)


@app.route('/neu', methods=['GET', 'POST'])
def neu():
    if request.method == 'POST':
        name = request.form['name']
        ort = request.form['ort']
        activity = lade_activity()
        tiere.append({'name': name, 'ort': ort})
        speichere_activity(activity)
        return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/bearbeiten/<name>', methods=['GET', 'POST'])
def bearbeiten(name):
    tiere = lade_tiere()
    tier = next((t for t in tiere if t['name'] == name), None)
    if not tier:
        return "Tier nicht gefunden", 404

    if request.method == 'POST':
        tier['name'] = request.form['name']
        tier['rasse'] = request.form['rasse']
        speichere_tiere(tiere)
        return redirect(url_for('index'))

    return render_template('edit.html', tier=tier)


@app.route('/loeschen/<name>', methods=['POST'])
def loeschen(name):
    tiere = lade_tiere()
    tiere = [t for t in tiere if t['name'] != name]
    speichere_tiere(tiere)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)