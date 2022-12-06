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

STIMULI = pd.read_csv('data/stimuli_original.csv') ## id, sentence, is_high_rate
FILLERS = pd.read_csv('data/fillers.csv') ## id, sentence,i s_acceptable
RESULTS = pd.read_csv('static/result.csv') ## date, name, age, gender, stimulus, is_filler, naturality

latin_square = 0 # 0, 1, 2, 3, 4 : 4 stimuli for each experiment

###########################################################

@app.route("/", methods=['GET', 'POST'])
def top_page():
    
    ### TOP PAGE ###
    if request.method == 'GET':
        selected_stimuli = STIMULI[STIMULI.id % 5 == latin_square]
        selected_fillers = FILLERS.sample(11)
        stimuli = pd.concat([selected_stimuli, selected_fillers]).sample(frac=1)['sentence'].to_list()
        return render_template('testpage.html', stimuli=stimuli)
    ### receive ajax json
    elif request.method == 'POST':
        ### record result
        now = str(datetime.datetime.today()).split('.')[0]
        userid = request.form['id']
        age = request.form['age']
        gender = request.form['gender']
        stimuli = request.form.getlist('stimuli[]')
        answers = request.form.getlist('answers[]')
        time_record = request.form.getlist('time_record[]')
        ## RESULTS : date,name,age,gender,stimulus,naturality,is_stimulus
        for sti, ans, tm in zip(stimuli, answers, time_record):
            is_stimulus = sti in STIMULI.sentence.values
            RESULTS.loc[len(RESULTS)] = [now, userid, age, gender, sti, ans, is_stimulus, tm]
        RESULTS.to_csv('static/result.csv', index=False)
        RESULTS.to_json('static/result.json', orient='records')
        latin_square = (latin_square + 1) % 5

        return jsonify({'status':'success'})

@app.route("/admin", methods=['GET', 'POST'])
def admin_page():
    return render_template('adminpage.html', result=RESULTS.values.tolist())


###########################################################

if __name__ == "__main__":
    #port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=8000, debug=True)