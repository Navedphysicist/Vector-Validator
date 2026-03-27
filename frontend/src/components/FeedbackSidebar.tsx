import type { FeedbackItem } from "../lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  items: FeedbackItem[];
}

export default function FeedbackSidebar({ open, onClose, items }: Props) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-40 flex justify-end">
      <div className="absolute inset-0 bg-black/30" onClick={onClose} />
      <div className="relative w-full max-w-3xl bg-white shadow-xl overflow-auto">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-900">Validation History ({items.length})</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
        </div>

        {items.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No feedback submitted yet.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-left">
                <tr>
                  <th className="px-4 py-3 font-medium text-gray-600">Company</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Role</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Role Family</th>
                  <th className="px-4 py-3 font-medium text-gray-600">P1</th>
                  <th className="px-4 py-3 font-medium text-gray-600">P2</th>
                  <th className="px-4 py-3 font-medium text-gray-600">P3</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Correct?</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Comment</th>
                  <th className="px-4 py-3 font-medium text-gray-600">User</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-900">{item.company}</td>
                    <td className="px-4 py-3 text-gray-700">{item.role}</td>
                    <td className="px-4 py-3 text-gray-700">{item.role_family}</td>
                    <td className="px-4 py-3 font-medium text-blue-700">{item.p1}</td>
                    <td className="px-4 py-3 text-gray-700">{item.p2}</td>
                    <td className="px-4 py-3 text-gray-700">{item.p3}</td>
                    <td className="px-4 py-3">
                      {item.is_correct ? (
                        <span className="text-green-600 font-medium">Yes</span>
                      ) : (
                        <span className="text-red-600 font-medium">No</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600 max-w-48 truncate">{item.comment || "—"}</td>
                    <td className="px-4 py-3 text-gray-500">{item.user_name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
