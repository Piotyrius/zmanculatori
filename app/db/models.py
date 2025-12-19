from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user")
    measurement_profiles: Mapped[list["MeasurementProfile"]] = relationship(
        back_populates="owner_user"
    )
    projects: Mapped[list["Project"]] = relationship(back_populates="owner_user")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class OrganizationMember(Base):
    __tablename__ = "organization_members"
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(64), nullable=False, default="member")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tier: Mapped[str] = mapped_column(String(64), nullable=False)
    capabilities_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(back_populates="subscriptions")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    owner_org_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="active"
    )  # active, archived

    owner_user: Mapped[Optional[User]] = relationship(back_populates="projects")


class MeasurementProfile(Base):
    __tablename__ = "measurement_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(
        String(64), nullable=False, default="womenswear"
    )  # womenswear, menswear, childrenswear, etc.
    unit: Mapped[str] = mapped_column(String(16), nullable=False, default="mm")
    values_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    owner_user: Mapped[User] = relationship(back_populates="measurement_profiles")


class Pattern(Base):
    __tablename__ = "patterns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    block_type: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_api_version: Mapped[str] = mapped_column(String(16), nullable=False)
    config_version_bundle_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False
    )
    canonical_request_hash: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    version_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class PatternResult(Base):
    __tablename__ = "pattern_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pattern_id: Mapped[int] = mapped_column(ForeignKey("patterns.id"), nullable=False)
    geometry_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True
    )  # optional, may store summary only
    exports_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class DraftingSchool(Base):
    __tablename__ = "drafting_schools"
    __table_args__ = (
        Index("idx_drafting_schools_name_version", "name", "version"),
        Index("idx_drafting_schools_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # For extensibility
    engine_min_version: Mapped[Optional[str]] = mapped_column(String(16))
    engine_max_version: Mapped[Optional[str]] = mapped_column(String(16))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class BlockConfig(Base):
    __tablename__ = "blocks"
    __table_args__ = (
        Index("idx_blocks_name_version", "name", "version"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # For extensibility
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class RuleGraphConfigModel(Base):
    __tablename__ = "rule_graphs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # For extensibility
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class TransformPipelineConfigModel(Base):
    __tablename__ = "transform_pipelines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # For extensibility
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class SizeProfileConfigModel(Base):
    __tablename__ = "size_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class EaseProfileConfigModel(Base):
    __tablename__ = "ease_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # For extensibility
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class SeamAllowanceProfileConfigModel(Base):
    __tablename__ = "seam_allowance_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class EducationalContent(Base):
    __tablename__ = "educational_content"
    __table_args__ = (
        Index("idx_educational_content_school", "drafting_school_id", "drafting_school_version"),
        Index("idx_educational_content_block", "block_id", "block_version"),
        Index("idx_educational_content_type", "content_type"),
        Index("idx_educational_content_priority", "priority"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(64), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Markdown content
    language: Mapped[str] = mapped_column(String(8), nullable=False, default="en")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Links to related resources (optional)
    drafting_school_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("drafting_schools.id")
    )
    drafting_school_version: Mapped[Optional[str]] = mapped_column(String(32))
    block_id: Mapped[Optional[int]] = mapped_column(ForeignKey("blocks.id"))
    block_version: Mapped[Optional[str]] = mapped_column(String(32))
    measurement_name: Mapped[Optional[str]] = mapped_column(String(64))
    
    metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class MeasurementCategory(Base):
    __tablename__ = "measurement_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class GradingTableConfig(Base):
    __tablename__ = "grading_tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    config_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    content_metadata_jsonb: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    drafting_school_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("drafting_schools.id")
    )
    drafting_school_version: Mapped[Optional[str]] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class ConfigAuditLog(Base):
    __tablename__ = "config_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    old_payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    new_payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class ApiToken(Base):
    __tablename__ = "api_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    scopes_jsonb: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )




