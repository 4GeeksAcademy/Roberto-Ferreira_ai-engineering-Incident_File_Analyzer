"use client";

import { useRef, useState } from "react";
import { analyzeIncidentFile } from "../lib/api-client";
import type { AnalysisSummary } from "../types";

type Props = {
  onComplete: (summary: AnalysisSummary) => void;
  onError: (message: string | null) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
};

export function AnalysisUpload({ onComplete, onError, loading, setLoading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  async function submit(file: File) {
    if (!file.name.toLowerCase().endsWith(".csv")) {
      onError("Please choose a CSV file.");
      return;
    }
    setLoading(true);
    onError(null);
    try {
      onComplete(await analyzeIncidentFile(file));
    } catch (cause) {
      onError(cause instanceof Error ? cause.message : "The incident file could not be analyzed.");
    } finally {
      setLoading(false);
    }
  }

  function handleDrop(event: React.DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files[0];
    if (file) void submit(file);
  }

  return (
    <section className="upload-card" aria-labelledby="upload-title">
      <div>
        <p className="eyebrow">Daily operations input</p>
        <h2 id="upload-title">Upload incident records</h2>
        <p className="muted">Use the official UTF-8 CSV export to generate a fresh analysis.</p>
      </div>
      <div
        className={`drop-zone${dragging ? " drop-zone-active" : ""}`}
        onDragEnter={(event) => { event.preventDefault(); setDragging(true); }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <span className="upload-icon" aria-hidden="true">↥</span>
        <strong>{loading ? "Analyzing file…" : "Drop your CSV here"}</strong>
        <span className="muted">or select a file from your computer</span>
        <button type="button" className="button button-secondary" onClick={() => inputRef.current?.click()} disabled={loading}>
          {loading ? "Please wait" : "Choose CSV file"}
        </button>
        <input
          ref={inputRef}
          className="visually-hidden"
          id="incident-file"
          type="file"
          accept=".csv,text/csv"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) void submit(file);
            event.currentTarget.value = "";
          }}
        />
      </div>
      <p className="file-hint">Accepted format: CSV · Maximum size is determined by the API.</p>
    </section>
  );
}
