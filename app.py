from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <h1>Michigan Sports Info!</h1>
        <ul>
            <li><a href="/filtered"> Men's Basketball </a></li>
        </ul>
    '''


@app.route('/filtered', methods=['GET', 'POST'])
def filtered():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        filtered_ordered = model.filtered_order(sortby, sortorder)
    else:
        filtered_ordered = model.filtered_order()
        
    return render_template("filtered.html", filtered_ordered=filtered_ordered)

@app.route('/marked', methods=['GET', 'POST'])
def marked():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        marked_ordered = model.marked_order(sortby, sortorder)
    else:
        marked_ordered = model.marked_order()
        
    return render_template("marked.html", marked_ordered=marked_ordered)


@app.route('/reviews', methods=['GET', 'POST'])
def review():
    reviews = model.get_review()
    return render_template("reviews.html", reviews=reviews)


@app.route('/compared', methods=['GET', 'POST'])
def compared():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        compared_ordered = model.compared_order(sortby, sortorder)
    else:
        compared_ordered = model.compared_order()
        
    return render_template("compared.html", compared_ordered=compared_ordered)



if __name__ == '__main__':
    model.init_filter()
    model.init_marker()
    model.init_reviews()
    model.init_comparator()
    app.run(debug=True)    