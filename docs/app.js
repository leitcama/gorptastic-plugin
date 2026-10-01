"use strict";

const list = document.querySelector("#problem-list");
const search = document.querySelector("#search");
const count = document.querySelector("#result-count");
const empty = document.querySelector("#empty");
const error = document.querySelector("#load-error");
const areas = [...document.querySelectorAll("[data-area]")];
let selectedArea = "all";
let questions = [];

function node(tag, content, className) {
  const result = document.createElement(tag);
  if (content !== undefined) result.textContent = content;
  if (className) result.className = className;
  return result;
}

function link(label, href, className) {
  const result = node("a", label, className);
  const url = new URL(href, location.href);
  if (url.protocol !== "https:" && url.origin !== location.origin) throw new Error("Unsupported link");
  result.href = url.href;
  return result;
}

function section(title, text) {
  const result = node("section", undefined, "research-section");
  result.append(node("h4", title), node("p", text));
  return result;
}

function renderQuestion(q, index) {
  const article = node("details", undefined, "problem");
  article.id = q.id;
  article.dataset.area = q.area;
  article.dataset.search = [q.title, q.summary, q.area_label, q.known, q.limit, q.task].join(" ").toLowerCase();
  article.open = index === 0;
  const summary = node("summary");
  const top = node("div", undefined, "question-top");
  top.append(node("span", q.id.toUpperCase(), "problem-id"), node("span", q.area_label, "area-label"), node("span", q.status, "state"));
  summary.append(top, node("h3", q.title), node("p", q.summary, "one-line"), node("span", "Read the question and first check", "detail-hint"));
  const body = node("div", undefined, "problem-body");
  body.append(section("What we know", q.known));
  const limit = section("What remains open", q.limit);
  limit.classList.add("scope-limit");
  body.append(limit, section("A useful first contribution", q.task));
  const checkSection = node("section", undefined, "research-section");
  checkSection.append(node("h4", "Proposed check"));
  const grid = node("dl", undefined, "check-grid");
  for (const [key, label] of [["comparison", "Comparison"], ["measure", "Measure"], ["horizon", "Time window"], ["decision_rule", "Decision rule"], ["falsifier", "Falsifier"]]) grid.append(node("dt", label), node("dd", q.check[key]));
  checkSection.append(grid);
  body.append(checkSection);
  const sourceSection = node("section", undefined, "research-section");
  sourceSection.append(node("h4", "Sources and public artifacts"));
  const sources = node("ul", undefined, "sources");
  for (const source of q.sources) {
    const item = node("li");
    item.append(link(source.title, source.url), node("span", source.locator + " · Source date: " + (source.source_date || "unknown") + " · Checked " + q.reviewed_on, "source-meta"));
    sources.append(item);
  }
  sourceSection.append(sources);
  body.append(sourceSection);
  const contribution = new URL("https://github.com/leitcama/gorptastic-plugin/issues/new");
  contribution.searchParams.set("template", "evidence.yml");
  contribution.searchParams.set("title", "[" + q.id.toUpperCase() + "] Evidence or correction");
  body.append(link("Contribute to this question", contribution.href, "contribute-link"), link("Permanent link", "#" + q.id, "permalink"));
  article.append(summary, body);
  return article;
}

function filter() {
  const term = search.value.trim().toLowerCase();
  let shown = 0;
  for (const article of list.children) {
    const matches = (selectedArea === "all" || article.dataset.area === selectedArea) && (!term || article.dataset.search.includes(term));
    article.hidden = !matches;
    if (matches) shown++;
  }
  count.textContent = shown + " of " + questions.length + " questions · Studies proposed; outcomes unverified";
  empty.hidden = shown !== 0;
}

search.addEventListener("input", filter);
for (const button of areas) button.addEventListener("click", () => {
  selectedArea = button.dataset.area;
  for (const candidate of areas) candidate.setAttribute("aria-pressed", String(candidate === button));
  filter();
});
document.querySelector("#clear").addEventListener("click", () => {
  search.value = "";
  selectedArea = "all";
  for (const candidate of areas) candidate.setAttribute("aria-pressed", String(candidate.dataset.area === "all"));
  filter();
  search.focus();
});

function openAnchor() {
  const id = decodeURIComponent(location.hash.slice(1));
  const target = [...list.children].find(article => article.id === id);
  if (target) {
    search.value = "";
    selectedArea = "all";
    for (const candidate of areas) candidate.setAttribute("aria-pressed", String(candidate.dataset.area === "all"));
    filter();
    target.open = true;
    target.scrollIntoView({block: "start"});
  }
}
window.addEventListener("hashchange", openAnchor);

fetch("questions.json", {cache: "no-cache"}).then(response => {
  if (!response.ok) throw new Error("Question records unavailable");
  return response.json();
}).then(data => {
  if (data.schema !== "gorptastic.community-questions.v1" || !Array.isArray(data.questions)) throw new Error("Unsupported question records");
  questions = data.questions;
  list.replaceChildren(...questions.map(renderQuestion));
  filter();
  openAnchor();
}).catch(() => {
  list.replaceChildren();
  count.textContent = "Question records unavailable";
  empty.hidden = true;
  error.hidden = false;
});
