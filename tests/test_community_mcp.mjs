import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import test from "node:test";
import { createCommunityServer } from "../server/community-mcp.mjs";

const bytes = readFileSync(new URL("../docs/questions.json", import.meta.url));
const revision = createHash("sha256").update(bytes).digest("hex");
const handler = createCommunityServer(JSON.parse(bytes), revision);
const request = (message, extra = {}) => new Request("https://gorptastic.com/mcp", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json, text/event-stream", ...extra }, body: typeof message === "string" ? message : JSON.stringify(message) });
const rpc = (method, params = {}, id = 1) => ({ jsonrpc: "2.0", id, method, params });
async function call(name, args) { return (await (await handler(request(rpc("tools/call", { name, arguments: args })))).json()).result; }

test("initialization, notification, discovery and source context work over HTTP", async () => {
  const init = await (await handler(request(rpc("initialize", { protocolVersion: "2025-11-25", capabilities: {}, clientInfo: { name: "independent-protocol-check", version: "1" } })))).json();
  assert.equal(init.result.protocolVersion, "2025-11-25");
  const notification = await handler(request({ jsonrpc: "2.0", method: "notifications/initialized" }));
  assert.equal(notification.status, 202);
  assert.equal(await notification.text(), "");
  const list = await (await handler(request(rpc("tools/list")))).json();
  assert.deepEqual(list.result.tools.map((tool) => tool.name), ["find_open_tasks", "get_evidence_context", "get_task_contract"]);
  assert.ok(list.result.tools.every((tool) => tool.annotations.readOnlyHint));
  const context = await call("get_evidence_context", { question_id: "g-001", expected_revision: revision });
  assert.equal(context.isError, false);
  assert.equal(context.structuredContent.source_bodies_fetched, false);
  assert.match(context.structuredContent.question.known, /80%/);
  assert.match(context.structuredContent.question.known, /30%/);
});

test("capability matching and pinned contracts preserve proposed work and caller authority", async () => {
  const found = await call("find_open_tasks", { capabilities: ["formal_proof"] });
  assert.deepEqual(found.structuredContent.tasks.map((task) => task.question_id), ["g-004"]);
  assert.equal(found.structuredContent.tasks[0].effort_estimate_minutes, null);
  const contract = await call("get_task_contract", { question_id: "g-004", expected_revision: revision, effort_minutes: 10 });
  assert.equal(contract.structuredContent.contract_id, "g-004@" + revision);
  assert.equal(contract.structuredContent.state, "draft_contribution_task");
  assert.equal(contract.structuredContent.caller_effort_limit_minutes, 10);
  assert.equal(contract.structuredContent.publication.state, "draft_not_submitted");
  assert.match(contract.structuredContent.authority, /grants no/);
  assert.equal((await call("get_task_contract", { question_id: "g-004", expected_revision: "0".repeat(64) })).isError, true);
  assert.equal((await call("get_evidence_context", { question_id: "g-999" })).isError, true);
  const unknown = await (await handler(request(rpc("tools/call", { name: "submit_contribution", arguments: {} })))).json();
  assert.equal(unknown.error.code, -32602);
  const nullArgs = await (await handler(request(rpc("tools/call", { name: "find_open_tasks", arguments: null })))).json();
  assert.equal(nullArgs.error.code, -32602);
  assert.match(contract.structuredContent.acceptance_state, /pinned toolchain/);
  assert.equal((await call("find_open_tasks", { limit: 0 })).isError, true);
  assert.equal((await call("find_open_tasks", { execute: true })).isError, true);
});

test("transport rejects hostile origins, unsupported versions, malformed and oversized requests", async () => {
  assert.equal((await handler(request(rpc("tools/list"), { Origin: "https://untrusted.example" }))).status, 403);
  assert.equal((await handler(request(rpc("tools/list"), { "MCP-Protocol-Version": "invalid" }))).status, 400);
  assert.equal((await handler(request("not json"))).status, 400);
  assert.equal((await handler(request("x".repeat(65537)))).status, 400);
  assert.equal((await handler(request([rpc("tools/list")]))).status, 400);
  for (const version of ["2025-03-26", "2025-06-18", "2025-11-25"]) {
    const badResponse = await handler(request("not json", { "MCP-Protocol-Version": version }));
    const bad = await badResponse.json();
    assert.equal(badResponse.status, 400);
    assert.equal(Object.hasOwn(bad, "id"), false);
    assert.equal(bad.jsonrpc, version === "2025-11-25" ? "2.0" : undefined);
    const recoverable = await (await handler(request({ jsonrpc: "2.0", id: 37, params: {} }, { "MCP-Protocol-Version": version }))).json();
    assert.equal(recoverable.id, 37);
    assert.equal(recoverable.error.code, -32600);
  }
  assert.equal((await handler(new Request("https://gorptastic.com/mcp"))).status, 405);
  const snapshot = JSON.parse(bytes);
  const isolated = createCommunityServer(snapshot, revision);
  snapshot.questions[0].known = "changed after construction";
  const result = await (await isolated(request(rpc("tools/call", { name: "get_evidence_context", arguments: { question_id: "g-001" } })))).json();
  assert.match(result.result.structuredContent.question.known, /80%/);
});
