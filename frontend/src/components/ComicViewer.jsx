// ── ComicViewer.jsx ───────────────────────────────────────────────────────────
export function ComicViewer({ comicUrl, scenes, onReset }) {
  return (
    <div>
      <div style={{ textAlign: "center", marginBottom: 20 }}>
        <h2 style={{ marginBottom: 4 }}>Your Comic is Ready!</h2>
        <p style={{ color: "#666", fontSize: 14 }}>
          {scenes.length} panels generated
        </p>
      </div>

      <img
        src={comicUrl}
        alt="Generated comic"
        style={{
          width: "100%",
          borderRadius: 10,
          boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
        }}
      />

      <div
        style={{
          display: "flex",
          gap: 12,
          marginTop: 20,
          justifyContent: "center",
        }}
      >
        <a
          href={comicUrl}
          download="comic.png"
          style={{
            padding: "10px 24px",
            background: "#22c55e",
            color: "#fff",
            borderRadius: 8,
            textDecoration: "none",
            fontWeight: 600,
          }}
        >
          ⬇ Download PNG
        </a>
        <button
          onClick={onReset}
          style={{
            padding: "10px 24px",
            background: "#f3f4f6",
            border: "1px solid #ddd",
            borderRadius: 8,
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          ← New Chapter
        </button>
      </div>

      {scenes.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <h3 style={{ marginBottom: 12 }}>Scene Breakdown</h3>
          {scenes.map((s, i) => (
            <div
              key={i}
              style={{
                padding: 14,
                marginBottom: 10,
                background: "#f9f9f9",
                borderRadius: 8,
                border: "1px solid #eee",
              }}
            >
              <strong>Scene {s.scene_number}:</strong> {s.panel_caption}
              <span
                style={{
                  marginLeft: 10,
                  fontSize: 12,
                  color: "#888",
                  background: "#eee",
                  padding: "2px 8px",
                  borderRadius: 99,
                }}
              >
                {s.mood}
              </span>
              {s.dialogue?.map((d, j) => (
                <p
                  key={j}
                  style={{ margin: "6px 0 0", fontSize: 13, color: "#555" }}
                >
                  💬 <em>{d.speaker}</em>: "{d.text}"
                </p>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
