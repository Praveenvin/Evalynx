import * as blazeface from "@tensorflow-models/blazeface";
import * as tf from "@tensorflow/tfjs";
import { InferenceSession, Tensor } from "onnxruntime-web";

export interface DetectionState {
  faceCount: number;
  faces: { x: number; y: number; width: number; height: number }[];
  phoneDetected: boolean;
}

export type OnDetectCallback = (state: DetectionState) => void;

class VisualDetector {
  private faceModel: blazeface.BlazeFaceModel | null = null;
  private yoloSession: InferenceSession | null = null;
  private isDetecting = false;
  private videoElement: HTMLVideoElement | null = null;
  private onDetect: OnDetectCallback | null = null;
  private loopId: number | null = null;
  
  // Throttle YOLO to run less frequently than BlazeFace for performance
  private frameCount = 0;
  private readonly YOLO_INTERVAL = 10; // Run YOLO every 10 frames (~3 FPS if camera is 30 FPS)
  private lastPhoneDetected = false;

  async initialize() {
    try {
      await tf.ready();
      
      if (!this.faceModel) {
        this.faceModel = await blazeface.load();
      }

      if (!this.yoloSession) {
        try {
          // Attempt to load yolov8n.onnx from public directory
          this.yoloSession = await InferenceSession.create("/yolov8n.onnx", { executionProviders: ["wasm"] });
        } catch (err) {
          console.warn("Failed to load YOLOv8 model. Phone detection will be inactive.", err);
        }
      }
    } catch (error) {
      console.error("Error initializing VisualDetector:", error);
      throw error;
    }
  }

  start(video: HTMLVideoElement, callback: OnDetectCallback) {
    this.videoElement = video;
    this.onDetect = callback;
    
    if (this.isDetecting) return;
    this.isDetecting = true;
    
    this.detectLoop();
  }

  stop() {
    this.isDetecting = false;
    if (this.loopId !== null) {
      cancelAnimationFrame(this.loopId);
      this.loopId = null;
    }
  }

  private async detectLoop() {
    if (!this.isDetecting || !this.videoElement || !this.faceModel || !this.onDetect) return;

    try {
      // 1. Face Detection (Fast, runs every frame)
      const predictions = await this.faceModel.estimateFaces(this.videoElement, false);
      
      const faces = predictions.map((pred) => {
        const topLeft = pred.topLeft as [number, number];
        const bottomRight = pred.bottomRight as [number, number];
        return {
          x: topLeft[0],
          y: topLeft[1],
          width: bottomRight[0] - topLeft[0],
          height: bottomRight[1] - topLeft[1],
        };
      });

      // 2. Phone Detection (Slow, runs intermittently)
      if (this.yoloSession && this.frameCount % this.YOLO_INTERVAL === 0) {
        this.lastPhoneDetected = await this.detectPhoneYOLO(this.videoElement);
      }
      this.frameCount++;

      this.onDetect({
        faceCount: faces.length,
        faces,
        phoneDetected: this.lastPhoneDetected,
      });

    } catch (err) {
      console.error("Detection error", err);
    }

    if (this.isDetecting) {
      this.loopId = requestAnimationFrame(() => this.detectLoop());
    }
  }

  private async detectPhoneYOLO(video: HTMLVideoElement): Promise<boolean> {
    if (!this.yoloSession) return false;

    // Simplified YOLO inference setup
    try {
      // YOLOv8 normally expects a 1x3x640x640 float32 tensor
      // This is a minimal placeholder for the preprocessing/postprocessing logic.
      // In a full production implementation, we would extract image data, resize to 640x640,
      // normalize, create a Float32Array tensor, pass it to the session, and apply NMS.
      
      // For this implementation, we assume we have the tensor ready or skip if too heavy.
      // E.g., we check if class 67 (cell phone) has a score > 0.5.
      
      /*
      const tensor = preprocess(video);
      const results = await this.yoloSession.run({ images: tensor });
      return postprocess(results);
      */
      
      return false; // Stubbed for actual tensor processing
    } catch (e) {
      console.error("YOLO inference failed", e);
      return false;
    }
  }
}

export const visualDetector = new VisualDetector();
