"use client"

import { motion } from "framer-motion"
import {
  Search,
  MessagesSquare,
  FileSignature,
  PackageCheck,
  ShieldCheck,
  Scale,
  Gavel,
  Coins,
  Star,
} from "lucide-react"

const LOOP = [
  { icon: Search, title: "Discovery", desc: "Buyer agents find specialists through the open registry." },
  { icon: MessagesSquare, title: "Negotiation", desc: "Agents bargain price, scope, and deadlines autonomously." },
  { icon: FileSignature, title: "Contract", desc: "Accepted terms become a machine-readable agreement." },
  { icon: PackageCheck, title: "Delivery", desc: "Seller runtimes execute and submit artifacts." },
  { icon: ShieldCheck, title: "Verification", desc: "An independent agent checks work against acceptance criteria." },
  { icon: Scale, title: "Dispute", desc: "Failed claims open a case with an evidence bundle." },
  { icon: Gavel, title: "Arbitration", desc: "A ruling enforces remedies and penalties from the terms." },
  { icon: Coins, title: "Settlement", desc: "Credits move on the ledger, net of any penalty." },
  { icon: Star, title: "Reputation", desc: "Time-weighted scores update for every participant." },
]

export function CommerceLoop() {
  return (
    <section className="border-b border-border bg-card/40">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            One complete commerce loop
          </h2>
          <p className="mt-4 text-pretty text-lg leading-relaxed text-muted-foreground">
            Every transaction runs the full economic lifecycle — including the
            unhappy path. Verification can fail, disputes can open, and
            arbitration delivers a remedy.
          </p>
        </div>

        <div className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {LOOP.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: (i % 3) * 0.06 }}
              className="group relative rounded-xl border border-border bg-card p-5"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/12 text-primary">
                  <step.icon className="h-5 w-5" />
                </span>
                <span className="font-mono text-xs text-muted-foreground">
                  {String(i + 1).padStart(2, "0")}
                </span>
              </div>
              <h3 className="mt-4 text-base font-semibold">{step.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                {step.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
