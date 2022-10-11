from flask import Flask, request, render_template, jsonify
import os, sys, re, collections, csv, glob, time, itertools

### instantiate app
class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='((',
		variable_end_string='))',
	))

app = CustomFlask(__name__)

###########################################################

@app.route("/", methods=['GET', 'POST'])
def top_page():
    ### TOP PAGE ###
    if request.method == 'GET':
        return render_template('testpage.html')


###########################################################

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)