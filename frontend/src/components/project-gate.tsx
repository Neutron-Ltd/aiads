"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useProject } from "@/contexts/project-context";

export function ProjectGate({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { currentProject, isLoading } = useProject();

  useEffect(() => {
    if (isLoading) return;
    if (pathname === "/" && !currentProject) {
      router.replace("/projects");
    }
  }, [pathname, currentProject, isLoading, router]);

  return <>{children}</>;
}
