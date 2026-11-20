/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PivotRenderer } from "@web/views/pivot/pivot_renderer";
import { pivotView } from "@web/views/pivot/pivot_view";

export class ProjectReportPivotRenderer extends PivotRenderer {
    onOpenView(cell) {
        if (cell.value === undefined) {
            return;
        }
        let projectId = null;
        if (cell.groupId && cell.groupId[0] && cell.groupId[0][0]) {
            projectId = cell.groupId[0][0];
        }
        if (!projectId) {
            return;
        }
        this.actionService.doAction({
            name: "Project Individual Report",
            res_model: "project.cost.report.type",
            type: "ir.actions.act_window",
            views: [[false, "pivot"]],
            view_mode: "pivot",
            context: {
                search_default_project_id: projectId,
            },
        });
    }
}

const projectReportPivotView = Object.assign({}, pivotView, {
    Renderer: ProjectReportPivotRenderer,
});

registry.category("views").add("project_report_pivot", projectReportPivotView);

export class ProjectIndividualReportPivotRenderer extends PivotRenderer {
    onOpenView(cell) {
        if (cell.value === undefined) {
            return;
        }
        const rowValues = (cell.groupId && cell.groupId[0]) || [];
        const projectId = rowValues[0];
        const recordType = rowValues[1];
        if (!projectId || !recordType) {
            return;
        }
        if (recordType === "task") {
            this.actionService.doAction({
                name: "Project Task Report",
                res_model: "project.cost.report.task",
                type: "ir.actions.act_window",
                views: [[false, "pivot"]],
                view_mode: "pivot",
                context: {
                    search_default_project_id: projectId,
                },
            });
        } else if (recordType === "mo") {
            this.actionService.doAction({
                name: "Project MO Report",
                res_model: "project.cost.report.production",
                type: "ir.actions.act_window",
                views: [[false, "pivot"]],
                view_mode: "pivot",
                context: {
                    search_default_project_id: projectId,
                },
            });
        }
    }
}

const projectIndividualReportPivotView = Object.assign({}, pivotView, {
    Renderer: ProjectIndividualReportPivotRenderer,
});

registry
    .category("views")
    .add("project_individual_report_pivot", projectIndividualReportPivotView);
