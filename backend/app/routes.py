from flask import Blueprint, request, jsonify
from datetime import datetime, date
from .database import db
from .models import JobApplication

# Create blueprint for API routes
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200


@api.route('/applications', methods=['GET'])
def get_applications():
    """Get all job applications."""
    try:
        applications = JobApplication.query.order_by(JobApplication.application_date.desc()).all()
        return jsonify([app.to_dict() for app in applications]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    """Get a single job application by ID."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        return jsonify(application.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/applications', methods=['POST'])
def create_application():
    """Create a new job application."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('company_name'):
            return jsonify({'error': 'company_name is required'}), 400
        if not data.get('position_title'):
            return jsonify({'error': 'position_title is required'}), 400
        
        # Parse application_date if provided
        application_date = date.today()
        if data.get('application_date'):
            try:
                application_date = datetime.fromisoformat(data['application_date']).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create new application
        application = JobApplication(
            company_name=data['company_name'],
            position_title=data['position_title'],
            location=data.get('location'),
            job_type=data.get('job_type'),
            job_level=data.get('job_level'),
            application_date=application_date,
            status=data.get('status', 'Applied'),
            job_description=data.get('job_description'),
            notes=data.get('notes')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify(application.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/applications/<int:app_id>', methods=['PUT'])
def update_application(app_id):
    """Update an existing job application."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields if provided
        if 'company_name' in data and not data['company_name']:
            return jsonify({'error': 'company_name cannot be empty'}), 400
        if 'position_title' in data and not data['position_title']:
            return jsonify({'error': 'position_title cannot be empty'}), 400
        
        # Update fields
        if 'company_name' in data:
            application.company_name = data['company_name']
        if 'position_title' in data:
            application.position_title = data['position_title']
        if 'location' in data:
            application.location = data['location']
        if 'job_type' in data:
            application.job_type = data['job_type']
        if 'job_level' in data:
            application.job_level = data['job_level']
        if 'status' in data:
            application.status = data['status']
        if 'job_description' in data:
            application.job_description = data['job_description']
        if 'notes' in data:
            application.notes = data['notes']
        if 'application_date' in data:
            try:
                application.application_date = datetime.fromisoformat(data['application_date']).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(application.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/applications/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    """Delete a job application."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Delete associated files if they exist
        if application.resume_path and os.path.exists(application.resume_path):
            try:
                os.remove(application.resume_path)
            except OSError:
                pass # Log error
                
        if application.cover_letter_path and os.path.exists(application.cover_letter_path):
            try:
                os.remove(application.cover_letter_path)
            except OSError:
                pass # Log error
        
        db.session.delete(application)
        db.session.commit()
        
        return jsonify({'message': 'Application deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# --- File Upload Utilities (Phase 2) ---

from werkzeug.utils import secure_filename
from flask import send_file, current_app
import os

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_document(file, app_id, doc_type):
    """Common logic to save a document."""
    if file.filename == '':
        raise ValueError('No selected file')
        
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed')
        
    filename = secure_filename(file.filename)
    # Create unique filename: {app_id}_{timestamp}_{filename}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{app_id}_{timestamp}_{doc_type}_{filename}"
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    return file_path, filename

# --- Resume Endpoints ---

@api.route('/applications/<int:app_id>/resume', methods=['POST'])
def upload_resume(app_id):
    """Upload a resume for an application."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
            
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        
        try:
            file_path, filename = save_document(file, app_id, 'resume')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
        # Delete old file if exists
        if application.resume_path and os.path.exists(application.resume_path):
            try:
                os.remove(application.resume_path)
            except OSError:
                pass

        application.resume_path = file_path
        application.resume_filename = filename
        db.session.commit()
        
        return jsonify(application.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/applications/<int:app_id>/resume', methods=['GET'])
def download_resume(app_id):
    """Download the resume."""
    try:
        application = JobApplication.query.get(app_id)
        if not application or not application.resume_path:
            return jsonify({'error': 'Resume not found'}), 404
            
        if not os.path.exists(application.resume_path):
            return jsonify({'error': 'File not found on server'}), 404
            
        return send_file(
            application.resume_path,
            as_attachment=True,
            download_name=application.resume_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/applications/<int:app_id>/resume', methods=['DELETE'])
def delete_resume(app_id):
    """Delete the resume."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
            
        if application.resume_path and os.path.exists(application.resume_path):
            try:
                os.remove(application.resume_path)
            except OSError:
                pass
                
        application.resume_path = None
        application.resume_filename = None
        db.session.commit()
        
        return jsonify({'message': 'Resume deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- Cover Letter Endpoints ---

@api.route('/applications/<int:app_id>/cover-letter', methods=['POST'])
def upload_cover_letter(app_id):
    """Upload a cover letter."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
            
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        
        try:
            file_path, filename = save_document(file, app_id, 'cover_letter')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
        # Delete old file if exists
        if application.cover_letter_path and os.path.exists(application.cover_letter_path):
            try:
                os.remove(application.cover_letter_path)
            except OSError:
                pass

        application.cover_letter_path = file_path
        application.cover_letter_filename = filename
        db.session.commit()
        
        return jsonify(application.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/applications/<int:app_id>/cover-letter', methods=['GET'])
def download_cover_letter(app_id):
    """Download the cover letter."""
    try:
        application = JobApplication.query.get(app_id)
        if not application or not application.cover_letter_path:
            return jsonify({'error': 'Cover letter not found'}), 404
            
        if not os.path.exists(application.cover_letter_path):
            return jsonify({'error': 'File not found on server'}), 404
            
        return send_file(
            application.cover_letter_path,
            as_attachment=True,
            download_name=application.cover_letter_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/applications/<int:app_id>/cover-letter', methods=['DELETE'])
def delete_cover_letter(app_id):
    """Delete the cover letter."""
    try:
        application = JobApplication.query.get(app_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
            
        if application.cover_letter_path and os.path.exists(application.cover_letter_path):
            try:
                os.remove(application.cover_letter_path)
            except OSError:
                pass
                
        application.cover_letter_path = None
        application.cover_letter_filename = None
        db.session.commit()
        
        return jsonify({'message': 'Cover letter deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
