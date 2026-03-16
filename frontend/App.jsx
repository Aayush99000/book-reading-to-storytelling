import { useState, useRef, useCallback } from "react";

const API_BASE = "http://127.0.0.1:8000";

const STYLES = [
  {
    id: "western_comic",
    label: "Western Comic",
    desc: "Bold colors, DC/Marvel ink style",
    emoji: "🦸",
  },
  {
    id: "manga",
    label: "Manga",
    desc: "Black & white, screen tones",
    emoji: "⛩️",
  },
  {
    id: "noir",
    label: "Noir",
    desc: "High contrast, deep shadows",
    emoji: "🕵️",
  },
];

function UploadZone({ onTextReady }) {
  const [dragging, setDragging] = useState(false);
  const [text, setText] = useState("");
  const [fileName, setFileName] = useState("");
  const [tab, setTab] = useState("paste"); // paste | upload
  const fileRef = useRef();

  function handleFile(file) {
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => setText(e.target.result);
    reader.readAsText(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
    setTab("upload");
  }

  function handleSubmit() {
    if (text.trim().length < 50) {
      alert("Please add at least a paragraph of text.");
      return;
    }
    onTextReady(text.trim());
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <div style={{ display: "flex", gap: 8 }}>
        {["paste", "upload"].map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              padding: "8px 20px",
              borderRadius: 8,
              border: "0.5px solid",
              borderColor:
                tab === t ? "#6c47ff" : "var(--color-border-secondary)",
              background: tab === t ? "#6c47ff" : "transparent",
              color: tab === t ? "#fff" : "var(--color-text-primary)",
              cursor: "pointer",
              fontWeight: tab === t ? 500 : 400,
              fontSize: 14,
            }}
          >
            {t === "paste" ? "✏️ Paste Text" : "📁 Upload File"}
          </button>
        ))}
      </div>

      {tab === "paste" ? (
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={`Paste your book chapter(s) here...\n\nYou can paste:\n• A single chapter\n• Multiple chapters\n• Any story text`}
          rows={12}
          style={{
            width: "100%",
            padding: 14,
            fontSize: 15,
            borderRadius: 10,
            border: "0.5px solid var(--color-border-secondary)",
            background: "var(--color-background-secondary)",
            color: "var(--color-text-primary)",
            resize: "vertical",
            lineHeight: 1.7,
            boxSizing: "border-box",
            outline: "none",
            fontFamily: "var(--font-sans)",
          }}
        />
      ) : (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileRef.current.click()}
          style={{
            border: `2px dashed ${dragging ? "#6c47ff" : "var(--color-border-secondary)"}`,
            borderRadius: 12,
            padding: "48px 24px",
            textAlign: "center",
            cursor: "pointer",
            background: dragging
              ? "#f0ecff"
              : "var(--color-background-secondary)",
            transition: "all 0.2s",
          }}
        >
          <div style={{ fontSize: 40, marginBottom: 12 }}>📄</div>
          {fileName ? (
            <>
              <p
                style={{ fontWeight: 500, margin: "0 0 4px", color: "#6c47ff" }}
              >
                {fileName}
              </p>
              <p
                style={{
                  fontSize: 13,
                  color: "var(--color-text-secondary)",
                  margin: 0,
                }}
              >
                {text.length.toLocaleString()} characters loaded ✅
              </p>
            </>
          ) : (
            <>
              <p
                style={{
                  fontWeight: 500,
                  margin: "0 0 4px",
                  color: "var(--color-text-primary)",
                }}
              >
                Drop your .txt or .md file here
              </p>
              <p
                style={{
                  fontSize: 13,
                  color: "var(--color-text-secondary)",
                  margin: 0,
                }}
              >
                or click to browse — supports .txt, .md files
              </p>
            </>
          )}
          <input
            ref={fileRef}
            type="file"
            accept=".txt,.md"
            style={{ display: "none" }}
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>
      )}

      {text.length > 0 && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            padding: "8px 14px",
            background: "var(--color-background-secondary)",
            borderRadius: 8,
            border: "0.5px solid var(--color-border-tertiary)",
            fontSize: 13,
            color: "var(--color-text-secondary)",
          }}
        >
          <span>📊</span>
          <span>{text.length.toLocaleString()} characters</span>
          <span>·</span>
          <span>~{Math.round(text.split(/\s+/).length / 200)} min read</span>
          <span>·</span>
          <span
            style={{
              color: text.length > 500 ? "#22c55e" : "#f59e0b",
              fontWeight: 500,
            }}
          >
            {text.length > 500 ? "✅ Good length" : "⚠️ Add more text"}
          </span>
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={text.length < 50}
        style={{
          padding: "13px 0",
          background:
            text.length >= 50 ? "#6c47ff" : "var(--color-border-secondary)",
          color: "#fff",
          border: "none",
          borderRadius: 10,
          fontSize: 16,
          fontWeight: 600,
          cursor: text.length >= 50 ? "pointer" : "not-allowed",
          transition: "all 0.2s",
          letterSpacing: 0.3,
        }}
      >
        Continue →
      </button>
    </div>
  );
}

