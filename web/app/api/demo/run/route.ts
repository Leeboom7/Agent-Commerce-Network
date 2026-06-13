import { NextResponse } from "next/server"
import { spawn } from "node:child_process"
import path from "node:path"
import { DEMO_SNAPSHOT } from "@/lib/mock/demo-snapshot"
import type { DemoResult } from "@/lib/types"

export const dynamic = "force-dynamic"
export const maxDuration = 60

// Resolve the repo root that contains the `demo` python package.
// In this monorepo the web app lives at <root>/web, so default one level up.
function repoRoot(): string {
  return process.env.ACN_DEMO_REPO_ROOT || path.resolve(process.cwd(), "..")
}

function pythonBin(): string {
  return process.env.PYTHON_BIN || "python3"
}

function runPythonBridge(timeoutMs = 45_000): Promise<DemoResult> {
  return new Promise((resolve, reject) => {
    const root = repoRoot()
    const proc = spawn(pythonBin(), ["-m", "demo.web_api"], {
      cwd: root,
      env: { ...process.env, PYTHONPATH: root, PYTHONUNBUFFERED: "1" },
    })

    let stdout = ""
    let stderr = ""
    const timer = setTimeout(() => {
      proc.kill("SIGKILL")
      reject(new Error("python bridge timed out"))
    }, timeoutMs)

    proc.stdout.on("data", (d) => (stdout += d.toString()))
    proc.stderr.on("data", (d) => (stderr += d.toString()))
    proc.on("error", (err) => {
      clearTimeout(timer)
      reject(err)
    })
    proc.on("close", (code) => {
      clearTimeout(timer)
      if (code !== 0) {
        reject(new Error(stderr.slice(-500) || `python exited with code ${code}`))
        return
      }
      // The bridge prints the JSON payload on the last non-empty line.
      const line = stdout
        .trim()
        .split("\n")
        .filter(Boolean)
        .pop()
      if (!line) {
        reject(new Error("python bridge produced no output"))
        return
      }
      try {
        resolve(JSON.parse(line) as DemoResult)
      } catch {
        reject(new Error("failed to parse python bridge output"))
      }
    })
  })
}

export async function POST() {
  try {
    const result = await runPythonBridge()
    return NextResponse.json({ ...result, source: "live" })
  } catch (err) {
    // Never break the demo on stage: fall back to the packaged snapshot.
    const reason = err instanceof Error ? err.message : "unknown error"
    return NextResponse.json({
      ...DEMO_SNAPSHOT,
      source: "snapshot",
      fallbackReason: reason,
    })
  }
}
