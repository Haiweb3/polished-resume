#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");
const { pathToFileURL } = require("url");

function findChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser"
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (candidate.includes("/")) {
      if (fs.existsSync(candidate)) {
        return candidate;
      }
      continue;
    }

    const probe = spawnSync("sh", ["-lc", `command -v ${candidate}`], {
      encoding: "utf8"
    });
    if (probe.status === 0) {
      return probe.stdout.trim();
    }
  }

  return null;
}

function main() {
  const [, , inputHtml, outputPdf] = process.argv;
  if (!inputHtml || !outputPdf) {
    console.error("Usage: export_pdf.js <input.html> <output.pdf>");
    process.exit(1);
  }

  const chrome = findChrome();
  if (!chrome) {
    console.error("Chrome or Chromium not found. Set CHROME_PATH or install Chrome.");
    process.exit(1);
  }

  const inputPath = path.resolve(inputHtml);
  const outputPath = path.resolve(outputPdf);
  if (!fs.existsSync(inputPath)) {
    console.error(`Input HTML not found: ${inputPath}`);
    process.exit(1);
  }
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), "polished-resume-chrome-"));

  const result = spawnSync(
    chrome,
    [
      "--headless=new",
      `--user-data-dir=${userDataDir}`,
      "--disable-gpu",
      "--no-first-run",
      "--no-default-browser-check",
      "--allow-file-access-from-files",
      "--no-pdf-header-footer",
      "--print-to-pdf-no-header",
      `--print-to-pdf=${outputPath}`,
      pathToFileURL(inputPath).href
    ],
    {
      encoding: "utf8"
    }
  );

  fs.rmSync(userDataDir, { recursive: true, force: true });

  if (result.error) {
    console.error(result.error.message);
    process.exit(1);
  }

  if (result.status !== 0) {
    const details = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
    if (details) {
      console.error(details);
    }
  }

  process.exit(result.status ?? 1);
}

main();
