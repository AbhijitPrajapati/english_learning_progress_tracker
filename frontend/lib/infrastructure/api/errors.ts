type ErrorCode =
  | "UNEXPECTED"
  | "INVALID_CREDENTIALS"
  | "INVALID_TOKEN"
  | "ALREADY_REGISTERED"
  | "SPEECH_NOT_FOUND";
export class ApiError extends Error {
  readonly status: number;
  readonly detail: string;
  readonly code: ErrorCode;

  constructor(status: number, detail: string, code: ErrorCode) {
    super(
      `API request failed with status ${status}\nError Code: ${code}\nDetail: ${detail}`,
    );
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
    this.code = code;

    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

export class NetworkError extends Error {
  constructor(options?: ErrorOptions) {
    super("Network request failed", options);
    this.name = "NetworkError";
  }
}
