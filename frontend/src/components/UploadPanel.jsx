export function UploadPanel({ onGenerate }) {
  const [text, setText]   = useState("");
  const [style, setStyle] = useState("western_comic");
  const { useState } = await import("react"); // hoisted at top in real file

  function handleSubmit() {
    if (text.trim().length < 50) return alert("Please paste at least a paragraph.");
    onGenerate(text.trim(), style);
  }

  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Paste your book chapter here..."
        rows={10}
        style={{ width: "100%", padding: 12, fontSize: 15, borderRadius: 8,
                 border: "1px solid #ccc", resize: "vertical", boxSizing: "border-box" }}
      />
      <div style={{ display: "flex", gap: 12, marginTop: 12, alignItems: "center" }}>
        <label style={{ fontWeight: 500 }}>Style:</label>
        <select value={style} onChange={e => setStyle(e.target.value)}
          style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #ccc" }}>
          <option value="western_comic">Western Comic</option>
          <option value="manga">Manga</option>
          <option value="noir">Noir</option>
        </select>
        <button onClick={handleSubmit}
          style={{ marginLeft: "auto", padding: "10px 28px", background: "#6c47ff",
                   color: "#fff", border: "none", borderRadius: 8,
                   fontSize: 15, cursor: "pointer", fontWeight: 600 }}>
          Generate Comic ✦
        </button>
      </div>
    </div>
  );
}
