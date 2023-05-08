from flask import *

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

app.secret_key="aksara"
app.run(port=3000)
