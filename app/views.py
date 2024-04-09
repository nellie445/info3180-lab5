"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, jsonify, send_from_directory
from flask_wtf.csrf import generate_csrf 
from werkzeug.utils import secure_filename
import os
from app.forms import MovieForm
from app.models import Movie

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# Route for adding movies.
@app.route('/api/v1/movies', methods=['POST'])
def save_movie():
    form = MovieForm()

    if form.validate_on_submit():
        poster = form.poster.data
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster=filename
        )

        db.session.add(movie)
        db.session.commit()

        response_data = {
            "message": "Movie successfully added",
            "title": form.title.data,
            "description": form.description.data,
            "poster": filename
        }
        return jsonify(response_data), 201

    else:
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400

# Route to fetch all movies
@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': movie.poster
        }
        movie_list.append(movie_data)
        
    return jsonify({'movies': movie_list})

# Route for retrieving CSRF token.
@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()}) 

# Route for serving uploaded poster images.
@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

# Function to collect form errors.
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages

# Route for serving static text files.
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

# Add headers to responses.
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Error handler for 404 Not Found.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404