import app_api
from utils.core import Engine
from flask import Flask, request, jsonify


recommendation_engine = Engine()
app_api.app_context["recommendation_engine"] = recommendation_engine

app_api.app.run(debug=True)