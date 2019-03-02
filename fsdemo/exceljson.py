from flask import Blueprint, render_template, request, redirect
from fsdemo.pagedata.exceljson import ExcelJsonPageData, ExcelJsonOutput

exceljson_page = Blueprint('exceljson', __name__, static_folder='static', template_folder='templates')

@exceljson_page.route('/', methods=['GET'])
def exceljson_index():
    if request.method == 'GET':
        try:
            input_filename = request.args.get('file', 'example.csv')
        except KeyError:
            input_filename = 'example.csv'
            pass
    return render_template('exceljson_index.html', pageData=ExcelJsonPageData(input_filename))

@exceljson_page.route('/output', methods=['GET', 'POST'])
def exceljson_output():
    if request.method == 'POST':
        return ExcelJsonOutput().autoOutputFile(request)
    else:
        return redirect('/exceljson')
