export interface AnalyzeRequest {
  company: string;
  role: string;
  user_name: string;
}

export interface AnalyzeResponse {
  business_model: string;
  industry: string;
  transaction_platform: string;
}

export interface RunAlgorithmRequest {
  business_model: string;
  industry: string;
  transaction_platform: string;
  role: string;
  user_name: string;
}

export interface RunAlgorithmResponse {
  role_family: string;
  tiers: Record<string, string>;
  p1: string;
  p2: string;
  p3: string;
}

export interface FeedbackRequest {
  company: string;
  industry: string;
  business_model: string;
  transaction_platform: string;
  role: string;
  role_family: string;
  p1: string;
  p2: string;
  p3: string;
  is_correct: boolean;
  comment?: string;
  user_name: string;
}

export interface FeedbackItem {
  id: string;
  company: string;
  industry: string;
  business_model: string;
  transaction_platform: string;
  role: string;
  role_family: string;
  p1: string;
  p2: string;
  p3: string;
  is_correct: boolean;
  comment?: string;
  user_name: string;
  created_at: string;
}

export interface UserSettings {
  user_name: string;
  llm_provider: string;
  llm_model: string;
  llm_api_key?: string;
  tavily_api_key?: string;
}

export interface SettingsStatus {
  user_name: string;
  llm_provider: string;
  llm_model: string;
  has_llm_key: boolean;
  has_tavily_key: boolean;
}
