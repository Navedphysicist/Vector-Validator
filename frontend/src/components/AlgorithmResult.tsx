interface Props {
  roleFamily: string;
  p1: string;
  p2: string;
  p3: string;
  vectors: { business_model: string; industry: string; transaction_platform: string };
}

const VECTOR_MAP: Record<string, keyof Props["vectors"]> = {
  Model: "business_model",
  Industry: "industry",
  Platform: "transaction_platform",
};

export default function AlgorithmResult({ roleFamily, p1, p2, p3, vectors }: Props) {
  const priorities = [
    { label: "P1", value: p1, border: "border-blue-500", badge: "bg-blue-600 text-white", text: "text-gray-900", tag: "Highest Priority", tagColor: "text-blue-600 bg-blue-50" },
    { label: "P2", value: p2, border: "border-gray-400", badge: "bg-gray-400 text-white", text: "text-gray-700", tag: null, tagColor: "" },
    { label: "P3", value: p3, border: "border-gray-300", badge: "bg-gray-300 text-gray-600", text: "text-gray-500", tag: null, tagColor: "" },
  ];

  return (
    <div className="space-y-3">
      <div>
        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Role Family</span>
        <p className="text-lg font-bold text-gray-900 mt-0.5">{roleFamily}</p>
      </div>
      <div className="space-y-2">
        {priorities.map(({ label, value, border, badge, text, tag, tagColor }) => {
          const vectorKey = VECTOR_MAP[value];
          const vectorValue = vectorKey ? vectors[vectorKey] : "";
          return (
            <div
              key={label}
              className={`flex items-center gap-3 bg-white rounded-lg px-4 py-3 border-l-4 ${border}`}
            >
              <span className={`text-xs font-bold px-2 py-0.5 rounded ${badge}`}>{label}</span>
              <span className={`text-sm font-semibold ${text}`}>{value}</span>
              {vectorValue && (
                <span className="text-sm text-gray-500">{vectorValue}</span>
              )}
              {tag && (
                <span className={`ml-auto text-xs font-medium px-2 py-0.5 rounded ${tagColor}`}>{tag}</span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
