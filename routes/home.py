from flask import Blueprint, render_template
from ..db import get_connection
 
home_bp = Blueprint('home', __name__, url_prefix='/')
 
@home_bp.get('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM personal_info")
    result_from_personal = cur.fetchone()
    if result_from_personal is None:
        return render_template('404.html')
    cur.execute("SELECT * FROM projects")
    result_from_projects = cur.fetchall()
    cur.close()
    conn.close()
    data = {
        'name': result_from_personal[1],
        'bio': result_from_personal[2],
        'location': result_from_personal[3],
        'email': result_from_personal[4],
        'picture': result_from_personal[5]
    }
    projects = []
    for project in result_from_projects:
        projects.append({
            'name': project[1],
            'demo_url': project[2],
            'image': project[3],
            'description': project[4]
        })
    data['projects'] = projects
    return render_template('homepage/home.html', data=data, name=data['name'])