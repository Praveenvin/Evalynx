import { ShieldCheck, Video, Layout, FileText, Smartphone } from "lucide-react";
import Button from "../Button";

interface ProctoringRulesModalProps {
  onAccept: () => void;
  onCancel: () => void;
}

export default function ProctoringRulesModal({ onAccept, onCancel }: ProctoringRulesModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="w-full max-w-md overflow-hidden rounded-2xl bg-surface shadow-xl border border-border">
        <div className="flex flex-col items-center justify-center bg-accent-soft p-6">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent text-white shadow-md">
            <ShieldCheck size={24} />
          </div>
          <h2 className="mt-4 text-xl font-bold text-ink">Proctored Interview</h2>
          <p className="mt-2 text-center text-sm text-ink-soft">
            This interview uses camera-based proctoring to maintain a fair environment.
          </p>
        </div>

        <div className="p-6">
          <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-ink-faint">
            During the interview:
          </h3>
          
          <ul className="flex flex-col gap-4">
            <li className="flex items-start gap-3">
              <Video className="text-accent mt-0.5" size={18} />
              <div>
                <p className="text-sm font-medium text-ink">Your camera must remain enabled</p>
                <p className="text-xs text-ink-soft">Ensure your face is clearly visible at all times.</p>
              </div>
            </li>
            
            <li className="flex items-start gap-3">
              <Layout className="text-accent mt-0.5" size={18} />
              <div>
                <p className="text-sm font-medium text-ink">Keep your browser in fullscreen</p>
                <p className="text-xs text-ink-soft">Do not switch tabs or exit fullscreen mode.</p>
              </div>
            </li>
            
            <li className="flex items-start gap-3">
              <FileText className="text-accent mt-0.5" size={18} />
              <div>
                <p className="text-sm font-medium text-ink">No copying or pasting</p>
                <p className="text-xs text-ink-soft">Using the clipboard is disabled and monitored.</p>
              </div>
            </li>
            
            <li className="flex items-start gap-3">
              <Smartphone className="text-accent mt-0.5" size={18} />
              <div>
                <p className="text-sm font-medium text-ink">No mobile devices</p>
                <p className="text-xs text-ink-soft">Mobile phones detected in view will trigger a violation.</p>
              </div>
            </li>
          </ul>

          <div className="mt-6 rounded-xl bg-warn/10 p-4 border border-warn/20">
            <p className="text-xs text-warn-strong font-medium">
              Important: Accumulating 10 violations will automatically submit and end your interview.
            </p>
          </div>

          <div className="mt-6 text-center text-xs text-ink-faint">
            Your webcam video is not recorded or stored. Only proctoring violation metadata is saved.
          </div>

          <div className="mt-6 flex gap-3">
            <Button variant="outline" className="flex-1" onClick={onCancel}>
              Cancel
            </Button>
            <Button className="flex-1" onClick={onAccept}>
              Allow Camera & Start
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
