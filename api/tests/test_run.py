from flaskapi.app import create_app

def test_create_app():
    app = create_app("some_name")
    assert app.name == "some_name"
