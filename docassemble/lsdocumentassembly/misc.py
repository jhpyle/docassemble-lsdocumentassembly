# pre-load
from flask import request, jsonify
from flask_cors import cross_origin
from docassemble.base.util import create_session, set_session_variables, interview_url
from docassemble.webapp.app_object import app, csrf
from docassemble.webapp.server import api_verify, jsonify_with_status, jsonify

@app.route('/newlssession', methods=['POST'])
@csrf.exempt
@cross_origin(origins='*', methods=['POST', 'HEAD'], automatic_options=True)
def lsapi_newsession():
    if not api_verify(request):
        return jsonify_with_status({"url": "Access denied."}, 403)
    post_data = request.get_json(silent=True)
    if post_data is None:
        post_data = request.form.copy()
    if 'yaml' not in post_data:
        return jsonify_with_status({"url": "No 'yaml' specified in POST data."}, 400)
    args = {}
    for key, val in post_data.items():
        if key != 'yaml':
            args[key] = val
    session_id = create_session(post_data['yaml'])
    if len(args):
        set_session_variables(post_data['yaml'], session_id, args, overwrite=True, process_objects=False)
    url = interview_url(i=post_data['yaml'], session=session_id, style='short_package')
    return jsonify({'url': url})