function StylePicker({ selected, onSelect }) {
  return (
    <div
      style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}
    >
      {STYLES.map((s) => (
        <div
          key={s.id}
          onClick={() => onSelect(s.id)}
          style={{
            padding: "16px 12px",
            borderRadius: 10,
            textAlign: "center",
            cursor: "pointer",
            border: `${selected === s.id ? "2px" : "0.5px"} solid ${selected === s.id ? "#6c47ff" : "var(--color-border-secondary)"}`,
            background:
              selected === s.id
                ? "#f0ecff"
                : "var(--color-background-secondary)",
            transition: "all 0.15s",
          }}
        >
          <div style={{ fontSize: 28, marginBottom: 8 }}>{s.emoji}</div>
          <div
            style={{
              fontWeight: 500,
              fontSize: 14,
              marginBottom: 4,
              color: "var(--color-text-primary)",
            }}
          >
            {s.label}
          </div>
          <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>
            {s.desc}
          </div>
        </div>
      ))}
    </div>
  );
}

function ProgressBar({ progress, status }) {
  const colors = {
    pending: "#f59e0b",
    processing: "#6c47ff",
    done: "#22c55e",
    failed: "#ef4444",
  };
  const messages = {
    pending: "Queuing your request...",
    processing:
      progress < 30
        ? "🧠 Extracting scenes with Groq AI..."
        : progress < 80
          ? "🎨 Generating comic panel images..."
          : "🖼️ Assembling your comic...",
    done: "✅ Your comic is ready!",
    failed: "❌ Something went wrong",
  };
  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          marginBottom: 16,
          fontSize: 15,
          color: "var(--color-text-secondary)",
        }}
      >
        {messages[status] || "Processing..."}
      </div>
      <div
        style={{
          background: "var(--color-border-tertiary)",
          borderRadius: 99,
          height: 10,
          overflow: "hidden",
          marginBottom: 8,
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            height: "100%",
            borderRadius: 99,
            background: colors[status] || "#6c47ff",
            transition: "width 0.8s ease",
          }}
        />
      </div>
      <div style={{ fontSize: 13, color: "var(--color-text-secondary)" }}>
        {progress}% complete
      </div>
    </div>
  );
}

function SceneCard({ scene, index }) {
  return (
    <div
      style={{
        padding: 14,
        borderRadius: 10,
        border: "0.5px solid var(--color-border-tertiary)",
        background: "var(--color-background-secondary)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginBottom: 8,
        }}
      >
        <span
          style={{
            background: "#6c47ff",
            color: "#fff",
            borderRadius: 99,
            fontSize: 11,
            fontWeight: 600,
            padding: "2px 10px",
          }}
        >
          Scene {scene.scene_number}
        </span>
        <span
          style={{
            background: "var(--color-background-primary)",
            border: "0.5px solid var(--color-border-secondary)",
            borderRadius: 99,
            fontSize: 11,
            padding: "2px 10px",
            color: "var(--color-text-secondary)",
          }}
        >
          {scene.mood}
        </span>
      </div>
      <p
        style={{
          margin: "0 0 6px",
          fontWeight: 500,
          fontSize: 14,
          color: "var(--color-text-primary)",
        }}
      >
        {scene.panel_caption}
      </p>
      {scene.dialogue?.map((d, i) => (
        <p
          key={i}
          style={{
            margin: "4px 0 0",
            fontSize: 13,
            color: "var(--color-text-secondary)",
          }}
        >
          💬 <em>{d.speaker}</em>: "{d.text}"
        </p>
      ))}
    </div>
  );
}

