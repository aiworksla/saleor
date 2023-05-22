# Generated by Django 3.2.16 on 2023-01-09 10:42

from django.db import migrations


FIX_CONSTRAINTS = """
ALTER TABLE app_app_permissions
    DROP CONSTRAINT IF EXISTS account_app_permissions_app_id_a360b5e0_fk_account_app_id;

ALTER TABLE app_app_permissions
    DROP CONSTRAINT IF EXISTS app_app_permissions_app_id_5941597d_fk_app_app_id;

ALTER TABLE app_app_permissions
    ADD CONSTRAINT app_app_permissions_app_id_5941597d_fk_app_app_id
    FOREIGN KEY (app_id) REFERENCES app_app(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE app_app_permissions
    RENAME CONSTRAINT account_serviceaccount_p_serviceaccount_id_permis_1686b2ab_uniq
    TO app_app_permissions_app_id_permission_id_0e940a82_uniq;

ALTER TABLE app_app_permissions
    RENAME CONSTRAINT account_serviceaccount_permissions_pkey
    TO app_app_permissions_pkey;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_auto_20221122_1148"),
    ]

    operations = [
        migrations.RunSQL(FIX_CONSTRAINTS, reverse_sql=migrations.RunSQL.noop),
    ]
