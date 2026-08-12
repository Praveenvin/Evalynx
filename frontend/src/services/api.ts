export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export class ApiError extends Error {
  status: number;
  message: any;

  constructor(message: any, status: number) {
    super(typeof message === "string" ? message : "API Error");
    this.name = "ApiError";
    this.status = status;
    this.message = message;
  }
}

export async function parseJsonOrThrow<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message: any = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (body?.error) {
        message = body.error; // Passes the structured error object
      } else if (body?.detail) {
        message = body.detail;
      } else if (body?.message) {
        message = body.message;
      }
    } catch {
      // response body was not JSON, fall back to default message
    }
    throw new ApiError(message, response.status);
  }
  return response.json() as Promise<T>;
}
