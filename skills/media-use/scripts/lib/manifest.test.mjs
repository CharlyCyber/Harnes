import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { appendRecord, ownFolder, ownMediaDir } from "./manifest.mjs";

function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), "harnes-media-manifest-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  return root;
}

test("rejects a .media directory redirected outside the project", (t) => {
  const project = fixture(t);
  const outside = join(project, "outside");
  mkdirSync(outside);
  writeFileSync(join(outside, "sentinel"), "untouched");
  symlinkSync(outside, join(project, ".media"), "dir");

  assert.throws(() => ownMediaDir(project), /leads outside the project folder/);
  assert.throws(
    () => appendRecord(project, { type: "image", id: "x", path: "x" }),
    /leads outside the project folder/,
  );
  assert.equal(readFileSync(join(outside, "sentinel"), "utf8"), "untouched");
  assert.deepEqual(readdirSync(outside).sort(), ["sentinel"]);
});

test("rejects a linked nested media directory before creating files through it", (t) => {
  const project = fixture(t);
  mkdirSync(join(project, ".media"));
  const outside = join(project, "outside");
  mkdirSync(outside);
  symlinkSync(outside, join(project, ".media", "images"), "dir");

  assert.throws(() => ownFolder(join(project, ".media"), "images/generated"), /is a link/);
  assert.deepEqual(readdirSync(outside), []);
});

test("refuses to append through a linked manifest file", (t) => {
  const project = fixture(t);
  mkdirSync(join(project, ".media"));
  const outside = join(project, "outside.jsonl");
  writeFileSync(outside, "keep this\n");
  symlinkSync(outside, join(project, ".media", "manifest.jsonl"));

  assert.throws(
    () => appendRecord(project, { type: "image", id: "x", path: "x" }),
    /is a link/,
  );
  assert.equal(readFileSync(outside, "utf8"), "keep this\n");
});

