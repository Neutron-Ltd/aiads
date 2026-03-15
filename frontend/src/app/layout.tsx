import type { Metadata } from "next";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppLayout } from "@/components/app-layout";
import { ProjectProvider } from "@/contexts/project-context";
import { ProjectGate } from "@/components/project-gate";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ads Co-Pilot",
  description: "Human-in-the-loop AI for Google Ads management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <TooltipProvider>
          <ProjectProvider>
            <ProjectGate>
              <AppLayout>{children}</AppLayout>
            </ProjectGate>
          </ProjectProvider>
        </TooltipProvider>
      </body>
    </html>
  );
}
