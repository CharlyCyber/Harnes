import assert from "node:assert/strict";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { freezeRecipe } from "./recipe-store.mjs";

function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), "harnes-recipe-store-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const project = join(root, "project");
  mkdirSync(project);
  writeFileSync(join(project, "frame.md"), "# Approved visual style\n");
  writeFileSync(join(project, "STORYBOARD.md"), "## Scene 1\nA safe placeholder.\n");
  writeFileSync(join(project, "BRIEF.md"), "---\nworkflow: general-video\n---\n");
  return { root, project };
}

test("does not freeze into a linked project recipe directory", (t) => {
  const { root, project } = fixture(t);
  const outside = join(root, "outside");
  mkdirSync(outside);
  writeFileSync(join(outside, "sentinel"), "untouched");
  mkdirSync(join(project, ".media"));
  symlinkSync(outside, join(project, ".media", "recipes"), "dir");

  assert.throws(
    () => freezeRecipe({ projectDir: project, name: "launch", blocks: [] }),
    /is a link/,
  );
  assert.deepEqual((awaitReadDir(outside)), ["sentinel"]);
  assert.equal(readFileSync(join(outside, "sentinel"), "utf8"), "untouched");
});

test("does not freeze content read through a linked project source", (t) => {
  const { root, project } = fixture(t);
  const outside = join(root, "outside-frame.md");
  writeFileSync(outside, "private frame data\n");
  rmSync(join(project, "frame.md"));
  symlinkSync(outside, join(project, "frame.md"));

  assert.throws(
    () => freezeRecipe({ projectDir: project, name: "launch", blocks: [] }),
    /link or not a regular file/,
  );
  assert.equal(readFileSync(outside, "utf8"), "private frame data\n");
});

function awaitReadDir(path) {
  return readdirSync(path).sort();
}

import { readdirSync } from "node:fs";
