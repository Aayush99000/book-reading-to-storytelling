// ── ProgressBar.jsx ───────────────────────────────────────────────────────────
export function ProgressBar({ progress }) {
  return (
    <div style={{ margin: "0 auto", maxWidth: 480 }}>
      <div
        style={{
          background: "#eee",
          borderRadius: 99,
          height: 14,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            height: "100%",
            background: "#6c47ff",
            borderRadius: 99,
            transition: "width 0.6s ease",
          }}
        />
      </div>
      <p style={{ marginTop: 6, fontSize: 13, color: "#888" }}>
        {progress}% complete
      </p>
    </div>
  );
}
