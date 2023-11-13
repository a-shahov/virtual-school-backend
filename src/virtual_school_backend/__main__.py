from virtual_school_backend import create_app

app = create_app()

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()