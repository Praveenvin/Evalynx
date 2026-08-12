import { useEffect, useState } from "react";
import { History, Eye, Loader2 } from "lucide-react";
import Button from "./Button";
import Pagination from "./common/Pagination";
import { getCourseRecommendationHistory, getCourseRecommendationHistoryDetail, type CourseRecommendationHistoryItem } from "../services/historyApi";

interface CourseRecommendationHistoryProps {
  onClose: () => void;
  onSelectDetail: (detail: any) => void;
}

export default function CourseRecommendationHistory({ onClose, onSelectDetail }: CourseRecommendationHistoryProps) {
  const [items, setItems] = useState<CourseRecommendationHistoryItem[]>([]);
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
      const res = await getCourseRecommendationHistory(p, 10);
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
      const res = await getCourseRecommendationHistoryDetail(id);
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
          <h2 className="font-display text-xl font-semibold text-ink">Course Recommendation History</h2>
          <p className="mt-1 text-sm text-ink-faint">Your past learning paths</p>
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
          <h3 className="text-sm font-medium text-ink">No recommendations yet.</h3>
          <p className="mt-1 text-sm text-ink-soft">Your generated learning paths will appear here.</p>
          <Button className="mt-4" onClick={onClose}>Start Course Recommendation</Button>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-ink-soft">
              <thead className="border-b border-border text-xs uppercase text-ink-faint">
                <tr>
                  <th className="pb-3 pr-4 font-medium">Date</th>
                  <th className="pb-3 pr-4 font-medium">Name</th>
                  <th className="pb-3 pr-4 font-medium">Career Goal</th>
                  <th className="pb-3 pr-4 font-medium">Courses</th>
                  <th className="pb-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {items.map((item) => (
                  <tr key={item.id} className="transition-colors hover:bg-canvas/50">
                    <td className="py-3 pr-4 whitespace-nowrap">{new Date(item.created_at).toLocaleDateString()}</td>
                    <td className="py-3 pr-4 capitalize">{item.student_name}</td>
                    <td className="py-3 pr-4 capitalize">{item.career_goal}</td>
                    <td className="py-3 pr-4">{item.course_count}</td>
                    <td className="py-3 text-right">
                      <Button 
                        variant="secondary" 
                        size="sm" 
                        onClick={() => handleViewDetails(item.id)} 
                        disabled={isDetailLoading}
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
