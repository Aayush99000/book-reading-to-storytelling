import { useState, useRef } from "react";
import { generateComic, pollStatus, getComicUrl } from "./api";
import UploadPanel from "./components/UploadPanel";
import ProgressBar from "./components/ProgressBar";
import ComicViewer from "./components/ComicViewer";

export default function App() {
  const [stage, setStage] = useState("idle"); // idle | loading | done | error
  const [progress, setProgress] = useState(0);
  const [comicUrl, setComicUrl] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");
  const pollRef = useRef(null);

  async function handleGenerate(text, style) {
    try {
      setStage("loading");
      setProgress(5);

      const { job_id } = await generateComic(text, style);

      // poll every 3 seconds
      pollRef.current = setInterval(async () => {
        const job = await pollStatus(job_id);
        setProgress(job.progress);

        if (job.status === "done") {
          clearInterval(pollRef.current);
          setComicUrl(getComicUrl(job.result_url));
          setScenes(job.scenes || []);
          setStage("done");
        } else if (job.status === "failed") {
          clearInterval(pollRef.current);
          setErrorMsg(job.error || "Something went wrong.");
          setStage("error");
        }
      }, 3000);
    } catch (e) {
      setErrorMsg(e.message);
      setStage("error");
    }
  }

  function handleReset() {
    clearInterval(pollRef.current);
    setStage("idle");
    setProgress(0);
    setComicUrl(null);
    setScenes([]);
    setErrorMsg("");
  }

  return (
    <div
      style={{
        maxWidth: 860,
        margin: "0 auto",
        padding: "2rem 1rem",
        fontFamily: "sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", fontSize: 28, marginBottom: 4 }}>
        📖 Book2Comic
      </h1>
      <p style={{ textAlign: "center", color: "#666", marginBottom: 32 }}>
        Paste a book chapter — get a comic strip back
      </p>

      {stage === "idle" && <UploadPanel onGenerate={handleGenerate} />}

      {stage === "loading" && (
        <div style={{ textAlign: "center" }}>
          <ProgressBar progress={progress} />
          <p style={{ color: "#555", marginTop: 12 }}>
            {progress < 30
              ? "Extracting scenes with Groq..."
              : progress < 80
                ? "Generating panel images..."
                : "Assembling your comic..."}
          </p>
        </div>
      )}

      {stage === "done" && (
        <ComicViewer
          comicUrl={comicUrl}
          scenes={scenes}
          onReset={handleReset}
        />
      )}

      {stage === "error" && (
        <div style={{ textAlign: "center" }}>
          <p style={{ color: "red" }}>❌ {errorMsg}</p>
          <button
            onClick={handleReset}
            style={{ marginTop: 12, padding: "8px 20px", cursor: "pointer" }}
          >
            Try again
          </button>
        </div>
      )}
    </div>
  );
}
