import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_OWNER = "nobnobz";
const REPO_NAME = "Omni-Template-Bot-Bid-Raiser";
const DEFAULT_BRANCH = "main";

const TYPE_PRIORITY = {
  omni: 0,
  aiometadata: 1,
  catalogsOnly: 2,
  aiostreams: 3
};

const TYPE_LABEL = {
  omni: "UME Omni Template",
  aiometadata: "UME AIOMetadata Template",
  catalogsOnly: "UME AIOMetadata (Catalogs Only)",
  aiostreams: "UME AIOStreams Template"
};

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = path.join(rootDir, "template-manifest.json");

async function main() {
  const templateFiles = await findTemplateFiles(rootDir);
  const templates = [];

  for (const absolutePath of templateFiles) {
    const relativePath = toPosix(path.relative(rootDir, absolutePath));
    const basename = path.basename(absolutePath);
    const type = getTemplateType(basename);

    if (!type) {
      continue;
    }

    const parsedJson = await readJsonIfNeeded(absolutePath, type);
    const version = resolveVersion({
      basename,
      parsedJson,
      type
    });

    const template = {
      id: relativePath,
      name: buildDisplayName(type, version),
      url: buildRawUrl(relativePath)
    };

    if (version) {
      template.version = version;
    }

    templates.push(template);
  }

  templates.sort(compareTemplates);

  const defaultOmniId = getDefaultOmniId(templates);
  for (const template of templates) {
    if (template.id === defaultOmniId) {
      template.isDefault = true;
    }
  }

  const manifest = {
    generatedAt: new Date().toISOString(),
    templates
  };

  await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  console.log(`Generated ${path.basename(manifestPath)} with ${templates.length} templates.`);
}

async function findTemplateFiles(directory) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (entry.name === ".git" || entry.name === ".github") {
      if (entry.name === ".github") {
        continue;
      }

      continue;
    }

    const absolutePath = path.join(directory, entry.name);

    if (entry.isDirectory()) {
      files.push(...await findTemplateFiles(absolutePath));
      continue;
    }

    if (!entry.isFile() || !entry.name.toLowerCase().endsWith(".json")) {
      continue;
    }

    if (entry.name === "template-manifest.json") {
      continue;
    }

    if (getTemplateType(entry.name)) {
      files.push(absolutePath);
    }
  }

  return files;
}

function getTemplateType(filename) {
  const normalized = filename.toLowerCase();

  if (!normalized.endsWith(".json")) {
    return null;
  }

  if (normalized.startsWith("ume-aiometadata-") && normalized.includes("catalogs-only")) {
    return "catalogsOnly";
  }

  if (normalized.startsWith("ume-aiometadata-")) {
    return "aiometadata";
  }

  if (normalized.startsWith("ume-aiostreams-")) {
    return "aiostreams";
  }

  if (normalized.startsWith("ume-omni-template-")) {
    return "omni";
  }

  return null;
}

async function readJsonIfNeeded(absolutePath, type) {
  if (type !== "aiostreams") {
    return null;
  }

  try {
    const raw = await fs.readFile(absolutePath, "utf8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function resolveVersion({ basename, parsedJson, type }) {
  const filenameVersion = normalizeVersion(extractVersionFromText(basename));

  if (type === "aiostreams") {
    const declaredVersion = normalizeVersion(extractAIOStreamsDeclaredVersion(parsedJson));
    return declaredVersion || filenameVersion || null;
  }

  return filenameVersion || null;
}

function extractVersionFromText(value) {
  if (!value) {
    return null;
  }

  const match = value.match(/v\d+(?:\.\d+)*/i);
  return match ? match[0] : null;
}

function extractAIOStreamsDeclaredVersion(parsedJson) {
  if (!parsedJson) {
    return null;
  }

  const candidates = [];

  if (Array.isArray(parsedJson)) {
    for (const item of parsedJson) {
      candidates.push(item?.metadata?.version);
      candidates.push(item?.version);
    }
  } else {
    candidates.push(parsedJson?.metadata?.version);
    candidates.push(parsedJson?.version);
  }

  for (const candidate of candidates) {
    const version = extractVersionFromText(String(candidate ?? ""));
    if (version) {
      return version;
    }

    if (typeof candidate === "string" && /^\d+(?:\.\d+)*$/.test(candidate.trim())) {
      return candidate.trim();
    }
  }

  return null;
}

function normalizeVersion(value) {
  if (!value || typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();
  if (!trimmed) {
    return null;
  }

  const clean = trimmed.startsWith("v") || trimmed.startsWith("V")
    ? trimmed.slice(1)
    : trimmed;

  if (!/^\d+(?:\.\d+)*$/.test(clean)) {
    return null;
  }

  return `v${clean}`;
}

function buildDisplayName(type, version) {
  const label = TYPE_LABEL[type] || "UME Template";
  return version ? `${label} ${version}` : label;
}

function buildRawUrl(relativePath) {
  const encodedPath = relativePath
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");

  return `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${DEFAULT_BRANCH}/${encodedPath}`;
}

function compareTemplates(left, right) {
  const versionComparison = compareVersions(left.version, right.version);
  if (versionComparison !== 0) {
    return versionComparison;
  }

  const typeComparison = (TYPE_PRIORITY[getTemplateType(path.basename(left.id))] ?? 99)
    - (TYPE_PRIORITY[getTemplateType(path.basename(right.id))] ?? 99);
  if (typeComparison !== 0) {
    return typeComparison;
  }

  return left.id.localeCompare(right.id);
}

function compareVersions(left, right) {
  if (!left && !right) {
    return 0;
  }

  if (!left) {
    return 1;
  }

  if (!right) {
    return -1;
  }

  const leftParts = versionToParts(left);
  const rightParts = versionToParts(right);
  const maxLength = Math.max(leftParts.length, rightParts.length);

  for (let index = 0; index < maxLength; index += 1) {
    const leftValue = leftParts[index] ?? 0;
    const rightValue = rightParts[index] ?? 0;

    if (leftValue !== rightValue) {
      return rightValue - leftValue;
    }
  }

  return 0;
}

function versionToParts(version) {
  return version.replace(/^v/i, "").split(".").map((part) => Number.parseInt(part, 10) || 0);
}

function getDefaultOmniId(templates) {
  for (const template of templates) {
    if (getTemplateType(path.basename(template.id)) === "omni") {
      return template.id;
    }
  }

  return null;
}

function toPosix(value) {
  return value.split(path.sep).join("/");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
