#!/usr/bin/python3
"""
Script to start a flask application and listen on port 5000
and configure the route /cities_by_state to be rendered with template
that uses data fetched from the backend
"""
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    """
    Rendering html template and displaying cities data retrieved
    from the backend
    """
    from models import storage
    from models.base_model import BaseModel
    from models.state import State
    from models.city import City
    states = storage.all(State)
    cities = storage.all(City)
    return render_template('8-cities_by_states.html', states=states, cities=cities)

@app.teardown_appcontext
def tearDown(self):
    """
    Method to remove the current session
    """
    from models import storage
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
