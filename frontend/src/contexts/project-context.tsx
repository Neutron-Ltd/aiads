"use client";

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import {
  type ProjectWithCampaigns,
  getProjectFull,
} from "@/lib/api";

const STORAGE_KEY = "ads-copilot-current-project-id";

interface ProjectContextValue {
  currentProject: ProjectWithCampaigns | null;
  currentProjectId: number | null;
  setCurrentProjectId: (id: number | null) => void;
  loadProject: (id: number) => Promise<void>;
  clearProject: () => void;
  isLoading: boolean;
  error: string | null;
}

const ProjectContext = createContext<ProjectContextValue | null>(null);

export function ProjectProvider({ children }: { children: React.ReactNode }) {
  const [currentProject, setCurrentProject] =
    useState<ProjectWithCampaigns | null>(null);
  const [currentProjectId, setCurrentProjectIdState] = useState<
    number | null
  >(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const setCurrentProjectId = useCallback((id: number | null) => {
    setCurrentProjectIdState(id);
    if (id === null) {
      localStorage.removeItem(STORAGE_KEY);
      setCurrentProject(null);
    } else {
      localStorage.setItem(STORAGE_KEY, String(id));
    }
  }, []);

  const loadProject = useCallback(async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const project = await getProjectFull(id);
      setCurrentProject(project);
      setCurrentProjectIdState(id);
      localStorage.setItem(STORAGE_KEY, String(id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load project");
      setCurrentProject(null);
      setCurrentProjectIdState(null);
      localStorage.removeItem(STORAGE_KEY);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearProject = useCallback(() => {
    setCurrentProject(null);
    setCurrentProjectIdState(null);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const id = parseInt(stored, 10);
      if (!isNaN(id)) {
        loadProject(id);
        return;
      }
    }
    setIsLoading(false);
  }, [loadProject]);

  const value: ProjectContextValue = {
    currentProject,
    currentProjectId,
    setCurrentProjectId,
    loadProject,
    clearProject,
    isLoading,
    error,
  };

  return (
    <ProjectContext.Provider value={value}>{children}</ProjectContext.Provider>
  );
}

export function useProject() {
  const ctx = useContext(ProjectContext);
  if (!ctx) {
    throw new Error("useProject must be used within ProjectProvider");
  }
  return ctx;
}
