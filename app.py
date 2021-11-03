from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///wines.sqlite'
app.config['SECRET_KAY']='velessa2128506'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Sort(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(35))
    def __str__(self):
        return self.name

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65))

    def __str__(self):
        return f'\"{self.name}\"'

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65))
    price=db.Column(db.Float)
    top=db.Column(db.Integer, default=0)
    sort_id=db.Column(db.Integer,db.ForeignKey('sort.id'))
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'))

    sort=db.relationship(Sort, backref=db.backref('wines'))
    producer = db.relationship(Producer, backref=db.backref('wines'))

    def __str__(self):
        return self.name

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author=db.Column(db.String(64))
    email=db.Column(db.String(64))
    text=db.Column(db.String(1024))

    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'))
    wine=db.relationship(Wine, backref=db.backref('comments'))

    def __str__(self):
        return f'{self.text} ({self.author}, {self.email})'
    def __lt__(self, other):
        return self.id>other.id

@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index')
@app.route('/index/<string:sorttype>')
def index(sorttype=None):
    wines=Wine.query.order_by(Wine.name)
    if sorttype=='bypriceasc':
        wines=sorted(wines,key=lambda x: x.price)
    if sorttype=='bypricedesc':
        wines=sorted(wines,key=lambda x: -x.price)
    if sorttype=='byproducer':
        wines=sorted(wines,key=lambda x: x.producer.name)
    if sorttype=='bysortwine':
        wines=sorted(wines,key=lambda x: x.sort.name)
    return render_template('index.html', wines=wines)

@app.route('/filter/<int:sort_id>/<int:producer_id>')
def filter(sort_id, producer_id):
    producer, sort = None, None
    if producer_id==0:
        wines=Wine.query.filter(Wine.sort_id==sort_id)
        sort=Sort.query.get(sort_id)
    elif sort_id==0:
        wines = Wine.query.filter(Wine.producer_id == producer_id)
        producer = Producer.query.get(producer_id)
    else:
        wines = Wine.query.filter(Wine.sort_id==sort_id, Wine.producer_id == producer_id)
        sort = Sort.query.get(sort_id)
        producer = Producer.query.get(producer_id)
    return render_template('filter.html', wines=wines, sort=sort, producer=producer)

@app.route('/wine/<int:pk>')
def wine(pk):
    #wine=Wine.query.get(pk)
    return render_template('wine.html', wine=Wine.query.get(pk))
                           #, comments=sorted(wine.comments))

@app.route('/add/comment/<int:pk>', methods=["POST"])
def add_comment(pk):
    #wine = Wine.query.get(pk)
    text = request.form.get('text')
    author = request.form.get("author")
    email = request.form.get("email")
    if author and text and email:
        new_comment=Comment(text=text, author=author, email=email, wine_id=pk)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('wine', pk=pk))

@app.route('/config/wine/<int:pk>')
def config(pk):
    wine=Wine.query.get(pk)
    return render_template('config.html', wine=wine, producers=Producer.query.all(), sorts=Sort.query.all(),)

@app.route('/change/wine/<int:pk>', methods=["POST"])
def change_wine(pk):
    wine=Wine.query.get(pk)
    new_name=request.form.get("name")
    if new_name and new_name != wine.name:
        wine.name=new_name
    new_price = float(request.form.get("price"))
    if new_price != wine.price:
        wine.price = new_price
    new_producer_id = int(request.form.get("producer"))
    if new_producer_id != wine.producer_id:
        wine.producer_id = new_producer_id
    new_sort_id = int(request.form.get("sort"))
    if new_sort_id != wine.sort_id:
        wine.sort_id = new_sort_id
    new_top = request.form.get('top')
    # print([new_top])
    if bool(new_top) != bool(wine.top):
        wine.top = int(bool(new_top))
    db.session.commit()
    return redirect(url_for('wine', pk=pk))


if __name__=='__main__':
    app.run(debug=True, port=5001)