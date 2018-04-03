from app.main import main
from flask import request
from flask import jsonify,render_template

@main.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({"error":"resource not found"})
        response.status_code = 404
        return response
    return render_template('main/404.html')