export default function App() {
  const [step, setStep] = useState("upload"); // upload | style | generating | done | error
  const [text, setText] = useState("");
  const [style, setStyle] = useState("western_comic");
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("pending");
  const [comicUrl, setComicUrl] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");
  const pollRef = useRef(null);

  function handleTextReady(t) {
    setText(t);
    setStep("style");
  }

  async function handleGenerate() {
    try {
      setStep("generating");
      setProgress(5);
      const res = await fetch(`${API_BASE}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chapter_text: text, style }),
      });
      if (!res.ok) throw new Error("Failed to start generation");
      const data = await res.json();
      setJobId(data.job_id);

      pollRef.current = setInterval(async () => {
        try {
          const r = await fetch(`${API_BASE}/status/${data.job_id}`);
          const job = await r.json();
          setProgress(job.progress || 0);
          setStatus(job.status);
          if (job.status === "done") {
            clearInterval(pollRef.current);
            setComicUrl(`${API_BASE}${job.result_url}`);
            setScenes(job.scenes || []);
            setStep("done");
          } else if (job.status === "failed") {
            clearInterval(pollRef.current);
            setErrorMsg(job.error || "Pipeline failed.");
            setStep("error");
          }
        } catch (e) {
          clearInterval(pollRef.current);
          setErrorMsg(e.message);
          setStep("error");
        }
      }, 3000);
    } catch (e) {
      setErrorMsg(e.message);
      setStep("error");
    }
  }

  function handleReset() {
    clearInterval(pollRef.current);
    setStep("upload");
    setText("");
    setStyle("western_comic");
    setJobId(null);
    setProgress(0);
    setStatus("pending");
    setComicUrl(null);
    setScenes([]);
    setErrorMsg("");
  }

  const stepLabels = ["Upload", "Style", "Generate", "Result"];
  const stepIndex = { upload: 0, style: 1, generating: 2, done: 3, error: 2 }[
    step
  ];

  return (
    <div
      style={{
        maxWidth: 720,
        margin: "0 auto",
        padding: "2rem 1rem",
        fontFamily: "var(--font-sans)",
      }}
    >
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <h1
          style={{
            fontSize: 32,
            fontWeight: 600,
            margin: "0 0 6px",
            color: "var(--color-text-primary)",
          }}
        >
          📖 Book2Comic
        </h1>
        <p
          style={{
            color: "var(--color-text-secondary)",
            margin: 0,
            fontSize: 15,
          }}
        >
          Turn any book chapter into a comic strip using AI
        </p>
      </div>

      {/* Step indicator */}
      <div style={{ display: "flex", alignItems: "center", marginBottom: 32 }}>
        {stepLabels.map((label, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              flex: i < stepLabels.length - 1 ? 1 : "none",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 4,
              }}
            >
              <div
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 99,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 13,
                  fontWeight: 600,
                  background:
                    i < stepIndex
                      ? "#22c55e"
                      : i === stepIndex
                        ? "#6c47ff"
                        : "var(--color-border-secondary)",
                  color:
                    i <= stepIndex ? "#fff" : "var(--color-text-secondary)",
                  transition: "all 0.3s",
                }}
              >
                {i < stepIndex ? "✓" : i + 1}
              </div>
              <span
                style={{
                  fontSize: 11,
                  color:
                    i === stepIndex ? "#6c47ff" : "var(--color-text-secondary)",
                  fontWeight: i === stepIndex ? 500 : 400,
                }}
              >
                {label}
              </span>
            </div>
            {i < stepLabels.length - 1 && (
              <div
                style={{
                  flex: 1,
                  height: 2,
                  margin: "0 8px",
                  marginBottom: 18,
                  background:
                    i < stepIndex ? "#22c55e" : "var(--color-border-tertiary)",
                  transition: "background 0.3s",
                }}
              />
            )}
          </div>
        ))}
      </div>

      {/* Main card */}
      <div
        style={{
          background: "var(--color-background-primary)",
          borderRadius: 16,
          border: "0.5px solid var(--color-border-tertiary)",
          padding: "28px 28px",
        }}
      >
        {/* Step 1: Upload */}
        {step === "upload" && (
          <>
            <h2
              style={{
                margin: "0 0 20px",
                fontSize: 18,
                fontWeight: 500,
                color: "var(--color-text-primary)",
              }}
            >
              Upload your book text
            </h2>
            <UploadZone onTextReady={handleTextReady} />
          </>
        )}

        {/* Step 2: Style */}
        {step === "style" && (
          <>
            <h2
              style={{
                margin: "0 0 6px",
                fontSize: 18,
                fontWeight: 500,
                color: "var(--color-text-primary)",
              }}
            >
              Choose your comic style
            </h2>
            <p
              style={{
                margin: "0 0 20px",
                fontSize: 14,
                color: "var(--color-text-secondary)",
              }}
            >
              {text.length.toLocaleString()} characters loaded · ~
              {Math.round(text.split(/\s+/).length / 200)} min read
            </p>
            <StylePicker selected={style} onSelect={setStyle} />
            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button
                onClick={() => setStep("upload")}
                style={{
                  flex: 1,
                  padding: "12px 0",
                  borderRadius: 10,
                  border: "0.5px solid var(--color-border-secondary)",
                  background: "transparent",
                  cursor: "pointer",
                  fontSize: 14,
                  color: "var(--color-text-primary)",
                }}
              >
                ← Back
              </button>
              <button
                onClick={handleGenerate}
                style={{
                  flex: 3,
                  padding: "12px 0",
                  borderRadius: 10,
                  border: "none",
                  background: "#6c47ff",
                  color: "#fff",
                  cursor: "pointer",
                  fontSize: 15,
                  fontWeight: 600,
                  letterSpacing: 0.3,
                }}
              >
                Generate Comic ✦
              </button>
            </div>
          </>
        )}

        {/* Step 3: Generating */}
        {step === "generating" && (
          <div style={{ padding: "24px 0" }}>
            <h2
              style={{
                margin: "0 0 28px",
                fontSize: 18,
                fontWeight: 500,
                textAlign: "center",
                color: "var(--color-text-primary)",
              }}
            >
              Creating your comic...
            </h2>
            <ProgressBar progress={progress} status={status} />
            <div
              style={{
                marginTop: 28,
                display: "grid",
                gridTemplateColumns: "1fr 1fr 1fr",
                gap: 10,
              }}
            >
              {[
                "🧠 Groq AI extracts scenes",
                "🎨 Replicate draws panels",
                "🖼️ Pillow assembles comic",
              ].map((s, i) => (
                <div
                  key={i}
                  style={{
                    padding: "10px 12px",
                    borderRadius: 8,
                    textAlign: "center",
                    fontSize: 12,
                    background: "var(--color-background-secondary)",
                    color: "var(--color-text-secondary)",
                    border: "0.5px solid var(--color-border-tertiary)",
                  }}
                >
                  {s}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Done */}
        {step === "done" && (
          <div>
            <div style={{ textAlign: "center", marginBottom: 20 }}>
              <h2
                style={{
                  margin: "0 0 4px",
                  fontSize: 20,
                  fontWeight: 500,
                  color: "var(--color-text-primary)",
                }}
              >
                Your comic is ready! 🎉
              </h2>
              <p
                style={{
                  margin: 0,
                  fontSize: 14,
                  color: "var(--color-text-secondary)",
                }}
              >
                {scenes.length} panels generated
              </p>
            </div>
            <img
              src={comicUrl}
              alt="Generated comic"
              style={{
                width: "100%",
                borderRadius: 12,
                border: "0.5px solid var(--color-border-tertiary)",
              }}
            />
            <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
              <a
                href={comicUrl}
                download="comic.png"
                style={{
                  flex: 1,
                  padding: "11px 0",
                  background: "#22c55e",
                  color: "#fff",
                  borderRadius: 10,
                  textDecoration: "none",
                  textAlign: "center",
                  fontWeight: 600,
                  fontSize: 14,
                }}
              >
                ⬇ Download PNG
              </a>
              <button
                onClick={handleReset}
                style={{
                  flex: 1,
                  padding: "11px 0",
                  background: "transparent",
                  border: "0.5px solid var(--color-border-secondary)",
                  borderRadius: 10,
                  cursor: "pointer",
                  fontSize: 14,
                  color: "var(--color-text-primary)",
                }}
              >
                ← New Chapter
              </button>
            </div>
            {scenes.length > 0 && (
              <div style={{ marginTop: 24 }}>
                <h3
                  style={{
                    fontSize: 15,
                    fontWeight: 500,
                    marginBottom: 12,
                    color: "var(--color-text-primary)",
                  }}
                >
                  Scene breakdown
                </h3>
                <div
                  style={{ display: "flex", flexDirection: "column", gap: 10 }}
                >
                  {scenes.map((s, i) => (
                    <SceneCard key={i} scene={s} index={i} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error */}
        {step === "error" && (
          <div style={{ textAlign: "center", padding: "24px 0" }}>
            <div style={{ fontSize: 40, marginBottom: 12 }}>❌</div>
            <h2
              style={{
                margin: "0 0 8px",
                fontSize: 18,
                fontWeight: 500,
                color: "var(--color-text-primary)",
              }}
            >
              Something went wrong
            </h2>
            <p
              style={{
                color: "var(--color-text-secondary)",
                fontSize: 13,
                marginBottom: 20,
                wordBreak: "break-word",
              }}
            >
              {errorMsg}
            </p>
            <button
              onClick={handleReset}
              style={{
                padding: "11px 32px",
                background: "#6c47ff",
                color: "#fff",
                border: "none",
                borderRadius: 10,
                cursor: "pointer",
                fontSize: 14,
                fontWeight: 600,
              }}
            >
              Try Again
            </button>
          </div>
        )}
      </div>

      <p
        style={{
          textAlign: "center",
          fontSize: 12,
          color: "var(--color-text-secondary)",
          marginTop: 20,
        }}
      >
        Powered by Groq · Replicate · FastAPI
      </p>
    </div>
  );
}
