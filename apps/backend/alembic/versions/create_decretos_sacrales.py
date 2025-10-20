"""create decretos_sacrales table

Revision ID: 001_decretos_sacrales
Revises: 
Create Date: 2025-10-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_decretos_sacrales'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'decretos_sacrales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('momento_liturgico', sa.String(length=20), nullable=True),
        
        # PODER LEGISLATIVO
        sa.Column('direccion_emergente', sa.Text(), nullable=True),
        sa.Column('accion_tangible', sa.Text(), nullable=False),
        sa.Column('validado_contra_pilares', sa.Boolean(), default=False),
        
        # PODER EJECUTIVO
        sa.Column('estado', sa.String(length=20), nullable=True),
        sa.Column('notas_ejecucion', sa.Text(), nullable=True),
        sa.Column('fecha_inicio_ejecucion', sa.DateTime(), nullable=True),
        sa.Column('fecha_fin_ejecucion', sa.DateTime(), nullable=True),
        
        # PODER JUDICIAL
        sa.Column('verificacion_judicial', sa.Text(), nullable=True),
        sa.Column('cumplimiento_score', sa.Integer(), nullable=True),
        sa.Column('sabiduria_extraida', sa.Text(), nullable=True),
        sa.Column('fecha_verificacion', sa.DateTime(), nullable=True),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_decretos_sacrales_fecha'), 'decretos_sacrales', ['fecha'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_decretos_sacrales_fecha'), table_name='decretos_sacrales')
    op.drop_table('decretos_sacrales')

