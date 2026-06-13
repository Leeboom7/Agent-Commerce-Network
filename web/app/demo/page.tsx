import type { Metadata } from "next"
import { DemoStage } from "@/components/demo/demo-stage"

export const metadata: Metadata = {
  title: "Live commerce demo",
  description:
    "Run the full agent commerce loop end to end: discovery, negotiation, delivery, a real verification failure, arbitration, settlement, and reputation — powered by the Python ACP runtime.",
}

export default function DemoPage() {
  return <DemoStage />
}
