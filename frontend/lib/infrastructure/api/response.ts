import { ApiContractError, ApiError, throwApiError } from "./errors";
import {
  EmailAlreadyRegistered,
  InvalidAudio,
  InvalidCredentials,
  InvalidCurrentPassword,
  InvalidToken,
  QuotaReached,
  RequestRejected,
  SpeechNotFound,
} from "@/lib/application/errors";

interface WireResponse<T> {
  data?: T;
  error?: unknown;
  response: Response;
}

function translateApiError(error: unknown): never {
  if (!(error instanceof ApiError)) throw error;

  switch (error.code) {
    case "ALREADY_REGISTERED":
      throw new EmailAlreadyRegistered();
    case "INVALID_CREDENTIALS":
      throw new InvalidCredentials();
    case "INVALID_CURRENT_PASSWORD":
      throw new InvalidCurrentPassword();
    case "INVALID_TOKEN":
      throw new InvalidToken();
    case "SPEECH_NOT_FOUND":
      throw new SpeechNotFound();
    case "INVALID_AUDIO":
      throw new InvalidAudio(error.detail);
    case "QUOTA_REACHED":
      throw new QuotaReached();
    case "VALIDATION_ERROR":
    case "UNEXPECTED":
      throw new RequestRejected(error.detail, { cause: error });
  }
}

export async function requireData<T>(
  request: Promise<WireResponse<T>>,
): Promise<T> {
  try {
    const { data, error, response } = await request;
    if (!response.ok || error !== undefined) throwApiError(response, error);
    if (data === undefined) {
      throw new ApiContractError("API success response did not contain a body");
    }
    return data;
  } catch (error) {
    return translateApiError(error);
  }
}

export async function requireNoContent(
  request: Promise<WireResponse<unknown>>,
): Promise<void> {
  try {
    const { error, response } = await request;
    if (!response.ok || error !== undefined) throwApiError(response, error);
    if (response.status !== 204) {
      throw new ApiContractError(
        `API returned ${response.status}; expected a no-content response`,
      );
    }
  } catch (error) {
    translateApiError(error);
  }
}
