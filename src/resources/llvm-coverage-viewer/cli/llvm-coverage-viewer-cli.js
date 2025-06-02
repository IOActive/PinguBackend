#!/usr/bin/env node
"use strict";
const commander = require("commander");
const fs = require("fs");
const path = require("path");
const fsPromises = require("node:fs/promises");
const btoa = require("btoa");
function _interopNamespaceDefault(e) {
  const n = Object.create(null, { [Symbol.toStringTag]: { value: "Module" } });
  if (e) {
    for (const k in e) {
      if (k !== "default") {
        const d = Object.getOwnPropertyDescriptor(e, k);
        Object.defineProperty(n, k, d.get ? d : {
          enumerable: true,
          get: () => e[k]
        });
      }
    }
  }
  n.default = e;
  return Object.freeze(n);
}
const fsPromises__namespace = /* @__PURE__ */ _interopNamespaceDefault(fsPromises);
const name = "@zeromake/llvm-coverage-viewer";
const version = "1.0.10";
const description = "Convert llvm coverage report json to single html file";
const bin = {
  "llvm-coverage-viewer": "./dist/cli/llvm-coverage-viewer-cli.js"
};
const pkg = {
  scripts: "dist/cli/llvm-coverage-viewer-cli.js",
  targets: [
    "node18-linux-x64",
    "node18-win-x64",
    "node18-macos-x64"
  ],
  assets: [
    "dist/worker/llvm-coverage-viewer-highlight-worker.js",
    "dist/app/llvm-coverage-viewer-browser.js",
    "dist/app/assets/llvm-coverage-viewer.css"
  ],
  outputPath: "dist"
};
const scripts = {
  dev: "vite",
  build: "npm run build-cli && npm run build-worker && npm run build-app",
  "build-cli": "vite build -c vite.config.cli.mjs",
  "build-worker": "vite build -c vite.config.worker.mjs",
  "build-app": "vite build -c vite.config.app.mjs",
  preview: "vite preview",
  "build-binary": "pkg dist/cli/llvm-coverage-viewer-cli.js --output dist/llvm-coverage-viewer --targets node18-linux-x64,node18-win-x64,node18-macos-x64"
};
const author = "zeromake <a390720046@gmail.com>";
const license = "MIT";
const files = [
  "dist/*",
  "README.md",
  "files"
];
const homepage = "https://github.com/zeromake/llvm-coverage-viewer";
const repository = {
  type: "git",
  url: "https://github.com/zeromake/llvm-coverage-viewer.git"
};
const devDependencies = {
  "@emotion/react": "^11.11.4",
  "@emotion/styled": "^11.11.5",
  "@mui/icons-material": "^5.15.14",
  "@mui/material": "^5.15.14",
  "@types/react": "^18.2.66",
  "@types/react-dom": "^18.2.22",
  "@vitejs/plugin-react": "^4.2.1",
  "@zeromake/html-to-vdom": "^0.9.1",
  atob: "^2.1.2",
  "browser-sync": "^3.0.2",
  classnames: "^2.5.1",
  "connect-history-api-fallback": "^1.5.0",
  "hack-font": "^3.3.0",
  "highlight.js": "^11.9.0",
  "mui-styles": "^2.0.4",
  "node-interval-tree": "^2.1.2",
  "object-hash": "^3.0.0",
  "prop-types": "^15.8.1",
  react: "^18.2.0",
  "react-dom": "^18.2.0",
  "react-redux": "^9.1.0",
  "react-router": "^6.22.3",
  "react-router-dom": "^6.22.3",
  redux: "^5.0.1",
  "redux-thunk": "^3.1.0",
  sass: "^1.72.0",
  "tiny-worker": "^2.3.0",
  "typeface-roboto": "1.1.13",
  "vdom-to-html": "^2.3.1",
  vite: "^5.2.0",
  "vite-plugin-css-injected-by-js": "^3.5.0"
};
const dependencies = {
  btoa: "^1.2.1",
  commander: "^12.0.0",
  "llvm-coverage-viewer": "^1.0.2"
};
const pkg$1 = {
  name,
  version,
  description,
  bin,
  pkg,
  scripts,
  author,
  license,
  files,
  homepage,
  repository,
  devDependencies,
  dependencies
};
const render_localfs_script_tag = (path2, content, replace = true) => `
  <script type="text/localfs" data-path="${path2}">
${replace ? btoa(content) : content}
<\/script>
`;
async function fsExist(p) {
  try {
    await fsPromises__namespace.access(p);
  } catch (e) {
    return false;
  }
}
const render_static_report = async ({ report, output, use_dist, prefix_dir: prefix_dir2, debug }) => {
  const dist = use_dist;
  const filenames = report.filenames;
  const local_fs_tags = [];
  local_fs_tags.push(render_localfs_script_tag("%%___static_report___%%.json", report.report_json, false));
  const headers = [];
  const footers = [];
  let output_html = output;
  if (debug) {
    await fsPromises__namespace.cp(
      path.join(dist, "app/assets"),
      path.join(output, "assets"),
      { recursive: true }
    );
    await fsPromises__namespace.cp(
      path.join(dist, "app/llvm-coverage-viewer-browser.js"),
      path.join(output, "llvm-coverage-viewer-browser.js")
    );
    await fsPromises__namespace.cp(
      path.join(dist, "worker/llvm-coverage-viewer-highlight-worker.js"),
      path.join(output, "llvm-coverage-viewer-highlight-worker.js")
    );
    headers.push(`<link rel="stylesheet" href="assets/llvm-coverage-viewer.css"></link>`);
    footers.push(`<script type="text/javascript" src="llvm-coverage-viewer-browser.js"><\/script>`);
    if (debug === "2") {
      for (const filename of filenames) {
        const filepath = path.isAbsolute(filename) ? filename : path.join(prefix_dir2, filename);
        const outpath = path.join(output, filename);
        const outdir = path.dirname(outpath);
        if (!await fsExist(outdir)) {
          await fsPromises__namespace.mkdir(outdir, { recursive: true });
        }
        await fsPromises__namespace.symlink(filepath, outpath);
      }
    } else {
      for (const filename of filenames) {
        const filepath = path.isAbsolute(filename) ? filename : path.join(prefix_dir2, filename);
        const content = await fsPromises__namespace.readFile(filepath, "utf8");
        local_fs_tags.push(render_localfs_script_tag(filename, content));
      }
    }
    output_html = path.join(output, "index.html");
  } else {
    const getFilePath = (relativePath) => path.join(process.pkg ? path.dirname(process.execPath) : path.join(__dirname, ".."), relativePath);
    const hl_worker_path = "%%___highlight_worker___%%.js";
    const [hl_worker_src, app_src, app_css] = await Promise.all([
      fsPromises__namespace.readFile(getFilePath("worker/llvm-coverage-viewer-highlight-worker.js"), "utf8"),
      fsPromises__namespace.readFile(getFilePath("app/llvm-coverage-viewer-browser.js"), "utf8"),
      fsPromises__namespace.readFile(getFilePath("app/assets/llvm-coverage-viewer.css"), "utf8")
    ]);
    local_fs_tags.push(render_localfs_script_tag(hl_worker_path, hl_worker_src, false));
    for (const filename of filenames) {
      const filepath = path.isAbsolute(filename) ? filename : path.join(prefix_dir2, filename);
      const content = await fsPromises__namespace.readFile(filepath, "utf8");
      local_fs_tags.push(render_localfs_script_tag(filename, content));
    }
    headers.push(`<style type="text/css">
${app_css}
</style>`);
    footers.push(`<script type="text/javascript">
${app_src}
<\/script>`);
  }
  const html = `
    <!doctype html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>LLVM Coverage Viewer</title>
        ${headers.join("\n\n")}
        ${local_fs_tags.join("\n\n")}
      </head>
      <body>
        <div id="llvm-coverage-viewer-root" class="llvm-coverage-viewer-root"></div>
        ${footers.join("\n\n")}
      </body>
    </html>
  `;
  await fsPromises__namespace.writeFile(output_html, html);
};
commander.program.version(pkg$1.version).option("-j, --json <file>", "Convert llvm code coverage json to html").option("-o, --output <file>", "Path to save html report to (debug mode is dir)").option("-d, --dir <dir>", "dir profix").option("-g, --debug <mode>", "debug mode", 0);
commander.program.parse();
const options = commander.program.opts();
if (!options.json || !options.output) {
  throw new Error("--output and --json required");
}
if (!fs.existsSync(options.json)) {
  throw new Error("report does not exist");
}
let report_json = null;
let report_origin_json = null;
const current_dir = path.resolve(".").replaceAll("\\", "/");
const prefix_dir = path.resolve(options.dir || current_dir).replaceAll("\\", "/");
try {
  report_origin_json = fs.readFileSync(options.json, "utf8");
  report_json = JSON.parse(report_origin_json);
} catch (e) {
  console.log("Error: Unable to read JSON file");
  throw e;
}
function normalize_filename(filename) {
  filename = filename.replaceAll("\\", "/");
  if (!path.isAbsolute(filename))
    filename = path.join(current_dir, filename);
  if (filename.startsWith(prefix_dir)) {
    filename = filename.substring(prefix_dir.length + 1);
  }
  return filename;
}
for (const data of report_json.data) {
  for (const file of data.files) {
    file.filename = normalize_filename(file.filename);
    for (const expansion of file.expansions) {
      expansion.filenames = expansion.filenames.map(normalize_filename);
    }
  }
  for (const fun of data.functions) {
    fun.filenames = fun.filenames.map(normalize_filename);
  }
}
render_static_report({
  use_dist: path.join(__dirname, ".."),
  report: {
    filenames: report_json.data[0].files.map(({ filename }) => filename),
    report_json: JSON.stringify(report_json)
  },
  output: options.output,
  prefix_dir,
  debug: options.debug || false
});
