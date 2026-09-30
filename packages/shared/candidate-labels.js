"use strict";

function normalizeStatus(status) {
  const labels = {
    received: "Received",
    in_progress: "In progress",
    selected: "Selected",
    discarded: "Discarded",
  };

  return labels[status] || status || "Unknown";
}

function normalizeStage(stage) {
  const labels = {
    pending: "Pending review",
    review: "Under review",
    personal_interview: "Personal interview",
    technical_interview: "Technical interview",
    offer_presented: "Offer presented",
  };

  return labels[stage] || stage || "Unknown";
}

function summarizePipeline(candidates = []) {
  const summary = {
    total: candidates.length,
    byStatus: {},
    byStage: {},
  };

  for (const candidate of candidates) {
    const status = candidate?.status || "received";
    const stage = candidate?.stage || "pending";

    summary.byStatus[status] = (summary.byStatus[status] || 0) + 1;
    summary.byStage[stage] = (summary.byStage[stage] || 0) + 1;
  }

  return summary;
}

module.exports = {
  normalizeStatus,
  normalizeStage,
  summarizePipeline,
};
