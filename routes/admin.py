from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..routes.auth import login_required
from ..db import get_connection
import base64
 
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
 
# @admin_bp.get('/')
# @login_required
# def admin():
#    return render_template('admin/admin.html')

@admin_bp.get('/')
@login_required
def admin():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT full_name FROM personal_info WHERE info_id = 1')
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    name = row[0] if row else "Admin"
    return render_template('admin/admin.html', name=name)


@admin_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        error = None
        data_uri = None
        full_name = request.form['full_name']
        bio = request.form['bio']
        location = request.form['location']
        email = request.form['email']
        picture = request.files['picture']


        if (error is None):
            conn = get_connection()
            cur = conn.cursor()
            if (data_uri is None):
                cur.execute(
                    '''
               INSERT INTO personal_info (info_id, full_name, bio, location, email)
               VALUES (1, %s, %s, %s, %s)
               ON CONFLICT (info_id)
               DO UPDATE SET
                  full_name = EXCLUDED.full_name,
                  bio = EXCLUDED.bio,
                  location = EXCLUDED.location,
                  email = EXCLUDED.email
               ''',
                    (full_name, bio, location, email)
                )
            else:
                cur.execute(
                    '''
               INSERT INTO personal_info (info_id,full_name, bio, location, email, picture)
               VALUES (1, %s, %s, %s, %s, %s)
               ON CONFLICT (info_id)
               DO UPDATE SET
                  full_name = EXCLUDED.full_name,
                  bio = EXCLUDED.bio,
                  location = EXCLUDED.location,
                  email = EXCLUDED.email,
                  picture = EXCLUDED.picture
               ''',
                    (full_name, bio, location, email, data_uri)
                )
            conn.commit()
            cur.close()
            conn.close()
        else:
            flash(error)
        return redirect(url_for('admin.edit_profile'))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM personal_info WHERE info_id = 1")
    result = cur.fetchone()
    cur.close()
    conn.close()

    data = {}
    if result:
        data = {
            'full_name': result[1],
            'bio': result[2],
            'location': result[3],
            'email': result[4],
            'picture': result[5]
        }

    return render_template('admin/edit-profile.html', data=data)

    
# @admin_bp.route('/edit-projects')
# @login_required
# def edit_projects():
#    return render_template('admin/edit-projects.html')

@admin_bp.route('/edit-projects')
@login_required
def edit_projects():
   conn = get_connection()
   cur = conn.cursor()
   cur.execute("SELECT * FROM projects")
   result_from_projects = cur.fetchall()
   cur.close()
   conn.close()
   projects = []
   for project in result_from_projects:
      projects.append({
         'id': project[0],
         'name': project[1],
         'demo_url': project[2],
         'image': project[3],
         'description': project[4]
      })
   return render_template('admin/edit-projects.html', projects=projects)

@admin_bp.post('/delete-project/<int:id>')
@login_required
def delete_project(id):
   conn = get_connection()
   cur = conn.cursor()
   cur.execute("DELETE FROM projects WHERE project_id = %s", (id,))
   conn.commit()
   cur.close()
   conn.close()
   return redirect(url_for('admin.edit_projects'))

# @admin_bp.route('/edit-project/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_project(id):
#     if request.method == 'POST':
#         error = None
#         name = request.form['name']
#         demo_url = request.form['demo_url']
#         description = request.form['description']
#         image = request.files['image']
#         if(not name):
#             error = 'Project name is required'
#         elif(not demo_url):
#             error = 'Demo URL is required'
#         elif(not description):
#             error = 'Description is required'
#         elif(not image):
#             error = 'Image is required'
 
#         if image:
#             allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
#             media_type = image.mimetype
#             if(media_type not in allowed_extensions):
#                 error = 'Invalid file type. Please upload an image file'
#             else:
#                 image_bytes = image.read()
#                 if(len(image_bytes) > 5000000):
#                     error = 'Image file is too large. Max size is 5MB'
#                 else:
#                     base64_data = base64.b64encode(image_bytes).decode('utf-8')
#                     data_uri = f"data:image/{media_type};base64,{base64_data}"
        
