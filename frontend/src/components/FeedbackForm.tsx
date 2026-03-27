import { useState } from "react";

interface Props {
  userName: string;
  onSubmit: (isCorrect: boolean, comment: string) => void;
  submitted: boolean;
}

export default function FeedbackForm({ userName, onSubmit, submitted }: Props) {
  const [comment, setComment] = useState("");
  const [selected, setSelected] = useState<boolean | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <p className="text-green-700 font-medium">Thanks for your feedback! Check the History sidebar to see your entry.</p>
      </div>
    );
  }

  if (submitting) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center justify-center gap-3">
        <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-blue-700 font-medium">Capturing feedback...</p>
      </div>
    );
  }

  function handleSubmit() {
    if (selected === null) return;
    setSubmitting(true);
    onSubmit(selected, comment);
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">Feedback</h3>
      <div className="bg-gray-50 rounded-lg p-4 space-y-4">
        <div>
          <p className="text-sm text-gray-700 mb-3">How does this ranking look?</p>
          <div className="space-y-2">
            <label
              className={`flex items-center gap-3 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${
                selected === true
                  ? "bg-green-50 border-green-400"
                  : "bg-white border-gray-200 hover:border-green-300 hover:bg-green-50/50"
              }`}
            >
              <input
                type="radio"
                name="feedback"
                checked={selected === true}
                onChange={() => setSelected(true)}
                className="w-4 h-4 text-green-600 focus:ring-green-500"
              />
              <span className={`text-sm font-medium ${selected === true ? "text-green-700" : "text-gray-700"}`}>Looks Good</span>
            </label>
            <label
              className={`flex items-center gap-3 px-4 py-3 rounded-lg border cursor-pointer transition-colors ${
                selected === false
                  ? "bg-red-50 border-red-400"
                  : "bg-white border-gray-200 hover:border-red-300 hover:bg-red-50/50"
              }`}
            >
              <input
                type="radio"
                name="feedback"
                checked={selected === false}
                onChange={() => setSelected(false)}
                className="w-4 h-4 text-red-600 focus:ring-red-500"
              />
              <span className={`text-sm font-medium ${selected === false ? "text-red-700" : "text-gray-700"}`}>Needs Adjustment</span>
            </label>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-600 mb-1">Comment (optional)</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Share your thoughts on this ranking..."
            rows={2}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">Submitting as: <span className="font-medium">{userName}</span></span>
          <button
            onClick={handleSubmit}
            disabled={selected === null}
            className="bg-gray-900 text-white rounded-lg px-6 py-2 text-sm font-medium hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  );
}
