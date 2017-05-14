import requests, json
from .api import db
from app.models import Movie, Cinema, Release, Broadcast, Seat


def getTodayMovie(appKey, cityId):
    url = 'http://v.juhe.cn/movie/movies.today'
    params = {
        'cityid': cityId,
        'key': appKey
    }
    res = requests.get(url=url, params=params)
    res = res.json()
    if res:
        error_code = res['error_code']
        if error_code == 0:
            result = res['result']
            print(result)
            return result
        else:
            print('%s:%s' % (res['error_code'],res['reason']))
    else:
        print('request api error')
    return False


def getMovieDetails(appKey, movieId):
    url = 'http://v.juhe.cn/movie/query'
    params = {
        'movieid': movieId,
        'key': appKey
    }
    res = requests.get(url=url, params=params)
    res = res.json()
    if res:
        error_code = res['error_code']
        if error_code == 0:
            result = res['result']
            print(result)
            return result
        else:
            print('%s:%s' % (res['error_code'], res['reason']))
    else:
        print('request api error')
    return False


def getCinemaByMovie(appKey, cityId, movieId):
    url = 'http://v.juhe.cn/movie/movies.cinemas'
    params = {
        'cityid': cityId,
        'movieid': movieId,
        'key': appKey
    }
    res = requests.get(url=url, params=params)
    res = res.json()
    if res:
        error_code = res['error_code']
        if error_code == 0:
            result = res['result']
            print(result)
            return result
        else:
            print('%s:%s' % (res['error_code'], res['reason']))
    else:
        print('request api error')
    return False


def getCinema(appKey, cityId):
    url = 'http://v.juhe.cn/movie/cinemas.search'
    params = {
        'cityid': cityId,
        'key': appKey,
        'pagesize': 5
    }
    res = requests.get(url=url, params=params)
    res = res.json()
    if res:
        error_code = res['error_code']
        if error_code == 0:
            result = res['result']
            result = result['data']
            print(result)
            return result
        else:
            print('%s:%s' % (res['error_code'], res['reason']))
    else:
        print('request api error')
    return False


def getMovieByCinema(appKey, cinemaId):
    url = 'http://v.juhe.cn/movie/cinemas.movies'
    params = {
        'cinemaid': cinemaId,
        'key': appKey
    }
    res = requests.get(url=url, params=params)
    res = res.json()
    if res:
        error_code = res['error_code']
        if error_code == 0:
            result = res['result']
            print(result)
            return result
        else:
            print('%s:%s' % (res['error_code'], res['reason']))
    else:
        print('request api error')
    return False


def create_database(appKey, cityId):
    print('create database')
    db.drop_all()
    db.create_all()
    cinemas = getCinema(appKey, cityId)
    for cinema in cinemas:
        c = Cinema()
        c.id = int(cinema['id'])
        c.cityName = cinema['cityName']
        c.cinemaName = cinema['cinemaName']
        c.address = cinema['address']
        c.telephone = cinema['telephone']
        c.latitude = float(cinema['latitude'])
        c.longitude = float(cinema['longitude'])
        c.trafficRoutes = cinema['trafficRoutes']
        result = getMovieByCinema(appKey, cinema['id'])
        lists = result['lists']
        for item in lists:
            # some problem there with the api
            # the item's movieId sometimes is None
            m = Movie.query.get(int(item['movieId']))
            if m is None:
                movieId = int(item['movieId'])
                movie = getMovieDetails(appKey, movieId)
                # api doesn't have details of the movie
                if movie == False:
                    m = Movie()
                    m.id = int(item['movieId'])
                    m.title = item['movieName']
                    m.poster = item['pic_url']
                # api has the details of the movie
                else:
                    m = Movie()
                    m.id = int(movie['movieid'])
                    m.actors = movie['actors']
                    m.also_known_as = movie['also_known_as']
                    m.country = movie['country']
                    m.directors = movie['directors']
                    m.film_locations = movie['film_locations']
                    m.genres = movie['genres']
                    m.language = movie['language']
                    m.plot_simple = movie['plot_simple']
                    m.poster = item['pic_url']
                    m.rating = movie['rating']
                    m.rating_count = movie['rating_count']
                    m.release_date = movie['release_date']
                    m.runtime = movie['runtime']
                    m.title = movie['title']
                    m.type = movie['type']
                    m.writers = movie['writers']
                    m.year = movie['year']
            r = Release()
            broadcasts_list = item['broadcast']
            for broadcast_item in broadcasts_list:
                b = Broadcast()
                b.hall = broadcast_item['hall']
                b.price = broadcast_item['price']
                b.time = broadcast_item['time']
                r.broadcasts.append(b)
                db.session.add(b)
            r.movie = m
            c.movies.append(r)
            db.session.add(r)
            db.session.add(m)
        db.session.add(c)
    db.session.commit()
    print('database create success!')
    return '<h1>database update success!</h1>'
