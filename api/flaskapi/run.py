from app import create_app

api = create_app(__name__)

@api.route("/")
def print_status():
    return 'website-data is working.'

if __name__ == '__main__':
    api.run(debug=False, host='0.0.0.0')
