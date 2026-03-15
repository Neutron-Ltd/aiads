import axios from "axios";

const baseURL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Project {
  id: number;
  project_name: string;
  target_url: string;
  google_ads_customer_id: string;
  created_at: string;
}

export interface ProjectCreate {
  project_name: string;
  target_url: string;
  google_ads_customer_id?: string;
}

export interface ProjectUpdate {
  project_name?: string;
  target_url?: string;
  google_ads_customer_id?: string;
}

export interface Campaign {
  id: number;
  project_id: number;
  campaign_name: string;
  budget: number;
  bidding_strategy: string;
  status: string;
  created_at: string;
  keywords?: Keyword[];
  ad_copies?: AdCopy[];
}

export interface Keyword {
  id: number;
  campaign_id: number;
  keyword_text: string;
  intent: string;
  match_type: string;
  status: string;
}

export interface AdCopyHeadline {
  id: number;
  text: string;
  position: number;
  is_pinned: boolean;
}

export interface AdCopyDescription {
  id: number;
  text: string;
  position: number;
  is_pinned: boolean;
}

export interface AdCopy {
  id: number;
  campaign_id: number;
  created_at: string;
  headlines: AdCopyHeadline[];
  descriptions: AdCopyDescription[];
}

export interface ProjectWithCampaigns extends Project {
  campaigns: Campaign[];
}

export async function getProjects(): Promise<Project[]> {
  const { data } = await api.get<Project[]>("/api/v1/projects");
  return data;
}

export async function createProject(
  project: ProjectCreate
): Promise<Project> {
  const { data } = await api.post<Project>("/api/v1/projects", project);
  return data;
}

export async function getProject(id: number): Promise<Project> {
  const { data } = await api.get<Project>(`/api/v1/projects/${id}`);
  return data;
}

export async function getProjectFull(
  id: number
): Promise<ProjectWithCampaigns> {
  const { data } = await api.get<ProjectWithCampaigns>(
    `/api/v1/projects/${id}/full`
  );
  return data;
}

export async function updateProject(
  id: number,
  project: ProjectUpdate
): Promise<Project> {
  const { data } = await api.put<Project>(`/api/v1/projects/${id}`, project);
  return data;
}

export async function deleteProject(id: number): Promise<void> {
  await api.delete(`/api/v1/projects/${id}`);
}
