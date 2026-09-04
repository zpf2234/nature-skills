import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { fetchToBuffer } from "../../scripts/lib/pdf-utils.mjs";


describe("browser fetch cleanup", () => {
  test("removes buffered response bytes after an HTTP error", async () => {
    const scripts = [];
    const evalImpl = async (_proxy, _target, script) => {
      scripts.push(script);
      if (scripts.length === 1) {
        return JSON.stringify({
          ok: false,
          status: 404,
          size: 4096,
          head: [],
          contentType: "text/html",
        });
      }
      return "";
    };

    const result = await fetchToBuffer(
      "proxy",
      "target",
      "https://example.test/missing.pdf",
      { evalImpl },
    );

    assert.equal(result.ok, false);
    assert.equal(result.status, 404);
    assert.equal(result.err, "HTTP 404");
    assert.equal(scripts.length, 2);
    assert.match(scripts[1], /delete window\['__litDlBytes_/);
  });

  test("preserves the dedicated oversized response status", async () => {
    const result = await fetchToBuffer(
      "proxy",
      "target",
      "https://example.test/large.pdf",
      {
        evalImpl: async () => JSON.stringify({
          ok: false,
          err: "pdf_too_large",
          size: 300 * 1024 * 1024,
        }),
      },
    );

    assert.equal(result.ok, false);
    assert.equal(result.err, "pdf_too_large");
    assert.equal(result.size, 300 * 1024 * 1024);
  });
});
