# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify,abort
import config
import requests
from modules import User, Car_rental, CarsDataset,Cars
from exits import db
import os
from decoratars import login_required
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_admin import Admin, BaseView, expose
import random
# from flask_login import LoginManager,UserMixin

from math import *

ip = '128.250.51.47'
url = 'http://freegeoip.net/json/' + ip
r = requests.get(url)
js = r.json()
#
# SAMPLE_RESPONSE = """{
#     "ip":"108.46.131.77",
#     "country_code":"US",
#     "country_name":"United States",
#     "region_code":"NY",
#     "region_name":"New York",
#     "city":"Brooklyn",
#     "zip_code":"11249",
#     "time_zone":"America/New_York",
#     "latitude":40.645,
#     "longitude":-73.945,
#     "metro_code":501
# }"""


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.secret_key = os.urandom(24)
GoogleMaps(app)


flask_admin = Admin()
flask_admin.init_app(app)
EARTH_REDIUS = 6378.137


@app.route('/')
@login_required
def index():

    username = session['username']

    return render_template('index.html', username=username)


# @app.route('/testmap/')
# @login_required
# def testmap():
#     locations = []
#     for n in range(0,50):
#         x=random.uniform(-37.803144,-37.803194)
#         y=random.uniform(144.96557,144.96559)
#         locations = [x,y]
#     print locations
#     map = Map(
#         identifier="mymap",
#         lat=locations[0].latitude,
#         lng=locations[0].longitude,
#         markers=[(loc.latitude, loc.longitude) for loc in locations]
#     )
#     return render_template('testmap.html', map=map)


