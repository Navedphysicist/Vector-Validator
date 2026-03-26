import { useState } from "react";

interface Props {
  vectors: { business_model: string; industry: string; transaction_platform: string };
  onVectorsChange: (vectors: { business_model: string; industry: string; transaction_platform: string }) => void;
  onRunAlgorithm: () => void;
  loading: boolean;
}

function EditableField({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  function save() {
    onChange(draft);
    setEditing(false);
  }

  if (editing) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-500 w-40">{label}:</span>
        <input
          type="text"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && save()}
          autoFocus
          className="flex-1 border border-blue-300 rounded px-2 py-1 text-sm focus:ring-2 focus:ring-blue-500"
        />
        <button onClick={save} className="text-blue-600 text-sm font-medium">Save</button>
        <button onClick={() => setEditing(false)} className="text-gray-400 text-sm">Cancel</button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium text-gray-500 w-40">{label}:</span>
      <span className="text-sm text-gray-900">{value}</span>
      <button onClick={() => { setDraft(value); setEditing(true); }} className="text-gray-400 hover:text-blue-600">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
      </button>
    </div>
  );
}

export default function VectorDisplay({ vectors, onVectorsChange, onRunAlgorithm, loading }: Props) {
  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">Vectors</h3>
      <div className="bg-gray-50 rounded-lg p-4 space-y-3">
        <EditableField
          label="Business Model"
          value={vectors.business_model}
          onChange={(v) => onVectorsChange({ ...vectors, business_model: v })}
        />
        <EditableField
          label="Industry"
          value={vectors.industry}
          onChange={(v) => onVectorsChange({ ...vectors, industry: v })}
        />
        <EditableField
          label="Transaction Platform"
          value={vectors.transaction_platform}
          onChange={(v) => onVectorsChange({ ...vectors, transaction_platform: v })}
        />
      </div>
      <button
        onClick={onRunAlgorithm}
        disabled={loading}
        className="w-full bg-emerald-600 text-white rounded-lg py-2.5 text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Running Algorithm..." : "Run Algorithm"}
      </button>
    </div>
  );
}
