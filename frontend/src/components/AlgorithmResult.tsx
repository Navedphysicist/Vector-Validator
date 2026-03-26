interface Props {
  roleFamily: string;
  p1: string;
  p2: string;
  p3: string;
}

export default function AlgorithmResult({ roleFamily, p1, p2, p3 }: Props) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">Result</h3>
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-blue-700">Role Family:</span>
          <span className="text-sm text-blue-900 font-semibold">{roleFamily}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-blue-700">Priority:</span>
          <div className="flex items-center gap-1.5">
            <span className="bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded">P1: {p1}</span>
            <span className="text-blue-400">&gt;</span>
            <span className="bg-blue-500 text-white text-xs font-bold px-2.5 py-1 rounded">P2: {p2}</span>
            <span className="text-blue-400">&gt;</span>
            <span className="bg-blue-400 text-white text-xs font-bold px-2.5 py-1 rounded">P3: {p3}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
