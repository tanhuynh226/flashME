from flask import Flask
app = Flask("server") #Change name

@app.route('/')
def homeRoute():
    pass

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

def afterRequest():
    # Update data with new retrieved / sent data?
    pass

app.after_request(afterRequest) 

'''
CREATE A POST ROUTE
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        etc
    elif request.authorization !== 'authorization':
        abort(401)
        this_is_never_executed()

RETURN JSON
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

GET USERNAME
@app.route('/user/<username>')
def profile(username):
    user = mongodb.fetch_user('')
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }


'''
