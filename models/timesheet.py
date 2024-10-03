
from odoo import fields, models


class TimeSheet(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = "timesheet"
    _description = "TimeSheet"
    _order = "id asc"

    # ---------------------------------------- Fields Declaration ---------------------------------

    # Basic
    date = fields.Date(required=True, related="task_id.due_date", readonly=False, store=True)

    # date = fields.Date(required=True, compute="_set_date")                       => working, need to know which one is best
    # date = fields.Date(required=True, default=lambda self: self._default_date()) => not working, please could you tell me why?

    description = fields.Text(string="Description")
    time = fields.Integer(string="Time(H)", required=True)

    # Relational
    task_id = fields.Many2one("todo.task")

    # # ---------------------------------------- Compute methods ------------------------------------
    # @api.depends("task_id")
    # def _set_date(self):
    #     for rec in self:
    #         rec.date = rec.task_id.due_date

    # ---------------------------------------- Default Methods ------------------------------------
    # def _default_date(self):
    #     return self.task_id.due_date
