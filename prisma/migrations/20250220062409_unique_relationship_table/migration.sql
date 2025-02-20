/*
  Warnings:

  - A unique constraint covering the columns `[projectId,languageId]` on the table `ProjectLanguage` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "ProjectLanguage_projectId_languageId_key" ON "ProjectLanguage"("projectId", "languageId");
