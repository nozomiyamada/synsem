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
RESULTS = pd.read_csv('static/result2.csv') ## date, name, age, gender, stimulus, is_filler, naturality

###########################################################

@app.route("/", methods=['GET', 'POST'])
def top_page():
    
    ### TOP PAGE ###
    if request.method == 'GET':
        selected_stimuli = STIMULI.sample(5)
        selected_fillers = FILLERS.sample(5)
        stimuli = pd.concat([selected_stimuli, selected_fillers]).sample(frac=1)['sentence'].to_list()
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
        ## RESULTS : date,name,age,gender,stimulus,naturality,is_stimulus
        for sti, ans in zip(stimuli, answers):
            is_stimulus = sti in STIMULI.sentence.values
            RESULTS.loc[len(RESULTS)] = [now, id_, age, gender, sti, ans, is_stimulus]
        RESULTS.to_csv('static/result2.csv', index=False)
        RESULTS.to_json('static/result.json', orient='records')

        return jsonify({'status':'success'})

@app.route("/admin", methods=['GET', 'POST'])
def admin_page():
    return render_template('adminpage.html', result=RESULTS.values.tolist())


###########################################################

if __name__ == "__main__":
    #port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=8000, debug=True)