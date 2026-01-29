from datetime import datetime, date
from .database import db


class JobApplication(db.Model):
    """Job Application model."""
    
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    position_title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)
    job_level = db.Column(db.String(50), nullable=True)
    application_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(50), nullable=False, default='Applied')
    job_description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'position_title': self.position_title,
            'location': self.location,
            'job_type': self.job_type,
            'job_level': self.job_level,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status,
            'job_description': self.job_description,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<JobApplication {self.id}: {self.position_title} at {self.company_name}>'
