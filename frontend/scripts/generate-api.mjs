import { spawnSync } from "node:child_process";
import {
  existsSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import openapiTS, { astToString } from "openapi-typescript";
import ts from "typescript";

const frontendRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const backendRoot = resolve(frontendRoot, "../backend");
const checkedContract = join(frontendRoot, "openapi/openapi.json");
const checkedTypes = join(
  frontendRoot,
  "lib/infrastructure/api/generated/schema.ts",
);

function pythonExecutable() {
  const virtualEnvironmentPython =
    process.platform === "win32"
      ? join(backendRoot, ".venv/Scripts/python.exe")
      : join(backendRoot, ".venv/bin/python");
  return existsSync(virtualEnvironmentPython)
    ? virtualEnvironmentPython
    : process.platform === "win32"
      ? "python"
      : "python3";
}

function exportContract(output) {
  const result = spawnSync(
    pythonExecutable(),
    [join(backendRoot, "scripts/export_openapi.py"), output],
    { cwd: backendRoot, encoding: "utf8" },
  );
  if (result.status !== 0) {
    throw new Error(result.stderr || result.stdout || "OpenAPI export failed");
  }
}

async function generateTypes(contractPath) {
  const schema = JSON.parse(readFileSync(contractPath, "utf8"));
  const nodes = await openapiTS(schema, {
    transform(schemaObject) {
      if (
        schemaObject.type === "string" &&
        (schemaObject.format === "binary" ||
          schemaObject.contentMediaType === "application/octet-stream")
      ) {
        return ts.factory.createTypeReferenceNode("Blob", undefined);
      }
      return undefined;
    },
  });
  return astToString(nodes);
}

async function generate() {
  exportContract(checkedContract);
  writeFileSync(checkedTypes, await generateTypes(checkedContract), "utf8");
}

async function check() {
  const temporaryDirectory = mkdtempSync(
    join(tmpdir(), "progress-tracker-api-"),
  );
  try {
    const contractPath = join(temporaryDirectory, "openapi.json");
    exportContract(contractPath);
    const generatedContract = readFileSync(contractPath, "utf8");
    const generatedTypes = await generateTypes(contractPath);
    const failures = [];
    if (generatedContract !== readFileSync(checkedContract, "utf8")) {
      failures.push("openapi/openapi.json");
    }
    if (generatedTypes !== readFileSync(checkedTypes, "utf8")) {
      failures.push("lib/infrastructure/api/generated/schema.ts");
    }
    if (failures.length) {
      throw new Error(
        `Generated API artifacts are stale: ${failures.join(", ")}. Run npm run generate:api.`,
      );
    }
  } finally {
    rmSync(temporaryDirectory, { recursive: true, force: true });
  }
}

if (process.argv.includes("--check")) {
  await check();
} else {
  await generate();
}