#         if error is None:
#             conn = get_connection()
#             cur = conn.cursor()
#             if data_uri is None:
#                 cur.execute(
#                 '''
#                 UPDATE projects
#                 SET project_name = %s, demo_url = %s, description = %s
#                 WHERE project_id = %s
#                 ''',
#                 (name, demo_url, description, id)
#             )
#             else:
#                 cur.execute(
#                 '''
#                 UPDATE projects
#                 SET project_name = %s, demo_url = %s, image = %s, description = %s
#                 WHERE project_id = %s
#                 ''',
#                 (name, demo_url, data_uri, description, id)
#             )
#             conn.commit()
#             cur.close()
#             conn.close()
#             return redirect(url_for('admin.edit_projects'))
#    # Existing code for the GET request

#     # GET request: fetch project data by id
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM projects WHERE project_id = %s", (id,))
#     project = cur.fetchone()
#     cur.close()
#     conn.close()

#     if project:
#         project_data = {
#             'id': project[0],
#             'name': project[1],
#             'demo_url': project[2],
#             'image': project[3],
#             'description': project[4]
#         }
#     else:
#         flash("Project not found.")
#         return redirect(url_for('admin.edit_projects'))

#     return render_template('admin/edit-project.html', data=project_data)

@admin_bp.route('/edit-project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    error = None
    data_uri = None

    if request.method == 'POST':
        name = request.form['name']
        demo_url = request.form['demo_url']
        description = request.form['description']
        image = request.files.get('image')

        if not name:
            error = 'Project name is required'
        elif not demo_url:
            error = 'Demo URL is required'
        elif not description:
            error = 'Description is required'

        if image and image.filename != '':
            allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
            media_type = image.mimetype
            if media_type not in allowed_extensions:
                error = 'Invalid file type. Please upload an image file'
            else:
                image_bytes = image.read()
                if len(image_bytes) > 5000000:
                    error = 'Image file is too large. Max size is 5MB'
                else:
                    import base64
                    base64_data = base64.b64encode(image_bytes).decode('utf-8')
                    data_uri = f"data:image/{media_type};base64,{base64_data}"

        if error is None:
            conn = get_connection()
            cur = conn.cursor()
            if data_uri is None:
                cur.execute(
                    '''
                    UPDATE projects
                    SET project_name = %s, demo_url = %s, description = %s
                    WHERE project_id = %s
                    ''',
                    (name, demo_url, description, id)
                )
            else:
                cur.execute(
                    '''
                    UPDATE projects
                    SET project_name = %s, demo_url = %s, image = %s, description = %s
                    WHERE project_id = %s
                    ''',
                    (name, demo_url, data_uri, description, id)
                )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('admin.edit_project', id=id))  # 👈 safer fallback

        else:
            flash(error)

    # GET request
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE project_id = %s", (id,))
    project = cur.fetchone()
    cur.close()
    conn.close()

    if project:
        project_data = {
            'id': project[0],
            'name': project[1],
            'demo_url': project[2],
            'image': project[3],
            'description': project[4]
        }
    else:
        flash("Project not found.")
        return redirect(url_for('admin.edit_projects'))  # This must exist!

    return render_template('admin/edit-project.html', data=project_data)


@admin_bp.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
   if request.method == 'POST':
      error = None
      data_uri = None
      name = request.form['name']
      demo_url = request.form['demo_url']
      description = request.form['description']
      image = request.files['image']
      if(not name):
         error = 'Project name is required'
      elif(not demo_url):
         error = 'Demo URL is required'
      elif(not description):
         error = 'Description is required'
 
      if image:
         allowed_extensions = ['image/jpeg', 'image/png', 'image/jpg']
         media_type = image.mimetype
         if(media_type not in allowed_extensions):
            error = 'Invalid file type. Please upload an image file'
         else:
            image_bytes = image.read()
            if(len(image_bytes) > 5000000):
               error = 'Image file is too large. Max size is 5MB'
            else:
               base64_data = base64.b64encode(image_bytes).decode('utf-8')
               data_uri = f"data:image/{media_type};base64,{base64_data}"
 
      if error is None:
         conn = get_connection()
         cur = conn.cursor()
         cur.execute(
            '''
            INSERT INTO projects (project_name, demo_url, image, description)
            VALUES (%s, %s, %s, %s)
            ''',
            (name, demo_url, data_uri, description)
         )
         conn.commit()
         cur.close()
         conn.close()
         return redirect(url_for('admin.edit_projects'))
      else:
         flash(error)
         return redirect(url_for('admin.add_project'))
   return render_template('admin/add-project.html')
