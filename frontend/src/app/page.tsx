"use client";

import Link from "next/link";
import { useProject } from "@/contexts/project-context";
import { buttonVariants } from "@/components/ui/button";

export default function DashboardPage() {
  const { currentProject } = useProject();

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="mt-2 text-muted-foreground">
            Your command center for Google Ads. View metrics, daily briefings,
            and quick insights.
          </p>
        </div>
        <Link
          href="/projects"
          className={buttonVariants({ variant: "outline", size: "sm" })}
        >
          Switch Project
        </Link>
      </div>
      {currentProject && (
        <div className="rounded-lg border bg-muted/30 p-4">
          <p className="text-sm font-medium text-muted-foreground">
            Current Project
          </p>
          <p className="mt-1 font-medium">{currentProject.project_name}</p>
          {currentProject.target_url && (
            <p className="mt-0.5 text-sm text-muted-foreground">
              {currentProject.target_url}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
