from app import application

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.run(host='0.0.0.0', port=8000)