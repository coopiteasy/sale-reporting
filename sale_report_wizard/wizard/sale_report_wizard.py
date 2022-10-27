import ast

from odoo import api, fields, models


class SaleReportWizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "Sales Report Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    filter_date_type = fields.Selection(
        [("confirmation_date", "Confirmation_date (keep only confirmed orders)"), 
        ("date_order", "Order Date")],
        default="confirmation_date",
        string="Filter by",
    )

    report = fields.Many2one("sale.reports.config", string="Preset Report")

    @api.multi
    def button_show(self):
        self.ensure_one()

        view_id = self.env.ref(self.report.view).id
        search_view_id = ""
        if self.report.search_view:
            search_view_id = self.env.ref(self.report.search_view).id

        domain = []

        # sale.report name date_order as date,
        # while report.all.channel.sale and sale.order 
        # name it as date_order
        filter_date_type = self.filter_date_type
        if (filter_date_type == "date_order" and 
            self.report.model == "sale.report"):
            filter_date_type = "date"

        # convert string representation of domain to domain
        # in place conversion of self.report.domain is impossible,
        # so we create a new obect domain
        if self.report.domain:
            domain = ast.literal_eval(self.report.domain)
        if self.filter_date_type and self.start_date and self.end_date:
            domain += [
                (filter_date_type, ">=", self.start_date),
                (filter_date_type, "<=", self.end_date),
            ]

        return {
            "name": "Sale Report",
            "type": "ir.actions.act_window",
            "res_model": self.report.model,
            "view_mode": self.report.view_mode,
            "views": [(view_id, self.report.view_mode)],
            "domain": domain,
            "limit": self.report.limit,
            "search_view_id": search_view_id,
        }
