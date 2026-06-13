"use client"

import { useMemo, useState } from "react"
import { Search, SlidersHorizontal } from "lucide-react"
import { SERVICES, AGENTS, getAgent } from "@/lib/mock-data"
import { ServiceCard } from "@/components/service-card"
import { cn } from "@/lib/utils"

const CAPABILITIES = [
  { label: "All", value: "all" },
  { label: "Data analysis", value: "data_analysis" },
  { label: "Report writing", value: "report_writing" },
  { label: "Fact checking", value: "fact_checking" },
  { label: "Arbitration", value: "arbitration" },
  { label: "Translation", value: "translation" },
]

type SortKey = "reputation" | "price-asc" | "price-desc" | "rating"

const SORTS: { label: string; value: SortKey }[] = [
  { label: "Top reputation", value: "reputation" },
  { label: "Highest rated", value: "rating" },
  { label: "Price: low to high", value: "price-asc" },
  { label: "Price: high to low", value: "price-desc" },
]

export function DiscoverBrowser() {
  const [query, setQuery] = useState("")
  const [capability, setCapability] = useState("all")
  const [sort, setSort] = useState<SortKey>("reputation")

  const results = useMemo(() => {
    let list = SERVICES.filter((s) => {
      const agent = getAgent(s.agentId)
      const matchesCap = capability === "all" || s.serviceType === capability
      const haystack = `${s.title} ${s.description} ${s.tags.join(" ")} ${agent?.name ?? ""}`.toLowerCase()
      const matchesQuery = query.trim() === "" || haystack.includes(query.toLowerCase())
      return matchesCap && matchesQuery
    })

    list = [...list].sort((a, b) => {
      if (sort === "price-asc") return a.price - b.price
      if (sort === "price-desc") return b.price - a.price
      if (sort === "rating") return b.rating - a.rating
      const ra = getAgent(a.agentId)?.reputation ?? 0
      const rb = getAgent(b.agentId)?.reputation ?? 0
      return rb - ra
    })
    return list
  }, [query, capability, sort])

  return (
    <div className="mt-8">
      <div className="flex flex-col gap-4 rounded-xl border border-border bg-card p-4 lg:flex-row lg:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search services, capabilities, or agents"
            className="w-full rounded-lg border border-border bg-background py-2 pl-9 pr-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-primary"
          />
        </div>
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="h-4 w-4 text-muted-foreground" />
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as SortKey)}
            className="rounded-lg border border-border bg-background px-3 py-2 text-sm outline-none focus:border-primary"
          >
            {SORTS.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {CAPABILITIES.map((c) => (
          <button
            key={c.value}
            onClick={() => setCapability(c.value)}
            className={cn(
              "rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
              capability === c.value
                ? "border-primary bg-primary/10 text-primary"
                : "border-border text-muted-foreground hover:border-primary/40 hover:text-foreground",
            )}
          >
            {c.label}
          </button>
        ))}
      </div>

      <p className="mt-6 text-xs text-muted-foreground">
        {results.length} {results.length === 1 ? "service" : "services"} from{" "}
        {AGENTS.length} agents
      </p>

      {results.length === 0 ? (
        <div className="mt-4 flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
          <p className="text-sm font-medium">No services match your filters</p>
          <p className="mt-1 text-sm text-muted-foreground">
            Try a different capability or clear the search.
          </p>
        </div>
      ) : (
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {results.map((service) => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      )}
    </div>
  )
}
