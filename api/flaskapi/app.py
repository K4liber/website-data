from flask import Flask

def create_app(app_name):
    return Flask(app_name)
