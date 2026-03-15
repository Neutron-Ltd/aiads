"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  createProject,
  deleteProject,
  getProjects,
  type Project,
  type ProjectCreate,
} from "@/lib/api";
import { useProject } from "@/contexts/project-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FolderOpen, Plus } from "lucide-react";

export default function ProjectsPage() {
  const router = useRouter();
  const { loadProject } = useProject();
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formData, setFormData] = useState<ProjectCreate>({
    project_name: "",
    target_url: "",
    google_ads_customer_id: "",
  });
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    setIsLoading(true);
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load projects"
      );
      setProjects([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.project_name.trim()) return;
    setIsCreating(true);
    setError(null);
    try {
      const project = await createProject(formData);
      await loadProject(project.id);
      setDialogOpen(false);
      setFormData({
        project_name: "",
        target_url: "",
        google_ads_customer_id: "",
      });
      router.push("/");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create project"
      );
    } finally {
      setIsCreating(false);
    }
  };

  const handleOpenProject = async (id: number) => {
    try {
      await loadProject(id);
      router.push("/");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to open project"
      );
    }
  };

  const handleDeleteProject = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    if (!confirm("Delete this project? This cannot be undone.")) return;
    try {
      await deleteProject(id);
      await fetchProjects();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to delete project"
      );
    }
  };

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Project Manager
          </h1>
          <p className="mt-2 text-muted-foreground">
            Select an existing project or create a new one to get started.
          </p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger>
            <Button>
              <Plus className="mr-2 size-4" />
              New Project
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Project</DialogTitle>
              <DialogDescription>
                Enter a name and target URL for your project.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleCreateProject}>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <label htmlFor="project_name" className="text-sm font-medium">
                    Project Name
                  </label>
                  <Input
                    id="project_name"
                    value={formData.project_name}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        project_name: e.target.value,
                      }))
                    }
                    placeholder="My Ads Project"
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <label htmlFor="target_url" className="text-sm font-medium">
                    Target URL
                  </label>
                  <Input
                    id="target_url"
                    type="url"
                    value={formData.target_url}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        target_url: e.target.value,
                      }))
                    }
                    placeholder="https://example.com"
                  />
                </div>
                <div className="grid gap-2">
                  <label
                    htmlFor="google_ads_customer_id"
                    className="text-sm font-medium"
                  >
                    Google Ads Customer ID
                  </label>
                  <Input
                    id="google_ads_customer_id"
                    value={formData.google_ads_customer_id || ""}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        google_ads_customer_id: e.target.value,
                      }))
                    }
                    placeholder="123-456-7890"
                  />
                  <p className="text-xs text-muted-foreground">
                    Required for production. Links this project to your Google
                    Ads account.
                  </p>
                </div>
              </div>
              {error && (
                <p className="mb-4 text-sm text-destructive">{error}</p>
              )}
              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setDialogOpen(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={isCreating}>
                  {isCreating ? "Creating..." : "Create & Open"}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {error && !dialogOpen && (
        <p className="mb-4 rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </p>
      )}

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-5 w-32 rounded bg-muted" />
                <div className="h-4 w-48 rounded bg-muted" />
              </CardHeader>
            </Card>
          ))}
        </div>
      ) : projects.length === 0 ? (
        <Card className="border-dashed">
          <CardHeader>
            <CardTitle>No projects yet</CardTitle>
            <CardDescription>
              Create your first project to start managing Google Ads campaigns
              with AI assistance.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => setDialogOpen(true)}>
              <Plus className="mr-2 size-4" />
              Create Project
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <Card
              key={project.id}
              className="cursor-pointer transition-colors hover:bg-muted/50"
              onClick={() => handleOpenProject(project.id)}
            >
              <CardHeader className="flex flex-row items-start gap-4">
                <div className="rounded-lg bg-primary/10 p-2">
                  <FolderOpen className="size-5 text-primary" />
                </div>
                <div className="min-w-0 flex-1">
                  <CardTitle className="truncate">
                    {project.project_name}
                  </CardTitle>
                  <CardDescription className="truncate">
                    {project.google_ads_customer_id ||
                      project.target_url ||
                      "No Google Ads account linked"}
                  </CardDescription>
                </div>
              </CardHeader>
              <CardFooter className="flex justify-between">
                <Button size="sm" onClick={() => handleOpenProject(project.id)}>
                  Open
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                  onClick={(e) => handleDeleteProject(e, project.id)}
                >
                  Delete
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
