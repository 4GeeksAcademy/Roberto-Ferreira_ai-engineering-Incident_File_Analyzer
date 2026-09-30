const test = require('node:test');
const assert = require('node:assert/strict');

const { normalizeStatus, normalizeStage, summarizePipeline } = require('./candidate-labels.js');

test('normalizeStatus converts raw API values to readable labels', () => {
  assert.equal(normalizeStatus('in_progress'), 'In progress');
  assert.equal(normalizeStatus('discarded'), 'Discarded');
  assert.equal(normalizeStatus('unknown'), 'unknown');
});

test('normalizeStage converts raw API values to readable labels', () => {
  assert.equal(normalizeStage('personal_interview'), 'Personal interview');
  assert.equal(normalizeStage('offer_presented'), 'Offer presented');
  assert.equal(normalizeStage('unknown'), 'unknown');
});

test('summarizePipeline counts status and stage values', () => {
  const summary = summarizePipeline([
    { status: 'received', stage: 'pending' },
    { status: 'in_progress', stage: 'personal_interview' },
    { status: 'discarded', stage: 'review' },
  ]);

  assert.equal(summary.total, 3);
  assert.equal(summary.byStatus.received, 1);
  assert.equal(summary.byStatus.in_progress, 1);
  assert.equal(summary.byStatus.discarded, 1);
  assert.equal(summary.byStage.personal_interview, 1);
});
