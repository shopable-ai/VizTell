import test from "node:test";
import assert from "node:assert/strict";
import { bindNewConversationButton } from "../src/project-page.js";

class FakeElement {
  constructor(dataset) {
    this.dataset = { ...(dataset || {}) };
    this.textContent = "";
    this.listeners = new Map();
  }
  addEventListener(type, handler) { this.listeners.set(type, handler); }
  click() {
    const handler = this.listeners.get("click");
    if (handler) handler({ preventDefault() {}, stopPropagation() {} });
  }
}

function createHarness(options = {}) {
  const dataset = { conversationId: "conversation-42" };
  if (!options.omitProjectId) {
    dataset.projectId = options.projectId === undefined ? "project-alpha" : options.projectId;
  }
  const root = new FakeElement(dataset);
  const button = new FakeElement({});
  const status = new FakeElement({});
  const page = Object.freeze({
    href: "https://chatgpt.local/projects/project-alpha/c/conversation-42",
    draft: "unsent draft",
    scrollTop: 240
  });
  const openTabCalls = [];
  bindNewConversationButton({
    root, button, status, page,
    openTab(url) { openTabCalls.push(url); }
  });
  return { root, button, status, page, openTabCalls };
}

test("click opens exactly one independent conversation tab for the current project", () => {
  const h = createHarness();
  h.button.click();
  assert.equal(h.openTabCalls.length, 1);
  const target = new URL(h.openTabCalls[0]);
  assert.equal(target.pathname, "/conversation.html");
  assert.equal(target.searchParams.get("projectId"), "project-alpha");
  assert.equal(target.searchParams.get("mode"), "new");
});

test("opening a tab does not mutate the original page state", () => {
  const h = createHarness();
  const before = {
    href: h.page.href,
    conversationId: h.root.dataset.conversationId,
    draft: h.page.draft,
    scrollTop: h.page.scrollTop
  };
  h.button.click();
  assert.equal(h.openTabCalls.length, 1, "the state-preservation assertion must not pass when no tab was opened");
  assert.deepEqual({
    href: h.page.href,
    conversationId: h.root.dataset.conversationId,
    draft: h.page.draft,
    scrollTop: h.page.scrollTop
  }, before);
});

test("missing project identity fails closed and gives feedback", () => {
  const h = createHarness({ omitProjectId: true });
  h.button.click();
  assert.deepEqual(h.openTabCalls, []);
  assert.equal(h.status.textContent, "未识别当前项目，未打开新标签页");
});

test("empty project identity fails closed and gives feedback", () => {
  const h = createHarness({ projectId: "" });
  h.button.click();
  assert.deepEqual(h.openTabCalls, []);
  assert.equal(h.status.textContent, "未识别当前项目，未打开新标签页");
});

test("project identity with special characters can be recovered from the target URL", () => {
  const h = createHarness({ projectId: "project/a & beta" });
  h.button.click();
  assert.equal(h.openTabCalls.length, 1);
  const target = new URL(h.openTabCalls[0]);
  assert.equal(target.searchParams.get("projectId"), "project/a & beta");
});
