from flask import Flask, request, render_template, jsonify
import os, datetime
import pandas as pd

### instantiate app
class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='((',
		variable_end_string='))',
	))

app = CustomFlask(__name__)

STIMULI = pd.read_csv('data/stimuli_original.csv') ## id, sentence
FILLERS = pd.read_csv('data/fillers.csv') ## id, filler
RESULTS = pd.read_csv('static/result.csv') ## date, name, age, gender, stimulus, is_filler, naturality

###########################################################

@app.route("/", methods=['GET', 'POST'])
def top_page():
    
    ### TOP PAGE ###
    if request.method == 'GET':
        selected_stimuli_1 = STIMULI[STIMULI.pattern == 1].sample(2)
        selected_stimuli_2 = STIMULI[STIMULI.pattern == 2].sample(2)
        selected_stimuli_3 = STIMULI[STIMULI.pattern == 3].sample(2)
        selected_fillers = FILLERS.sample(4)
        stimuli = pd.concat([selected_stimuli_1, selected_stimuli_2, selected_stimuli_3])[['id', 'sentence']]
        stimuli = pd.concat([stimuli, selected_fillers]).sample(frac=1)['sentence'].to_list()
        return render_template('testpage.html', stimuli=stimuli)
    ### receive ajax json
    elif request.method == 'POST':
        ### record result
        now = str(datetime.datetime.today()).split('.')[0]
        id_ = request.form['id']
        age = request.form['age']
        gender = request.form['gender']
        stimuli = request.form.getlist('stimuli[]')
        answers = request.form.getlist('answers[]')
        time_record = request.form.getlist('time_record[]')
        ## RESULTS : date,name,age,gender,stimulus,naturality,is_stimulus
        for sti, ans, tm in zip(stimuli, answers, time_record):
            is_stimulus = sti in STIMULI.sentence.values
            RESULTS.loc[len(RESULTS)] = [now, id_, age, gender, sti, ans, is_stimulus, tm]
        RESULTS.to_csv('static/result.csv', index=False)
        RESULTS.to_json('static/result.json', orient='records')

        return jsonify({'status':'success'})

@app.route("/admin", methods=['GET', 'POST'])
def admin_page():
    return render_template('adminpage.html', result=RESULTS.values.tolist())


###########################################################

if __name__ == "__main__":
    #port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=8000, debug=True)