# This file makes the models directory a Python package
from app.v2.models.project import Project
from app.v2.models.admin import Admin

__all__ = [Project, Admin]