"""init with project, user and category

Revision ID: c37b749781d5
Revises: 
Create Date: 2024-03-01 04:54:38.129838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.hashing import Hasher


# revision identifiers, used by Alembic.
revision: str = 'c37b749781d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    category_table = op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=False)
    op.create_index(op.f('ix_category_url'), 'category', ['url'], unique=True)
    user_table = op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_card', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_id_card'), 'user', ['id_card'], unique=True)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    project_table = op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('donated', sa.Float(), nullable=True),
    sa.Column('goal', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
    op.create_index(op.f('ix_project_title'), 'project', ['title'], unique=False)
    # ### end Alembic commands ###


    op.bulk_insert(category_table, [
        {
            "name": "Comunidades de bajos recursos",
            "description": "Comunidades que necesitan de algún recurso o apoyo del resto de comunidades para un fin en concreto.",
            "url": "bajos-recursos",
        },
        {
            "name": "Educación y cultura",
            "description": "Aportes para el apoyo a la educación y la cultura en una sociedad que cada vez necesita más estos medios.",
            "url": "educacion-y-cultura",
        },
        {
            "name": "Personas",
            "description": "Personas con algún problema puntual importante que requiere apoyo y recursos para poder superar una situación díficil.",
            "url": "personas",
        },
        {
            "name": "Personas sin hogar",
            "description": "Peronas en situación de calle o de muy bajos recursos, necesitadas de colaboración para poder subsistir de una forma más humana.",
            "url": "personas-sin-hogar",
        },
        {
            "name": "Emergencias",
            "description": "Situaciones imprevistas necesitadas de apoyo social y recursos puntuales de forma urgente.",
            "url": "emergencias",
        },
        {
            "name": "Organizaciones no gubernamentales",
            "description": "Organizaciones que no son parte de las esferas gubernamentales o empresas, cuyo fin fundamental es el bien social.",
            "url": "ong",
        },
    ])

    op.bulk_insert(user_table, [
        {
            "id_card": "0000000",
            "name": "Admin",
            "email": "example@mail.com",
            "password": Hasher.get_password_hash("admin"),
            "is_superuser": True,
            "is_active": True,
        }
    ])

    op.bulk_insert(project_table, [
        {
            "title": "Plataforma Crowdfunding",
            "description": "Proyecto que representa a la aplicación actual, para habilitar la contribución en forma de donaciones a esta pequeña iniciativa.",
            "donated": 0,
            "goal": 0,
            "user_id": 1,
            "category_id": 6,
        },
    ])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_title'), table_name='project')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_id_card'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_category_url'), table_name='category')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
