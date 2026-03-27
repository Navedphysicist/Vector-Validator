import { useState, useEffect } from "react";
import { saveSettings, getSettings } from "../lib/api";
import type { SettingsStatus } from "../lib/types";

const LLM_MODELS: Record<string, string[]> = {
  openai: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
  groq: ["llama-4-scout-17b-16e-instruct", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
};

interface Props {
  userName: string;
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
}

export default function SettingsModal({ userName, open, onClose, onSaved }: Props) {
  const [provider, setProvider] = useState("openai");
  const [model, setModel] = useState("gpt-4o");
  const [llmKey, setLlmKey] = useState("");
  const [tavilyKey, setTavilyKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState<SettingsStatus | null>(null);

  useEffect(() => {
    if (open && userName) {
      // Reset key fields so "Configured" badge shows correctly
      setLlmKey("");
      setTavilyKey("");
      getSettings(userName)
        .then((s) => {
          setStatus(s);
          setProvider(s.llm_provider);
          setModel(s.llm_model);
        })
        .catch(() => setStatus(null));
    }
  }, [open, userName]);

  if (!open) return null;

  const models = LLM_MODELS[provider] || [];
  const llmConfigured = status?.has_llm_key && !llmKey;
  const tavilyConfigured = status?.has_tavily_key && !tavilyKey;

  async function handleSave() {
    setSaving(true);
    try {
      await saveSettings({
        user_name: userName,
        llm_provider: provider,
        llm_model: model,
        llm_api_key: llmKey || undefined,
        tavily_api_key: tavilyKey || undefined,
      });
      onSaved();
      onClose();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-xl font-semibold text-gray-900">Settings</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
        </div>
        <p className="text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mb-4">Both API keys are required to run the application. Configure your LLM and Tavily keys below.</p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">LLM Provider</label>
            <select
              value={provider}
              onChange={(e) => { setProvider(e.target.value); setModel(LLM_MODELS[e.target.value]?.[0] || ""); }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="openai">OpenAI</option>
              <option value="groq">Groq</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {models.map((m) => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-sm font-medium text-gray-700">LLM API Key</label>
              {llmConfigured && (
                <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-0.5 rounded">Configured</span>
              )}
            </div>
            <input
              type="password"
              value={llmKey}
              onChange={(e) => setLlmKey(e.target.value)}
              placeholder={llmConfigured ? "••••••••••••••••" : "sk-..."}
              className={`w-full rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                llmConfigured
                  ? "border-green-300 bg-green-50/50"
                  : "border-gray-300"
              }`}
            />
            {llmConfigured && (
              <p className="text-xs text-gray-500 mt-1">Key already saved. Enter a new value to update it.</p>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-sm font-medium text-gray-700">Tavily API Key</label>
              {tavilyConfigured && (
                <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-0.5 rounded">Configured</span>
              )}
            </div>
            <input
              type="password"
              value={tavilyKey}
              onChange={(e) => setTavilyKey(e.target.value)}
              placeholder={tavilyConfigured ? "••••••••••••••••" : "tvly-..."}
              className={`w-full rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                tavilyConfigured
                  ? "border-green-300 bg-green-50/50"
                  : "border-gray-300"
              }`}
            />
            {tavilyConfigured && (
              <p className="text-xs text-gray-500 mt-1">Key already saved. Enter a new value to update it.</p>
            )}
          </div>
        </div>

        <button
          onClick={handleSave}
          disabled={saving}
          className="mt-6 w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {saving ? "Saving..." : "Save Settings"}
        </button>
      </div>
    </div>
  );
}
