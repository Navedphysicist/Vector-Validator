interface Props {
  roleFamily: string;
  p1: string;
  p2: string;
  p3: string;
  vectors: { business_model: string; industry: string; transaction_platform: string };
  tiers: Record<string, string>;
}

const VECTOR_MAP: Record<string, keyof Props["vectors"]> = {
  Model: "business_model",
  Industry: "industry",
  Platform: "transaction_platform",
};

const VECTOR_DISPLAY_NAME: Record<string, string> = {
  Model: "Business Model",
  Industry: "Industry",
  Platform: "Transaction Platform",
};

export default function AlgorithmResult({ roleFamily, p1, p2, p3, vectors, tiers }: Props) {
  const uniqueVectors = Object.entries(tiers)
    .filter(([, tier]) => tier === "Unique")
    .map(([name]) => name);

  const priorities = [
    { label: "P1", value: p1, border: "border-blue-500", badge: "bg-blue-600 text-white", text: "text-gray-900" },
    { label: "P2", value: p2, border: "border-gray-400", badge: "bg-gray-400 text-white", text: "text-gray-700" },
    { label: "P3", value: p3, border: "border-gray-300", badge: "bg-gray-300 text-gray-600", text: "text-gray-500" },
  ];

  return (
    <div className="space-y-3">
      {/* Role Family */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3">
        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Role Family</span>
        <p className="text-sm font-semibold text-gray-900 mt-0.5">{roleFamily}</p>
      </div>

      {/* Unique Vectors Callout */}
      {uniqueVectors.length > 0 ? (
        <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 space-y-1">
          <span className="text-xs font-semibold text-amber-800 uppercase tracking-wide">Unique Vectors</span>
          {uniqueVectors.map((name) => {
            const vectorKey = VECTOR_MAP[name];
            const vectorValue = vectorKey ? vectors[vectorKey] : "";
            const displayName = VECTOR_DISPLAY_NAME[name] || name;
            return (
              <p key={name} className="text-sm text-amber-800">
                <span className="font-medium">{displayName}:</span> {vectorValue || name}
              </p>
            );
          })}
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3">
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Vector Classification</span>
          <p className="text-sm text-gray-600 mt-0.5">No unique vectors detected — all vectors are common. Using default priority order for this role family.</p>
        </div>
      )}

      {/* Final Prioritization */}
      <div className="bg-white border-2 border-blue-200 rounded-xl shadow-sm overflow-hidden">
        <div className="bg-blue-50 px-4 py-3 border-b border-blue-200">
          <h3 className="text-sm font-bold text-blue-900 uppercase tracking-wide">Final Prioritization</h3>
        </div>
        <div className="divide-y divide-gray-100">
          {priorities.map(({ label, value, border, badge, text }, index) => {
            const vectorKey = VECTOR_MAP[value];
            const vectorValue = vectorKey ? vectors[vectorKey] : "";
            const isUnique = tiers[value] === "Unique";
            const isP1 = index === 0;
            return (
              <div
                key={label}
                className={`flex items-center gap-3 px-4 py-3.5 border-l-4 ${border} ${isP1 ? "bg-blue-50/30" : ""}`}
              >
                <span className={`text-xs font-bold px-2.5 py-1 rounded ${badge}`}>{label}</span>
                <div className="flex-1 min-w-0">
                  <span className={`text-sm font-semibold ${text}`}>{value}</span>
                  {vectorValue && (
                    <span className="text-sm text-gray-500 ml-2">{vectorValue}</span>
                  )}
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {isUnique && (
                    <span className="text-xs font-medium px-2 py-0.5 rounded text-amber-700 bg-amber-50 border border-amber-200">Unique</span>
                  )}
                  {isP1 && (
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded text-blue-700 bg-blue-100 border border-blue-200">Highest Priority</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
