type ApiErrorShape = {
  detail?: string | { message?: string };
};

const defaultBaseUrl = "/api";

function buildUrl(path: string) {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? defaultBaseUrl;
  return `${baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
}

async function parseJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!text) {
    return {} as T;
  }

  try {
    return JSON.parse(text) as T;
  } catch {
    return text as unknown as T;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);

  if (init?.body instanceof FormData) {
    headers.delete("Content-Type");
  } else if (init?.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const token = typeof window !== "undefined" ? window.localStorage.getItem("authToken") : null;
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(buildUrl(path), {
    ...init,
    headers,
  });

  if (!response.ok) {
    const payload = (await parseJson<ApiErrorShape>(response)) as ApiErrorShape;
    const detail = typeof payload.detail === "string" ? payload.detail : payload.detail?.message;
    throw new Error(detail ?? `Request failed with status ${response.status}`);
  }

  return parseJson<T>(response);
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
}

export interface RegisterResponse {
  id: string;
  email: string;
  created_at: string;
}

export interface MistakeFrequency {
  category: string;
  opportunities: number;
  occurances: number;
}

export interface DetectedMistake {
  category: string;
  original_text: string;
  correction: string;
  explanation: string;
}

export interface SpeechAnalysis {
  frequencies: MistakeFrequency[];
  mistakes: DetectedMistake[];
  feedback: string;
}

export interface SpeechCreationResponse {
  id: string;
  created_at: string;
  transcript: string;
  analysis: SpeechAnalysis;
}

export interface Timeframe {
  start: string;
  end: string;
}

export interface DistributionResponse {
  total_samples: number;
  mistake_frequencies: MistakeFrequency[];
}

export interface TimeSeriesPoint {
  time: string;
  opportunities: number;
  occurances: number;
}

export interface TimeSeriesResponse {
  points: TimeSeriesPoint[];
}

export const authApi = {
  login: (payload: LoginRequest) =>
    request<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  register: (payload: RegisterRequest) =>
    request<RegisterResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export const speechApi = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    return request<SpeechCreationResponse>("/speeches/", {
      method: "POST",
      body: formData,
    });
  },
};

export const analyticsApi = {
  getDistribution: (timeframe: Timeframe) =>
    request<DistributionResponse>("/analytics/distribution", {
      method: "POST",
      body: JSON.stringify({ timeframe }),
    }),
  getTimeSeries: (timeframe: Timeframe, mistakeCategory: string) =>
    request<TimeSeriesResponse>("/analytics/time-series", {
      method: "POST",
      body: JSON.stringify({ timeframe, mistake_category: mistakeCategory }),
    }),
};

export function saveAuthToken(token: string) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem("authToken", token);
  }
}

export function clearAuthToken() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem("authToken");
  }
}

export function getStoredAuthToken() {
  if (typeof window === "undefined") {
    return null;
  }

  return window.localStorage.getItem("authToken");
}
