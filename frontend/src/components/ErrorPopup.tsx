import { AlertCircle, ShieldAlert, WifiOff, Activity } from "lucide-react";

export type ApiErrorCode = 
  | "INVALID_API_KEY"
  | "RATE_LIMITED"
  | "QUOTA_EXCEEDED"
  | "AI_SERVICE_UNAVAILABLE"
  | "AI_TIMEOUT"
  | "MISSING_API_KEY"
  | "AI_REQUEST_FAILED";

export interface ApiErrorDetail {
  code: ApiErrorCode;
  message: string;
}

interface ErrorPopupProps {
  error: string | ApiErrorDetail;
}

export default function ErrorPopup({ error }: ErrorPopupProps) {
  if (typeof error === "string") {
    return (
      <div className="mb-4 flex items-start gap-3 rounded-xl border border-weak bg-weak-soft/30 p-4 text-sm text-weak">
        <AlertCircle size={18} className="mt-0.5 shrink-0" />
        <div>
          <p className="font-semibold">Error</p>
          <p className="mt-1 opacity-90">{error}</p>
        </div>
      </div>
    );
  }

  let title = "AI Service Error";
  let icon = <AlertCircle size={18} className="mt-0.5 shrink-0" />;

  switch (error.code) {
    case "INVALID_API_KEY":
    case "MISSING_API_KEY":
      title = "Invalid API Key";
      icon = <ShieldAlert size={18} className="mt-0.5 shrink-0 text-warn" />;
      break;
    case "RATE_LIMITED":
    case "QUOTA_EXCEEDED":
      title = "Evalynx AI limit reached";
      icon = <Activity size={18} className="mt-0.5 shrink-0 text-warn" />;
      break;
    case "AI_TIMEOUT":
    case "AI_SERVICE_UNAVAILABLE":
      title = "AI Service Unavailable";
      icon = <WifiOff size={18} className="mt-0.5 shrink-0 text-warn" />;
      break;
  }

  return (
    <div className="mb-4 flex items-start gap-3 rounded-xl border border-warn/30 bg-warn/10 p-4 text-sm text-warn">
      {icon}
      <div>
        <p className="font-semibold">{title}</p>
        <p className="mt-1 opacity-90">{error.message}</p>
      </div>
    </div>
  );
}
