import { spawn } from "node:child_process";

import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function runPythonDemo() {
  return new Promise<unknown>((resolve, reject) => {
    const repoRoot = process.env.ACN_DEMO_REPO_ROOT ?? "..";
    const pathSeparator = process.platform === "win32" ? ";" : ":";
    const pythonPath = [repoRoot, process.env.PYTHONPATH].filter(Boolean).join(pathSeparator);
    const pythonCommand = process.env.PYTHON_BIN || process.env.PYTHON || "python";
    const child = spawn(pythonCommand, ["-m", "demo.web_api"], {
      env: { ...process.env, PYTHONPATH: pythonPath },
      shell: process.platform === "win32",
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk: Buffer) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `Python demo exited with code ${code}`));
        return;
      }

      try {
        resolve(JSON.parse(stdout));
      } catch (error) {
        reject(new Error(`Failed to parse Python demo JSON: ${error instanceof Error ? error.message : String(error)}`));
      }
    });
  });
}

export async function POST() {
  try {
    const result = await runPythonDemo();
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        error: "demo_run_failed",
        message: error instanceof Error ? error.message : "Unknown demo failure",
      },
      { status: 500 },
    );
  }
}
