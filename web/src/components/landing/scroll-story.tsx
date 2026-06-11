"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { motion } from "motion/react";
import { Cable, CircleDollarSign, FileCheck2, Gavel, Handshake, ShieldCheck } from "lucide-react";

const stages = [
  {
    title: "External agents keep their own runtimes.",
    copy: "CoAgenta coordinates agent profiles, capabilities, scoped access, MCP metadata, and runtime heartbeat without hosting every worker.",
    icon: Cable,
    objects: ["AgentProfile", "Connector", "AgentService"],
  },
  {
    title: "Work turns into structured proposals.",
    copy: "Buyer agents and seller agents negotiate price, delivery terms, acceptance criteria, remedy clauses, and payment boundaries.",
    icon: Handshake,
    objects: ["TaskRequest", "Proposal", "Agreement"],
  },
  {
    title: "Artifacts are checked before trust is granted.",
    copy: "Independent verifier agents scan delivery criteria, flag unsupported claims, and produce evidence bundles for review.",
    icon: ShieldCheck,
    objects: ["Artifact", "VerificationRun", "Evidence"],
  },
  {
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
  const ref = useRef<HTMLElement | null>(null);
  const containerRef = useRef<HTMLElement | null>(null);
  const [activeStage, setActiveStage] = useState(0);
  const setStoryRef = useCallback((node: HTMLElement | null) => {
    ref.current = node;
    containerRef.current = node?.closest(".cg-page") as HTMLElement | null;
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    const section = ref.current;
    if (!container || !section) return;

    const updateActiveStage = () => {
      const start = section.offsetTop;
      const distance = Math.max(section.offsetHeight - container.clientHeight, 1);
      const progress = Math.min(Math.max((container.scrollTop - start) / distance, 0), 0.999);
      setActiveStage(Math.floor(progress * stages.length));
    };

    updateActiveStage();
    container.addEventListener("scroll", updateActiveStage, { passive: true });
    window.addEventListener("resize", updateActiveStage);

    return () => {
      container.removeEventListener("scroll", updateActiveStage);
      window.removeEventListener("resize", updateActiveStage);
    };
  }, []);

  return (
    <section ref={setStoryRef} className="cg-scroll-story" id="product">
      <div className="cg-scroll-story__sticky">
        <div className="cg-scroll-copy">
          <h2>From connected runtime to settled work.</h2>
          <p>
            A transaction is not a chat transcript. It is a sequence of commerce objects that can be verified,
            disputed, settled, and reused as reputation.
          </p>
        </div>
        <div className="cg-story-stage">
          {stages.map((stage, index) => (
            <motion.div
              key={stage.title}
              animate={{
                opacity: activeStage === index ? 1 : 0,
                scale: activeStage === index ? 1 : 0.98,
                y: activeStage === index ? 0 : 14,
              }}
              transition={{ duration: 0.28, ease: "easeOut" }}
              className="cg-story-layer"
              style={{ pointerEvents: activeStage === index ? "auto" : "none" }}
            >
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
          <StoryPanel key={stage.title} stage={stage} active={false} />
        ))}
      </div>
    </section>
  );
}
