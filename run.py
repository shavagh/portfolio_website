from portfolio import create_app

# initialise the app
app = create_app() 

# run the app 
if __name__ == '__main__':
    app.run(debug=True)