from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True) # Prod ortamda debug'ı kapatmayı unutma Alkım