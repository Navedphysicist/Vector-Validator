import { useState } from "react";

interface Props {
  userName: string;
  onSubmit: (isCorrect: boolean, comment: string) => void;
  submitted: boolean;
}

export default function FeedbackForm({ userName, onSubmit, submitted }: Props) {
  const [comment, setComment] = useState("");
  const [selected, setSelected] = useState<boolean | null>(null);

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <p className="text-green-700 font-medium">Thanks for your feedback! Check the History sidebar to see your entry.</p>
      </div>
    );
  }

  function handleSubmit() {
    if (selected === null) return;
    onSubmit(selected, comment);
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">Feedback</h3>
      <div className="bg-gray-50 rounded-lg p-4 space-y-4">
        <div>
          <p className="text-sm text-gray-700 mb-2">How does this ranking look?</p>
          <div className="flex gap-3">
            <button
              onClick={() => setSelected(true)}
              className={`px-4 py-2 rounded-lg text-sm font-medium border ${
                selected === true
                  ? "bg-green-100 border-green-500 text-green-700"
                  : "bg-white border-gray-300 text-gray-600 hover:bg-gray-50"
              }`}
            >
              Looks Good
            </button>
            <button
              onClick={() => setSelected(false)}
              className={`px-4 py-2 rounded-lg text-sm font-medium border ${
                selected === false
                  ? "bg-red-100 border-red-500 text-red-700"
                  : "bg-white border-gray-300 text-gray-600 hover:bg-gray-50"
              }`}
            >
              Needs Adjustment
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-600 mb-1">Comment (optional)</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Why is this correct/incorrect?"
            rows={2}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="text-xs text-gray-500">Submitting as: <span className="font-medium">{userName}</span></div>

        <button
          onClick={handleSubmit}
          disabled={selected === null}
          className="w-full bg-gray-900 text-white rounded-lg py-2.5 text-sm font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Submit Feedback
        </button>
      </div>
    </div>
  );
}
