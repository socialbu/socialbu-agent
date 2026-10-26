import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';

const workflow = JSON.parse(readFileSync(new URL('./workflow.json', import.meta.url)));
const now = Date.parse('2026-10-26T12:00:00Z');
class TestDate extends Date {
  constructor(...args) { super(...(args.length ? args : [now])); }
  static now() { return now; }
}
const account = { id: 123, name: 'Example account', post_media_required: false };
const headers = ['row_id', 'account_id', 'team_id', 'content', 'media_url', 'publish_at', 'options_json', 'status', 'socialbu_post_id', 'result', 'attempted_at'];
const row = {
  row_id: 'post-001', account_id: '123', team_id: '', content: 'A real approved caption.',
  media_url: '', publish_at: '2026-10-27T09:30:00+05:00', options_json: '', status: 'approved',
  socialbu_post_id: '', result: '', attempted_at: '',
};
function run(name, input, context = {}) {
  const code = workflow.nodes.find(node => node.name === name).parameters.jsCode;
  if (name === 'Prepare row' && !input[0]?.body) {
    input = [{ statusCode: 200, body: { values: [headers, ...input.map(row => headers.map(key => row[key] ?? ''))] } }];
  }
  const values = {
    Settings: { preview_only: true },
    'Connected accounts': { statusCode: 200, body: [account] },
    ...context,
  };
  return new Function('$input', '$', 'Date', code)(
    { all: () => input.map(json => ({ json })), first: () => ({ json: input[0] }) },
    name => ({ first: () => ({ json: values[name] }) }), TestDate,
  ).map(item => item.json);
}
function prepare(overrides = {}, context = {}) { return run('Prepare row', [{ ...row, ...overrides }], context)[0]; }
const prepared = prepare();
function outcome(overrides = {}, responseOverrides = {}) {
  return run('Record outcome', [{
    statusCode: 200,
    body: { success: true, posts: [{
      id: 456, account_id: 123, publish_at: prepared.request.publish_at,
      draft: false, published: false, approved: true, ...overrides,
    }] }, ...responseOverrides,
  }], { 'Prepare row': prepared })[0];
}

