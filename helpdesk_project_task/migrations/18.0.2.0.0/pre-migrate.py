from odoo.tools import sql


def migrate(cr, version):
    """Create task_id and migrate the first linked task from the old
    many2many relation."""
    if not sql.table_exists(cr, "helpdesk_ticket_project_task_rel"):
        return

    if not sql.column_exists(cr, "helpdesk_ticket", "task_id"):
        cr.execute("ALTER TABLE helpdesk_ticket ADD COLUMN task_id INTEGER")

    cr.execute(
        """
        UPDATE helpdesk_ticket t
        SET task_id = rel.task_id
        FROM (
            SELECT DISTINCT ON (ticket_id) ticket_id, task_id
            FROM helpdesk_ticket_project_task_rel
            ORDER BY ticket_id, task_id
        ) rel
        WHERE t.id = rel.ticket_id
        """
    )
