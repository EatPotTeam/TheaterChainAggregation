import os
from flask import jsonify, request
from .. import db
from .database_operation import create_database
from . import main
from ..models import Movie, Cinema, Release, Broadcast, Seat


@main.route('/')
def index():
    return '<h1>Cinema Server!</h1>'


@main.route('/api/movie/', methods=['GET'])
def allMovie():
    movies = Movie.query.all()
    results = []
    for movie in movies:
        results.append({
            'movieId': movie.id,
            'movieName': movie.title,
            'pic_url': movie.poster
        })
    response = {
        'results': results
    }
    print(response)
    return jsonify(response)


@main.route('/api/movie/<int:id>/', methods=['GET'])
def findMovieById(id):
    movie = Movie.query.get_or_404(id)
    response = {}
    if movie:
        result = {
            'movieId': movie.id,
            'rating': movie.rating,
            'genres': movie.genres,
            'runtime': movie.runtime,
            'language': movie.language,
            'title': movie.title,
            'poster': movie.poster,
            'writers': movie.writers,
            'film_locations': movie.film_locations,
            'directors': movie.directors,
            'rating_count': movie.rating_count,
            'actors': movie.actors,
            'plot_simple': movie.plot_simple,
            'year': movie.year,
            'country': movie.country,
            'type': movie.type,
            'release_date': movie.release_date,
            'also_known_as': movie.also_known_as
        }
        response['result'] = result
    return jsonify(response)


@main.route('/api/cinema/', methods=['GET'])
def allCinema():
    cinemas = Cinema.query.all()
    results = []
    for cinema in cinemas:
        results.append({
            'id': cinema.id,
            'cityName': cinema.cityName,
            'cinemaName': cinema.cinemaName,
            'address': cinema.address,
            'telephone': cinema.telephone,
            'latitude': cinema.latitude,
            'longitude': cinema.longitude,
            'trafficRoutes': cinema.trafficRoutes
        })
    response = {
        'results': results
    }
    return jsonify(response)


@main.route('/api/cinema/<int:id>/', methods=['GET'])
def cinemaBroadcast(id):
    cinema = Cinema.query.get_or_404(id)
    cinema_info = {
        'id': cinema.id,
        'name': cinema.cinemaName,
        'city': cinema.cityName,
        'telephone': cinema.telephone,
        'address': cinema.address
    }
    lists = []
    for movie_release in cinema.movies:
        movie = movie_release.movie
        item = {
            'movieId': movie.id,
            'movieName': movie.title,
            'pic_url': movie.poster
        }
        broadcasts = movie_release.broadcasts
        broadcast_list = []
        for broadcast in broadcasts:
            broadcast_list.append({
                'broadcastId': broadcast.id,
                'hall': broadcast.hall,
                'price': broadcast.price,
                'time': broadcast.time
            })
        item['broadcast'] = broadcast_list
        lists.append(item)
    response = {
        'result': {
            'cinema_info': cinema_info,
            'lists': lists
        }
    }
    return jsonify(response)


@main.route('/api/movie/<int:id>/cinema', methods=['GET'])
def movieOnCinema(id):
    movie = Movie.query.get_or_404(id)
    cinemas = movie.cinemas
    result = []
    for cinema_release in cinemas:
        cinema = cinema_release.cinema
        result.append({
            'cinemaName': cinema.cinemaName,
            'cinemaId': cinema.id,
            'address': cinema.address,
            'latitude': cinema.latitude,
            'longitude': cinema.longitude
        })
    response = {
        'result': result
    }
    return jsonify(response)


@main.route('/api/broadcast/<int:id>/', methods=['GET'])
def getSeats(id):
    broadcast = Broadcast.query.get_or_404(id)
    seats = broadcast.seats
    result = []
    for seat in seats:
        result.append({
            'broadcastId': seat.broadcast_id,
            'row': seat.row,
            'col': seat.col
        })
    response = {
        'result': result
    }
    return jsonify(response)


@main.route('/api/broadcast/<int:id>', methods=['POST'])
def lockSeat(id):
    broadcast = Broadcast.query.get_or_404(id)
    print(request.json)
    info = request.json
    if info is None or info == '':
        return jsonify({
            'result': 'no seat info'
        })
    else:
        seat_exist = Seat.query.filter_by(
            broadcast_id=broadcast.id, row=int(info['row']), col=int(info['col'])).count()
        if seat_exist > 0:
            return jsonify({
                'result': 'seat has been lock'
            })
        else:
            seat = Seat(row=int(info['row']), col=int(info['col']))
            broadcast.seats.append(seat)
            db.session.add(seat)
            db.session.add(broadcast)
            db.session.commit()
            return jsonify({
                'result': 'success'
            })


@main.route('/api/broadcast/<int:id>', methods=['DELETE'])
def unlockSeat(id):
        broadcast = Broadcast.query.get_or_404(id)
        info = request.json
        if info is None or info == '':
            return jsonify({
                'result': 'no seat info'
            })
        else:
            seat = Seat.query\
                .filter_by(broadcast_id=broadcast.id, row=int(info['row']), col=int(info['col']))\
                .first_or_404()
            db.session.delete(seat)
            db.session.commit()
            return jsonify({
                'result': 'success'
            })


@main.route('/api/update', methods=['GET'])
def update():
    cityId = 5  # guangzhou
    appKey = os.environ.get('API_APPKEY') or '9a74f1b39739139d30b397fb0098d124'  # the key for query the info api
    create_database(appKey, cityId)
    return '<h1>Database update success!</h1>'
