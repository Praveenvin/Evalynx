export type ViolationType = 
  | "tab_switch" 
  | "fullscreen_exit" 
  | "copy_paste" 
  | "phone_detected" 
  | "multiple_faces" 
  | "no_face";

export interface Violation {
  id: string;
  type: ViolationType;
  timestamp: number;
}

export type AutoSubmitCallback = (metadata: Violation[]) => void;
export type ToastCallback = (message: string, currentCount: number) => void;

class ViolationManager {
  private violations: Violation[] = [];
  private lastViolationTime: number = 0;
  private readonly COOLDOWN_MS = 500;
  private readonly MAX_VIOLATIONS = 10;
  private isAutoSubmitting = false;

  private onAutoSubmit: AutoSubmitCallback | null = null;
  private onToast: ToastCallback | null = null;

  setCallbacks(onAutoSubmit: AutoSubmitCallback, onToast: ToastCallback) {
    this.onAutoSubmit = onAutoSubmit;
    this.onToast = onToast;
  }

  getViolations() {
    return [...this.violations];
  }

  getViolationCount() {
    return this.violations.length;
  }

  reset() {
    this.violations = [];
    this.lastViolationTime = 0;
    this.isAutoSubmitting = false;
  }

  registerViolation(type: ViolationType, message: string) {
    if (this.isAutoSubmitting) return;

    const now = Date.now();
    if (now - this.lastViolationTime < this.COOLDOWN_MS) {
      return; // Debounce during cooldown
    }

    this.lastViolationTime = now;
    
    const violation: Violation = {
      id: Math.random().toString(36).substring(2, 9),
      type,
      timestamp: now
    };

    this.violations.push(violation);
    
    const count = this.violations.length;
    
    if (this.onToast) {
      this.onToast(message, count);
    }

    if (count >= this.MAX_VIOLATIONS) {
      this.triggerAutoSubmit();
    }
  }

  private triggerAutoSubmit() {
    if (this.isAutoSubmitting) return;
    this.isAutoSubmitting = true;
    
    if (this.onAutoSubmit) {
      this.onAutoSubmit(this.getViolations());
    }
  }
}

export const violationManager = new ViolationManager();