@app.route('/login/', methods=['GET', 'POST'])
def login(username,password):
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('register'):
            return render_template('register.html')

        username = request.form.get('username')
        password = request.form.get('password')
        # authorid=request.form('')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            return redirect('/')
        else:
            return u'wrong username or password,please try again '


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            return u'different passwords,please try again!'
        else:
            user = User(username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/car_rental/', methods=['GET', 'POST'])
# @login_required
def car_rental():
    if request.method == 'GET':
        return render_template('car_rental.html')
    else:
        name = "test"
        brand = "tet"
        if 'name' in request.form:
            name = request.form['name']
            brand = request.form['brand']
        return render_template('car_rental.html', name=name, brand=brand)
        # title = request.form.get('title')
        # content = request.form.get('content')
        # car_rental = Car_rental(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        # car_rental.author = user
        # db.session.add(car_rental)
        # db.session.commit()
        # return redirect(url_for('index'))


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.context_processor
def my_context_processor():
    user = session.get('username')
    if user:
        return {'user': user}
    return {}


def url_for_other_page(page):
    # args = request.view_args.copy()
    args = dict(request.view_args.items() + request.args.to_dict().items())  # 如果采用上面那句则换页时querystring会丢失
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/users/<username>/')
@login_required
def get_users(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('users.html', user=user)




@app.route('/ContactUs/', methods=['GET', 'POST'])
@login_required
def ContactUs():
    username = session['username']
    return render_template('ContactUs.html',username=username)


@app.route('/faq/', methods=['GET', 'POST'])
@login_required
def faq():
    username = session['username']
    return render_template('Faq.html',username=username)

# save car
@app.route('/booking/savecar',methods=['POST'])
@login_required
def bookingsavecar():
    if request.method == 'POST':
        # value from post
        Bdatetime = request.form.get('Bdatetime')
        Btime = request.form.get('Btime')
        Bday = request.form.get('Bday')
        Rdatetime = request.form.get('Rdatetime')
        Rtime = request.form.get('Rtime')
        Rday = request.form.get('Rday')

        name = request.form['name']
            # brand = request.form['brand']
            # seat = request.form['seat']
            # bluetooth = request.form['bluetooth']
            # vehicleType = request.form['vehicleType']

        # return 'test'

        carinfo = Cars(Rdatetime=Rdatetime, Bdatetime=Bdatetime, carname=name,
                       Rday=Rday, Rtime=Rtime, Btime=Btime, Bday=Bday)

        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        carinfo.author = user
        db.session.add(carinfo)
        db.session.commit()
        return redirect(url_for('booking'))


# get values from map
@app.route('/booking/car/', methods=['GET', 'POST'])
@login_required
def bookingcar():
    username = session['username']
    if request.method == 'GET':
        # return map
        return redirect(url_for('booking'))
        #return render_template('car.html',name='tom')
    else:
     # values from map
        name = request.form['name']
        price = request.form['price']
        brand = request.form['brand']

        seat = request.form['seat']
        bluetooth = request.form['bluetooth']
        vehicleType = request.form['vehicleType']

        kilometer = request.form['kilometer']


        #return 'test'


        return render_template('car.html', name=name, price=price, brand=brand, bluetooth=bluetooth, seat=seat,
                               vehicleType=vehicleType, username=username,kilometer=kilometer)


def rand(a,b):
    return random.random()*(a-b)+b
@app.route('/booking/', methods=['GET', 'POST'])
@login_required
def booking():
    username = session['username']
    page_data = CarsDataset.query
    for p in page_data:
        name = p.serializer()['name']
        db.session.query(CarsDataset).filter(CarsDataset.name==name).update(
            {'lat': rand(-37.817000,-37.778999), 'lng': rand(144.95000,144.99399)})
    db.session.commit()
    # catdatas = CarsDataset.query.all()
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        if int(tid) == 1:
            page_data = page_data.filter_by(brand='audi')

        if int(tid) == 2:
            page_data = page_data.filter_by(brand='volkswagen')

        if int(tid) == 3:
            page_data = page_data.filter_by(brand='bmw')

        if int(tid) == 4:
            page_data = page_data.filter_by(brand='peugeot')

        if int(tid) == 5:
            page_data = page_data.filter_by(brand='mercedesBenz')

        if int(tid) == 6:
            page_data = page_data.filter_by(brand='ford')

    time = request.args.get("time", 0)
    if int(time) == 1:
        page_data = page_data.filter_by(gearbox='manual')
    if int(time) == 2:
        page_data = page_data.filter_by(gearbox='automatic')

    pm = request.args.get("pm", 0)
    p = dict(
        tid=tid,
        time=time,
        pm=pm
    )
    locations = [d.serializer() for d in page_data]

    Lat_A = -37.80314407
    Lng_A = 144.9655776
    Lat_B = page_data.with_entities(CarsDataset.lat).all()
    Lng_B = page_data.with_entities(CarsDataset.lng).all()
    sb = haversine(Lng_A, Lat_A, Lng_B, Lat_B)
    sb = [s for s in sb]

    context = {
        'CarsDataset': CarsDataset.query.all()
    }

    # Lat = page_data.with_entities(CarsDataset.lat).all()
    # Lng = page_data.with_entities(CarsDataset.lng).all()
    # for x,y in zip(Lat,Lng):
    #     sndmap = Map(
    #         identifier="sndmap",
    #         lat=-37.8253632,
    #         lng=144.9504107,
    #         style="height:500px;width:500px;margin:0;",
    #         markers=[{
    #             'lat':x,
    #             'lng':y,
    #         }]
    #      )

    boxcontent = "<form method='post' action='http://127.0.0.1:5000/booking/car/'><div>{0}<input type='hidden' name='name' value='{0}'/></div>"" \
    ""<div>{1}$/Day<input type='hidden' name='price' value='{1}'/><div><input type='hidden' name='brand' value='{2}'/></div> <div><input type='hidden' name='seat' value='{3}'/></div>" \
    "<div><input type='hidden' name='bluetooth' value='{4}'/></div>" \
    "<div><input type='hidden' name='vehicleType' value='{5}'/></div>" \
                 "<div><input type='hidden' name='kilometer' value='{6}'/></div>" \
                 "</div><button type='submit'class=btn btn-primary>booking</button></form>"

    carmap = Map(
        identifier="carmap",
        style="height:700px;width:800px;margin:0;",
        zoom="15",
        language="en",

        # lat=locations[0]['lat'],
        lat =-37.80314407,
        # lng=locations[0]['lng'],
        lng=144.9655776,
        icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
        name=locations[0]['name'],
        brand=locations[0]['brand'],
        seat=locations[0]['seat'],
        bluetooth=locations[0]['bluetooth'],
        vehicleType=locations[0]['vehicleType'],
        kilometer=locations[0]['kilometer'],
        price=locations[0]['price'],

        markers=[{"lat": loc['lat'], "lng": loc['lng'],
                  "infobox": boxcontent.format(loc['name'].encode('utf-8'), loc['price'], loc['brand'].encode('utf-8'), loc['seat'],
                                               loc['bluetooth'], loc['vehicleType'],loc['kilometer'])} for loc in locations]
    )

    # markers = [{"lat": loc['lat'], "lng": loc['lng'],
    #             "infobox": boxcontent.format(loc['name'].encode('utf-8'), loc['price'], loc['brand'].encode('utf-8'),
    #                                          loc['seat'],
    #                                          loc['bluetooth'], loc['vehicleType'], loc['kilometer'])} for loc in
    #            locations]
    # )


    # if request.method == 'POST':
    #     location = request.form.get('location')
    #     Bdatetime = request.form.get('Bdatetime')
    #     Btime = request.form.get('Btime')
    #     Bday = request.form.get('Bday')
    #
    #     Rdatetime = request.form.get('Rdatetime')
    #     Rtime = request.form.get('Rtime')
    #     Rday = request.form.get('Rday')
    #
    #     cattype = request.form.get('type')
    #     gearbox = request.form.get('gear')
    #
    #     car = Cars(location=location, Rdatetime=Rdatetime, Bdatetime=Bdatetime, cattype=cattype, gearbox=gearbox,
    #                Rday=Rday, Rtime=Rtime, Btime=Btime, Bday=Bday)
    #     user_id = session.get('user_id')
    #     user = User.query.filter(User.id == user_id).first()
    #     car.author = user
    #     db.session.add(car)
    #     db.session.commit()

    return render_template('booking.html', carmap=carmap, page_data=page_data, sb=sb, p=p, username=username,**context)

@app.route('/tables/', methods=['GET', 'POST'])
@login_required
def tables():
    username = session['username']

    author_id = session['user_id']

    context = {
        'Cars': Cars.query.filter_by(author_id=author_id)
    }

    return render_template('tables.html',username=username,**context)


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    conter = 0
    for x, y in zip(lon2, lat2):
        conter += 1
        # print(x[0], y[0], conter, lon1, lat1)
        lon1_, lat1_, lon2, lat2 = map(radians, [lon1, lat1, x[0], y[0]])
        # haversine公式
        dlon = lon2 - lon1_
        dlat = lat2 - lat1_
        a = sin(dlat / 2) ** 2 + cos(lat1_) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        yield c * r


@app.route('/api/cardatas')
def fetch_cardata():
    datas = CarsDataset.query.all()
    return jsonify({'data': [d.serializer() for d in datas]})


if __name__ == '__main__':
    app.run()