test('converts an explicit timezone to UTC without changing approved copy', () => {
  assert.equal(prepared.request.publish_at, '2026-10-27 04:30:00');
  assert.equal(prepared.request.content, row.content);
  assert.deepEqual(prepared.request.accounts, [123]);
  assert.equal(prepared.request.draft, false);
  assert.equal(prepared.preview_only, true);
  assert.equal(prepared.status, 'processing');
  assert.equal(prepare({ publish_at: '2026-10-27T09:30:00-07:00' }).request.publish_at, '2026-10-27 16:30:00');
});
test('rejects ambiguous, impossible, past, and too-soon dates', () => {
  for (const value of ['tomorrow', '2026-10-27 09:30:00', '2026-10-27T09:30:00', '2027-02-29T09:30:00Z', '2026-10-27T24:00:00Z', '2026-10-27T09:30:00+15:00', '2026-10-27T09:30:00+14:01', '2026-10-26T12:14:59Z', '2026-01-01T09:30:00Z']) {
    assert.equal(prepare({ publish_at: value }).status, 'needs_fix', value);
  }
  assert.equal(prepare({ publish_at: '2028-02-29T09:30:00Z' }).status, 'processing');
});
test('requires explicit approval, skips recorded IDs, and picks only one row', () => {
  const rows = [
    { ...row, row_id: 'draft', status: 'draft' },
    { ...row, row_id: 'saved', socialbu_post_id: '1234' },
    { ...row, row_id: 'first', status: ' Approved ' },
    { ...row, row_id: 'second' },
  ];
  assert.equal(run('Prepare row', rows)[0].row_id, 'first');
  for (const status of ['processing', 'needs_review', 'scheduled', 'awaiting_approval', 'media_error', 'needs_fix']) {
    assert.deepEqual(run('Prepare row', [{ ...row, status }]), []);
  }
  assert.deepEqual(run('Prepare row', []), []);
});
test('duplicate or absent IDs and damaged headers stop before writes', () => {
  assert.throws(() => run('Prepare row', [row, { ...row, status: 'draft' }]), /Duplicate row_id/);
  assert.throws(() => prepare({ row_id: '' }), /unique row_id/);
  assert.throws(() => prepare({ row_id: ' spaced ' }), /surrounding spaces/);
  const broken = headers.filter(key => key !== 'result');
  assert.throws(() => run('Prepare row', [{ statusCode: 200, body: { values: [broken] } }]), /headers/);
  assert.equal(run('Prepare row', [{ statusCode: 200, body: { values: [headers, headers.slice(0, 8).map(key => row[key])] } }])[0].status, 'processing');
});
test('requires valid credentials, account IDs, and unambiguous team selection', () => {
  for (const id of ['other', '123.5', '999', '9007199254740993']) assert.equal(prepare({ account_id: id }).status, 'needs_fix');
  assert.throws(() => prepare({}, { 'Connected accounts': { statusCode: 401, body: {} } }), /accounts/);
  const shared = { 'Connected accounts': { statusCode: 200, body: [{ ...account, team_id: 77 }] } };
  assert.equal(prepare({}, shared).status, 'needs_fix');
  assert.equal(prepare({ team_id: '77' }, shared).request.team_id, 77);
  assert.equal(prepare({ team_id: '78' }, shared).status, 'needs_fix');
  assert.throws(() => prepare({}, { Settings: { preview_only: 'false' } }), /boolean/);
});
test('validates required media, approved content, and network options', () => {
  assert.equal(prepare({ content: ' ' }).status, 'needs_fix');
  assert.equal(prepare({ media_url: 'https://drive.google.com/file/d/example/view' }).status, 'needs_fix');
  for (const media_url of ['file:///secret', 'https://user:pass@example.com/image.jpg', 'not a url']) assert.equal(prepare({ media_url }).status, 'needs_fix');
  assert.equal(prepare({}, { 'Connected accounts': { statusCode: 200, body: [{ ...account, post_media_required: true }] } }).status, 'needs_fix');
  assert.equal(prepare({ media_url: 'https://example.com/image.jpg' }).status, 'processing');
  for (const options_json of ['[]', 'null', '"text"', '{broken']) assert.equal(prepare({ options_json }).status, 'needs_fix');
  assert.deepEqual(prepare({ options_json: '{"some_network_option":true}' }).request.options, { some_network_option: true });
});
test('media failures never become permission to create a post', () => {
  const context = { 'Prepare row': prepared };
  for (const response of [{ error: 'timeout' }, { statusCode: 200, body: {} }, { statusCode: 400, body: { success: false } }]) {
    const result = run('Check media', [response], context)[0];
    assert.equal(result.status, 'media_error');
    assert.equal(result.upload_token, undefined);
  }
  assert.equal(run('Check media', [{ statusCode: 200, body: { success: true, upload_token: 'test-only' } }], context)[0].upload_token, 'test-only');
});
test('records acceptance separately from team approval or publishing', () => {
  assert.equal(outcome().status, 'scheduled');
  assert.equal(outcome().socialbu_post_id, '456');
  assert.equal(outcome({ approved: false }).status, 'awaiting_approval');
  for (const override of [{ account_id: 999 }, { published: true }, { draft: true }, { publish_at: 'wrong' }, { approved: undefined }]) {
    assert.equal(outcome(override).status, 'needs_review');
    assert.equal(outcome(override).socialbu_post_id, '456');
  }
});
test('unknown create outcomes require review and preserve any returned post ID', () => {
  for (const response of [{ error: 'timeout', body: undefined }, { statusCode: 500 }, { body: { success: true, posts: [] } }, { body: { success: false } }]) {
    assert.equal(outcome({}, response).status, 'needs_review');
  }
  assert.equal(outcome({}, { statusCode: 500 }).socialbu_post_id, '456');
});
test('export is inactive, preview-first, uses stored auth, and never retries creates', () => {
  assert.equal(workflow.active, false);
  assert.equal(JSON.parse(workflow.nodes.find(n => n.name === 'Settings').parameters.jsonOutput).preview_only, true);
  assert.equal(workflow.settings.saveExecutionProgress, false);
  for (const node of workflow.nodes.filter(n => n.parameters.genericAuthType === 'httpHeaderAuth')) {
    assert.equal(node.parameters.genericAuthType, 'httpHeaderAuth');
    assert.match(node.parameters.url, /^https:\/\/socialbu\.com\/api\/v1\//);
    assert.equal(node.retryOnFail, false);
    assert.equal(node.parameters.options.redirect.redirect.followRedirects, false);
    assert.equal(node.credentials, undefined);
  }
  const names = new Set(workflow.nodes.map(n => n.name));
  for (const [source, connection] of Object.entries(workflow.connections)) {
    assert.ok(names.has(source));
    for (const branch of connection.main) for (const target of branch) assert.ok(names.has(target.node));
  }
  for (const node of workflow.nodes.filter(n => n.parameters.operation === 'update')) {
    assert.deepEqual(node.parameters.columns.matchingColumns, ['row_id']);
    assert.equal(node.parameters.options.cellFormat, 'RAW');
    assert.deepEqual(Object.keys(node.parameters.columns.value), ['row_id', 'status', 'socialbu_post_id', 'result', 'attempted_at']);
  }
});
