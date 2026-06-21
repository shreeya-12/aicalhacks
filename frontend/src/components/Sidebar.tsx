import { useState } from "react";
import type { AgeGroup, HistoryItem } from "../types";

const AGE_LABELS: Record<AgeGroup, string> = {
  elementary: "Elementary",
  middle_school: "Middle",
  high_school: "High School",
  college: "College",
};

interface SidebarProps {
  history: HistoryItem[];
  onSelect: (topic: string, ageGroup: AgeGroup) => void;
  isLoading: boolean;
}

export function Sidebar({ history, onSelect, isLoading }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar${collapsed ? " sidebar--collapsed" : ""}`}>
      <div className="sidebar-header">
        <button
          className="sidebar-toggle"
          onClick={() => setCollapsed((c) => !c)}
          title={collapsed ? "Expand history" : "Collapse history"}
        >
          {collapsed ? "›" : "‹"}
        </button>
        {!collapsed && <span className="sidebar-title">History</span>}
      </div>

      {!collapsed && (
        <div className="sidebar-body">
          {history.length === 0 ? (
            <p className="sidebar-empty">
              Generated lessons will appear here.
            </p>
          ) : (
            <ul className="sidebar-list">
              {history.map((item, i) => (
                <li key={`${item.topic}-${item.age_group}-${i}`}>
                  <button
                    className="sidebar-item"
                    onClick={() => onSelect(item.topic, item.age_group)}
                    disabled={isLoading}
                    title={`${item.topic} · ${AGE_LABELS[item.age_group]}`}
                  >
                    <span className="sidebar-item-topic">{item.topic}</span>
                    <span className="sidebar-item-age">
                      {AGE_LABELS[item.age_group]}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </aside>
  );
}
