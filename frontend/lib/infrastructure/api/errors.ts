import type { components } from "./generated/schema";

export type ErrorCode = components["schemas"]["ErrorCode"];
export type ApiErrorBody = components["schemas"]["ErrorBody"];

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly detail: string,
    readonly code: ErrorCode,
  ) {
    super(`${code}: ${detail}`);
    this.name = "ApiError";
  }
}

export class NetworkError extends Error {
  constructor(options?: ErrorOptions) {
    super("Network request failed", options);
    this.name = "NetworkError";
  }
}

export class ApiContractError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiContractError";
  }
}

const ERROR_CODES = {
  UNEXPECTED: true,
  INVALID_CREDENTIALS: true,
  INVALID_CURRENT_PASSWORD: true,
  INVALID_TOKEN: true,
  ALREADY_REGISTERED: true,
  SPEECH_NOT_FOUND: true,
  INVALID_AUDIO: true,
  VALIDATION_ERROR: true,
  QUOTA_REACHED: true
} satisfies Record<ErrorCode, true>;

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.detail === "string" &&
    typeof candidate.code === "string" &&
    candidate.code in ERROR_CODES
  );
}

export function throwApiError(response: Response, error: unknown): never {
  if (isApiErrorBody(error)) {
    throw new ApiError(response.status, error.detail, error.code);
  }
  throw new ApiContractError(
    `API returned an undocumented error payload with status ${response.status}`,
  );
}
