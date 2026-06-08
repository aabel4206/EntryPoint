from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    student_type = Column(String(50), nullable=False)
    major = Column(String(100), nullable=True)
    is_international = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="student_profile")
    task_completions = relationship("StudentTaskCompletion", back_populates="student_profile")


class ResourceCategory(Base):
    __tablename__ = "resource_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    resources = relationship("Resource", back_populates="category")
    monitored_pages = relationship("MonitoredPage", back_populates="category")


class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("resource_categories.category_id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("ResourceCategory", back_populates="resources")
    checklist_tasks = relationship("ChecklistTask", back_populates="resource")


class ChecklistTemplate(Base):
    __tablename__ = "checklist_templates"

    template_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    student_type = Column(String(50), nullable=False)
    is_international = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("ChecklistTask", back_populates="template")


class ChecklistTask(Base):
    __tablename__ = "checklist_tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("checklist_templates.template_id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.resource_id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), nullable=False, default="medium")
    due_stage = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    template = relationship("ChecklistTemplate", back_populates="tasks")
    resource = relationship("Resource", back_populates="checklist_tasks")
    completions = relationship("StudentTaskCompletion", back_populates="task")


class StudentTaskCompletion(Base):
    __tablename__ = "student_task_completion"

    completion_id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.profile_id"), nullable=False)
    task_id = Column(Integer, ForeignKey("checklist_tasks.task_id"), nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    student_profile = relationship("StudentProfile", back_populates="task_completions")
    task = relationship("ChecklistTask", back_populates="completions")


class MonitoredPage(Base):
    __tablename__ = "monitored_pages"

    page_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("resource_categories.category_id"), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(Text, unique=True, nullable=False)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    category = relationship("ResourceCategory", back_populates="monitored_pages")
    change_logs = relationship("PageChangeLog", back_populates="monitored_page")


class PageChangeLog(Base):
    __tablename__ = "page_change_logs"

    change_id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("monitored_pages.page_id"), nullable=False)
    previous_content_hash = Column(String(255), nullable=True)
    new_content_hash = Column(String(255), nullable=False)
    change_summary = Column(Text, nullable=True)
    importance_level = Column(String(20), nullable=False, default="low")
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by_admin = Column(Boolean, nullable=False, default=False)

    monitored_page = relationship("MonitoredPage", back_populates="change_logs")