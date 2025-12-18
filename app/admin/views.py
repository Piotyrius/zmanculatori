from __future__ import annotations

from sqladmin import ModelView

from ..db.models import (
    User,
    Organization,
    OrganizationMember,
    Subscription,
    Project,
    Pattern,
    PatternResult,
    DraftingSchool,
    BlockConfig,
    RuleGraphConfigModel,
    TransformPipelineConfigModel,
    SizeProfileConfigModel,
    EaseProfileConfigModel,
    SeamAllowanceProfileConfigModel,
    ConfigAuditLog,
)


class UserAdmin(ModelView, model=User):  # type: ignore[misc]
    column_list = [User.id, User.email, User.is_admin, User.created_at]
    column_searchable_list = [User.email]


class OrganizationAdmin(ModelView, model=Organization):  # type: ignore[misc]
    column_list = [Organization.id, Organization.name, Organization.owner_id, Organization.created_at]


class OrganizationMemberAdmin(ModelView, model=OrganizationMember):  # type: ignore[misc]
    column_list = [OrganizationMember.id, OrganizationMember.organization_id, OrganizationMember.user_id, OrganizationMember.role]


class SubscriptionAdmin(ModelView, model=Subscription):  # type: ignore[misc]
    column_list = [Subscription.id, Subscription.user_id, Subscription.tier, Subscription.valid_until]


class ProjectAdmin(ModelView, model=Project):  # type: ignore[misc]
    column_list = [Project.id, Project.name, Project.owner_user_id, Project.owner_org_id, Project.created_at]


class PatternAdmin(ModelView, model=Pattern):  # type: ignore[misc]
    column_list = [Pattern.id, Pattern.project_id, Pattern.block_type, Pattern.status, Pattern.created_at]


class PatternResultAdmin(ModelView, model=PatternResult):  # type: ignore[misc]
    column_list = [PatternResult.id, PatternResult.pattern_id, PatternResult.created_at]


class DraftingSchoolAdmin(ModelView, model=DraftingSchool):  # type: ignore[misc]
    column_list = [DraftingSchool.id, DraftingSchool.name, DraftingSchool.version, DraftingSchool.is_active, DraftingSchool.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class BlockConfigAdmin(ModelView, model=BlockConfig):  # type: ignore[misc]
    column_list = [BlockConfig.id, BlockConfig.name, BlockConfig.version, BlockConfig.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class RuleGraphConfigAdmin(ModelView, model=RuleGraphConfigModel):  # type: ignore[misc]
    column_list = [RuleGraphConfigModel.id, RuleGraphConfigModel.name, RuleGraphConfigModel.version, RuleGraphConfigModel.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class TransformPipelineConfigAdmin(ModelView, model=TransformPipelineConfigModel):  # type: ignore[misc]
    column_list = [TransformPipelineConfigModel.id, TransformPipelineConfigModel.name, TransformPipelineConfigModel.version, TransformPipelineConfigModel.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class SizeProfileConfigAdmin(ModelView, model=SizeProfileConfigModel):  # type: ignore[misc]
    column_list = [SizeProfileConfigModel.id, SizeProfileConfigModel.name, SizeProfileConfigModel.version, SizeProfileConfigModel.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class EaseProfileConfigAdmin(ModelView, model=EaseProfileConfigModel):  # type: ignore[misc]
    column_list = [EaseProfileConfigModel.id, EaseProfileConfigModel.name, EaseProfileConfigModel.version, EaseProfileConfigModel.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class SeamAllowanceProfileConfigAdmin(ModelView, model=SeamAllowanceProfileConfigModel):  # type: ignore[misc]
    column_list = [SeamAllowanceProfileConfigModel.id, SeamAllowanceProfileConfigModel.name, SeamAllowanceProfileConfigModel.version, SeamAllowanceProfileConfigModel.created_at]
    can_create = False
    can_edit = False
    can_delete = False


class ConfigAuditLogAdmin(ModelView, model=ConfigAuditLog):  # type: ignore[misc]
    column_list = [ConfigAuditLog.id, ConfigAuditLog.resource_type, ConfigAuditLog.resource_id, ConfigAuditLog.action, ConfigAuditLog.created_at]
    can_create = False
    can_edit = False
    can_delete = False










