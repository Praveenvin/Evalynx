import { useEffect, useState } from "react";
import { History, Eye, Loader2 } from "lucide-react";
import Button from "./Button";
import Pagination from "./common/Pagination";
import { getMockInterviewHistory, getMockInterviewHistoryDetail, type MockInterviewHistoryItem } from "../services/historyApi";

interface MockInterviewHistoryProps {
  onClose: () => void;
  onSelectDetail: (detail: any) => void;
}

export default function MockInterviewHistory({ onClose, onSelectDetail }: MockInterviewHistoryProps) {
  const [items, setItems] = useState<MockInterviewHistoryItem[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);

  useEffect(() => {
    loadHistory(page);
  }, [page]);

  const loadHistory = async (p: number) => {
    setIsLoading(true);
    try {
      const res = await getMockInterviewHistory(p, 10);
      setItems(res.items);
      setTotalPages(res.total_pages);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewDetails = async (id: string) => {
    setIsDetailLoading(true);
    try {
      const res = await getMockInterviewHistoryDetail(id);
      onSelectDetail(res);
    } catch (err) {
      console.error("Failed to load history details", err);
    } finally {
      setIsDetailLoading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-border bg-surface p-5 sm:p-6 mt-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-display text-xl font-semibold text-ink">Mock Interview History</h2>
          <p className="mt-1 text-sm text-ink-faint">Your past mock interviews</p>
        </div>
        <Button variant="ghost" size="sm" onClick={onClose}>
          Close History
        </Button>
      </div>

      {isLoading ? (
        <div className="flex h-32 items-center justify-center text-ink-faint">
          <Loader2 className="animate-spin" size={24} />
        </div>
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <History size={40} className="text-ink-faint/50 mb-4" />
          <h3 className="text-sm font-medium text-ink">No interview history yet.</h3>
          <p className="mt-1 text-sm text-ink-soft">Your completed mock interviews will appear here.</p>
          <Button className="mt-4" onClick={onClose}>Start Mock Interview</Button>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-ink-soft">
              <thead className="border-b border-border text-xs uppercase text-ink-faint">
                <tr>
                  <th className="pb-3 pr-4 font-medium">Date</th>
                  <th className="pb-3 pr-4 font-medium">Role</th>
                  <th className="pb-3 pr-4 font-medium">Mode</th>
                  <th className="pb-3 pr-4 font-medium">Score</th>
                  <th className="pb-3 pr-4 font-medium">Status</th>
                  <th className="pb-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {items.map((item) => (
                  <tr key={item.id} className="transition-colors hover:bg-canvas/50">
                    <td className="py-3 pr-4 whitespace-nowrap">{new Date(item.created_at).toLocaleDateString()}</td>
                    <td className="py-3 pr-4 capitalize">{item.role || "Resume-based"}</td>
                    <td className="py-3 pr-4 capitalize">{item.mode}</td>
                    <td className="py-3 pr-4">{item.overall_score !== null ? `${item.overall_score}%` : "-"}</td>
                    <td className="py-3 pr-4">{item.is_complete ? "Completed" : "Incomplete"}</td>
                    <td className="py-3 text-right">
                      <Button 
                        variant="secondary" 
                        size="sm" 
                        onClick={() => handleViewDetails(item.id)} 
                        disabled={isDetailLoading || !item.is_complete}
                        className={!item.is_complete ? "opacity-50" : ""}
                      >
                        <Eye size={14} /> <span className="hidden sm:inline">View</span>
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
