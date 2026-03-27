import { useState, useEffect } from "react";
import CompanyRoleInput from "./components/CompanyRoleInput";
import VectorDisplay from "./components/VectorDisplay";
import AlgorithmResult from "./components/AlgorithmResult";
import FeedbackForm from "./components/FeedbackForm";
import FeedbackSidebar from "./components/FeedbackSidebar";
import SettingsModal from "./components/SettingsModal";
import { getUserName, setUserName } from "./stores/settings";
import { analyze, runAlgorithm, submitFeedback, getFeedback } from "./lib/api";
import type { AnalyzeResponse, RunAlgorithmResponse, FeedbackItem } from "./lib/types";

type Step = "input" | "vectors" | "result" | "feedback";

function App() {
  const [userName, setUserNameState] = useState(getUserName() || "");
  const [showNamePrompt, setShowNamePrompt] = useState(!getUserName());
  const [showSettings, setShowSettings] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);

  const [step, setStep] = useState<Step>("input");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [vectors, setVectors] = useState<AnalyzeResponse | null>(null);
  const [result, setResult] = useState<RunAlgorithmResponse | null>(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [newFeedbackCount, setNewFeedbackCount] = useState(0);
  const [feedbackItems, setFeedbackItems] = useState<FeedbackItem[]>([]);

  useEffect(() => {
    if (!getUserName()) {
      setShowNamePrompt(true);
    } else {
      getFeedback(100).then(setFeedbackItems).catch(() => {});
    }
  }, []);

  function handleNameSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (userName.trim()) {
      setUserName(userName.trim());
      setUserNameState(userName.trim());
      setShowNamePrompt(false);
      setShowSettings(true);
      // Fetch history now that the user is logged in
      getFeedback(100).then(setFeedbackItems).catch(() => {});
    }
  }

  async function handleAnalyze(comp: string, r: string) {
    setError("");
    setCompany(comp);
    setRole(r);
    setAnalyzing(true);
    try {
      const res = await analyze({ company: comp, role: r, user_name: userName });
      setVectors(res);
      setStep("vectors");
      setResult(null);
      setFeedbackSubmitted(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleRunAlgorithm() {
    if (!vectors) return;
    setError("");
    setRunning(true);
    try {
      const res = await runAlgorithm({
        business_model: vectors.business_model,
        industry: vectors.industry,
        transaction_platform: vectors.transaction_platform,
        role,
        user_name: userName,
      });
      setResult(res);
      setStep("result");
      setFeedbackSubmitted(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Algorithm failed");
    } finally {
      setRunning(false);
    }
  }

  async function handleFeedback(isCorrect: boolean, comment: string) {
    if (!vectors || !result) return;
    try {
      await submitFeedback({
        company,
        industry: vectors.industry,
        business_model: vectors.business_model,
        transaction_platform: vectors.transaction_platform,
        role,
        role_family: result.role_family,
        p1: result.p1,
        p2: result.p2,
        p3: result.p3,
        is_correct: isCorrect,
        comment: comment || undefined,
        user_name: userName,
      });
      setFeedbackSubmitted(true);
      setNewFeedbackCount((c) => c + 1);
      setFeedbackItems((prev) => [{
        id: crypto.randomUUID(),
        company,
        industry: vectors.industry,
        business_model: vectors.business_model,
        transaction_platform: vectors.transaction_platform,
        role,
        role_family: result.role_family,
        p1: result.p1,
        p2: result.p2,
        p3: result.p3,
        is_correct: isCorrect,
        comment: comment || undefined,
        user_name: userName,
        created_at: new Date().toISOString(),
      }, ...prev]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to submit feedback");
    }
  }

  function handleReset() {
    setStep("input");
    setVectors(null);
    setResult(null);
    setFeedbackSubmitted(false);
    setError("");
  }

  // Name prompt
  if (showNamePrompt) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <form onSubmit={handleNameSubmit} className="bg-white rounded-xl shadow-lg p-10 w-full max-w-sm">
          <div className="flex items-center gap-3 mb-1">
            <img src="/logo.svg" alt="Vector Validator" className="w-9 h-9" />
            <h1 className="text-2xl font-bold text-gray-900">Vector Validator</h1>
          </div>
          <p className="text-sm text-gray-500 mb-8">Validate executive search priority vectors</p>
          <label className="block text-sm font-medium text-gray-700 mb-1">What's your name?</label>
          <input
            type="text"
            value={userName}
            onChange={(e) => setUserNameState(e.target.value)}
            placeholder="Your name"
            autoFocus
            className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm mb-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={!userName.trim()}
            className="w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            Get Started
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-30">
        <div className="max-w-2xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <img src="/logo.svg" alt="Vector Validator" className="w-8 h-8" />
            <div>
              <h1 className="text-lg font-bold text-gray-900">Vector Validator</h1>
              <p className="text-xs text-gray-500">Signed in as {userName}</p>
            </div>
          </div>
          <div className="flex gap-2 items-center">
            <button
              onClick={() => { setShowSidebar(true); setNewFeedbackCount(0); }}
              className="relative text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100 text-sm font-medium"
              title="View history"
            >
              History
              {newFeedbackCount > 0 && (
                <span className="absolute -top-1 -right-1 min-w-[20px] h-5 bg-blue-600 text-white text-xs font-bold rounded-full flex items-center justify-center px-1">
                  {newFeedbackCount}
                </span>
              )}
            </button>
            <button
              onClick={() => setShowSettings(true)}
              className="text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100"
              title="Settings"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-2xl mx-auto px-4 py-8 space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
            {error}
            <button onClick={() => setError("")} className="ml-2 text-red-500 hover:text-red-700">&times;</button>
          </div>
        )}

        {/* Step 1: Input */}
        <CompanyRoleInput onAnalyze={handleAnalyze} loading={analyzing} disabled={false} />

        {/* Analysis loading indicator */}
        {analyzing && (
          <div className="bg-white border border-gray-200 rounded-lg p-4 flex items-center gap-3">
            <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm text-gray-600">Analyzing vectors for <span className="font-medium text-gray-900">{company}</span>...</span>
          </div>
        )}

        {/* Step 2: Vectors */}
        {vectors && step !== "input" && (
          <VectorDisplay
            vectors={vectors}
            onVectorsChange={setVectors}
            onRunAlgorithm={handleRunAlgorithm}
            loading={running}
          />
        )}

        {/* Step 3: Result */}
        {result && vectors && (step === "result" || feedbackSubmitted) && (
          <AlgorithmResult
            roleFamily={result.role_family}
            p1={result.p1}
            p2={result.p2}
            p3={result.p3}
            vectors={vectors}
            tiers={result.tiers}
          />
        )}

        {/* Step 4: Feedback */}
        {result && (
          <FeedbackForm
            userName={userName}
            onSubmit={handleFeedback}
            submitted={feedbackSubmitted}
          />
        )}

        {/* Reset */}
        {feedbackSubmitted && (
          <button
            onClick={handleReset}
            className="w-full border border-gray-300 text-gray-700 rounded-lg py-2.5 text-sm font-medium hover:bg-gray-50"
          >
            Test Another Company
          </button>
        )}
      </main>

      {/* Modals */}
      <SettingsModal
        userName={userName}
        open={showSettings}
        onClose={() => setShowSettings(false)}
        onSaved={() => {}}
      />
      <FeedbackSidebar open={showSidebar} onClose={() => setShowSidebar(false)} items={feedbackItems} />
    </div>
  );
}

export default App;
