
from dateutil.relativedelta import relativedelta
from odoo import fields, models, exceptions, api


class ToDoTask(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = "todo.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Task"
    _order = "id desc"

    # ---------------------------------------- Fields Declaration ---------------------------------

    # Basic
    name = fields.Char(string="Task Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    due_date = fields.Date(string="Due Date", required=True, tracking=True,
                           default=lambda self: self._default_due_date())

    # Special
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string="Status", default="new")

    # Relational
    assign_to = fields.Many2one("res.partner", string="Assign To", required=True, tracking=True)

    # --------------------------------------- SQL Constraints ----------------------------------
    _sql_constraints = [
        ('unique_task_name', 'UNIQUE(name)', 'Task name must be unique!')
    ]

    # ---------------------------------------- Default Methods ------------------------------------
    def _default_due_date(self):
        return fields.Date.context_today(self) + relativedelta(days=3)

    # ---------------------------------------- Action Methods -------------------------------------
    def todo_task_accept_action_button(self):
        for rec in self:
            if rec.state == "in_progress":
                raise exceptions.UserError("You can't accept In Progress task, already accepted!")
            else:
                rec.state = "in_progress"
        return True

    def todo_task_finish_action_button(self):
        for rec in self:
            if rec.state == "new":
                raise exceptions.UserError("A New task cannot be finished, You must accept it first.")
            else:
                rec.state = "completed"
        return True

    # ------------------------------------------ CRUD Methods -------------------------------------
    @api.model
    def create(self, vals):
        # Check if the partner is assigned to in progress task
        in_progress_partner = self.env['todo.task'].search(
            [('assign_to', '=', vals['assign_to']), ('state', '=', 'in_progress')])
        new_partner = self.env['todo.task'].search(
            [('assign_to', '=', vals['assign_to']), ('state', '=', 'new')])
        if in_progress_partner:
            raise exceptions.ValidationError("The partner has an in progress task, cannot assigned to new one now.")
        if new_partner:
            raise exceptions.ValidationError("The partner has a new waiting task, cannot assigned to new one now.")

        return super().create(vals)

    def unlink(self):
        for rec in self:
            if rec.state not in ['new', 'completed']:
                raise exceptions.UserError("Only New or Completed tasks can be deleted!")
        return super().unlink()
