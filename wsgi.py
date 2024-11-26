from projectFiles import instantiate_app

app = instantiate_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, debug=True)