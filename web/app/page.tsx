import { LandingHero } from "@/components/landing/hero"
import { ProblemSection } from "@/components/landing/problem-section"
import { CommerceLoop } from "@/components/landing/commerce-loop"
import { ComparisonSection } from "@/components/landing/comparison-section"
import { TwoSidedSection } from "@/components/landing/two-sided-section"
import { ConnectorSection } from "@/components/landing/connector-section"
import { BaselineSection } from "@/components/landing/baseline-section"
import { ClosingCta } from "@/components/landing/closing-cta"

export default function HomePage() {
  return (
    <>
      <LandingHero />
      <ProblemSection />
      <CommerceLoop />
      <ComparisonSection />
      <TwoSidedSection />
      <ConnectorSection />
      <BaselineSection />
      <ClosingCta />
    </>
  )
}
