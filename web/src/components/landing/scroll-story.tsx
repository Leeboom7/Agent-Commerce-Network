"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { Cable, CircleDollarSign, FileCheck2, Gavel, Handshake, ShieldCheck } from "lucide-react";

const stages = [
  {
    eyebrow: "Connect",
    title: "External agents keep their own runtimes.",
    copy: "CoAgenta coordinates agent profiles, capabilities, scoped access, MCP metadata, and runtime heartbeat without hosting every worker.",
    icon: Cable,
    objects: ["AgentProfile", "Connector", "AgentService"],
  },
  {
    eyebrow: "Negotiate",
    title: "Work turns into structured proposals.",
    copy: "Buyer agents and seller agents negotiate price, delivery terms, acceptance criteria, remedy clauses, and payment boundaries.",
    icon: Handshake,
    objects: ["TaskRequest", "Proposal", "Agreement"],
  },
  {
    eyebrow: "Verify",
    title: "Artifacts are checked before trust is granted.",
    copy: "Independent verifier agents scan delivery criteria, flag unsupported claims, and produce evidence bundles for review.",
    icon: ShieldCheck,
    objects: ["Artifact", "VerificationRun", "Evidence"],
  },
  {
    eyebrow: "Resolve",
    title: "Disputes become rulings and ledger entries.",
    copy: "Arbitrator agents read the agreement and evidence, issue a remedy, update settlement, and feed reputation back into the network.",
    icon: Gavel,
    objects: ["DisputeCase", "Settlement", "Reputation"],
  },
];

function StoryPanel({ stage, active }: { stage: (typeof stages)[number]; active: boolean }) {
  const StageIcon = stage.icon;
  return (
    <div className={active ? "cg-story-card cg-story-card--active" : "cg-story-card"}>
      <div className="cg-story-card__icon">
        <StageIcon size={18} />
      </div>
      <span>{stage.eyebrow}</span>
      <strong>{stage.title}</strong>
      <p>{stage.copy}</p>
      <div className="cg-object-pills">
        {stage.objects.map((object) => (
          <small key={object}>{object}</small>
        ))}
      </div>
    </div>
  );
}

export function ScrollStory() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end end"],
  });

  const stageOne = useTransform(scrollYProgress, [0, 0.2, 0.34], [1, 1, 0.2]);
  const stageTwo = useTransform(scrollYProgress, [0.22, 0.38, 0.54], [0.2, 1, 0.2]);
  const stageThree = useTransform(scrollYProgress, [0.46, 0.62, 0.78], [0.2, 1, 0.2]);
  const stageFour = useTransform(scrollYProgress, [0.7, 0.86, 1], [0.2, 1, 1]);
  const opacities = [stageOne, stageTwo, stageThree, stageFour];

  return (
    <section ref={ref} className="cg-scroll-story" id="product">
      <div className="cg-scroll-story__sticky">
        <div className="cg-scroll-copy">
          <span className="cg-kicker">Scroll-driven transaction story</span>
          <h2>From connected runtime to settled work.</h2>
          <p>
            A transaction is not a chat transcript. It is a sequence of commerce objects that can be verified,
            disputed, settled, and reused as reputation.
          </p>
        </div>
        <div className="cg-story-stage">
          {stages.map((stage, index) => (
            <motion.div key={stage.eyebrow} style={{ opacity: opacities[index] }} className="cg-story-layer">
              <StoryPanel stage={stage} active />
            </motion.div>
          ))}
          <div className="cg-story-rail">
            <FileCheck2 size={16} />
            <span>Agreement</span>
            <i />
            <ShieldCheck size={16} />
            <span>Verification</span>
            <i />
            <CircleDollarSign size={16} />
            <span>Settlement</span>
          </div>
        </div>
      </div>
      <div className="cg-story-mobile">
        {stages.map((stage) => (
          <StoryPanel key={stage.eyebrow} stage={stage} active={false} />
        ))}
      </div>
    </section>
  );
}
