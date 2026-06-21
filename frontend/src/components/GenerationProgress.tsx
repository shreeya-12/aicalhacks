import { useEffect, useState } from "react";

// Live generation (plan -> research -> write -> images) can take a few minutes.
// We can't get real progress from the backend, so this shows a reassuring
// time-based bar that eases toward ~95% and cycles through the real stages.
const STAGES = [
  "Planning the chapters…",
  "Researching the web with Browserbase…",
  "Reading articles and sources…",
  "Writing your story with Claude…",
  "Illustrating each chapter…",
  "Putting it all together…",
];

const STAGE_INTERVAL_MS = 18000; // advance the label roughly every 18s

export function GenerationProgress() {
  const [stage, setStage] = useState(0);
  const [pct, setPct] = useState(4);

  useEffect(() => {
    const stageTimer = setInterval(() => {
      setStage((s) => Math.min(s + 1, STAGES.length - 1));
    }, STAGE_INTERVAL_MS);

    // Creep the bar forward, slowing as it approaches 95% (never hits 100%
    // until the request actually resolves and this unmounts).
    const barTimer = setInterval(() => {
      setPct((p) => (p >= 95 ? 95 : p + Math.max(0.4, (95 - p) * 0.04)));
    }, 600);

    return () => {
      clearInterval(stageTimer);
      clearInterval(barTimer);
    };
  }, []);

  return (
    <div className="gen-progress" role="status" aria-live="polite">
      <div className="gen-progress-track">
        <div className="gen-progress-fill" style={{ width: `${pct}%` }} />
      </div>
      <p className="gen-progress-label">
        <span className="gen-progress-spinner" />
        {STAGES[stage]}
      </p>
      <p className="gen-progress-hint">
        This can take a couple of minutes for a fresh topic — hang tight.
      </p>

      <style>{`
        .gen-progress {
          margin-top: 1.25rem;
          display: flex;
          flex-direction: column;
          gap: 0.6rem;
        }
        .gen-progress-track {
          width: 100%;
          height: 8px;
          background: rgba(124, 58, 237, 0.12);
          border-radius: 999px;
          overflow: hidden;
        }
        .gen-progress-fill {
          height: 100%;
          border-radius: 999px;
          background: linear-gradient(90deg, #7c3aed, #a855f7);
          transition: width 0.6s ease-out;
        }
        .gen-progress-label {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin: 0;
          font-weight: 600;
          color: #6d28d9;
          font-size: 0.95rem;
        }
        .gen-progress-hint {
          margin: 0;
          font-size: 0.82rem;
          color: #9ca3af;
        }
        .gen-progress-spinner {
          width: 14px;
          height: 14px;
          border: 2px solid rgba(124, 58, 237, 0.3);
          border-top-color: #7c3aed;
          border-radius: 50%;
          animation: gen-spin 0.7s linear infinite;
          flex-shrink: 0;
        }
        @keyframes gen-spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
