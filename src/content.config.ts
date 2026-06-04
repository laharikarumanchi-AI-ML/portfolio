import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: z.object({
    // Existing v1 fields
    title:          z.string(),
    oneLiner:       z.string(),
    headlineNumber: z.string(),
    techStack:      z.array(z.string()),
    year:           z.number(),
    githubUrl:      z.string().url().optional(),
    demoUrl:        z.string().url().optional(),
    featured:       z.boolean().default(false),
    order:          z.number(),

    // NEW v2 fields
    category:        z.enum(['Agents', 'RAG', 'Classical ML']),
    status:          z.enum(['shipped', 'in-progress']).default('shipped'),
    lastUpdated:     z.coerce.date().optional(),
    readTimeMinutes: z.number().int().positive().optional(),

    // Migration flag (removed in PR #9)
    v2:              z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { projects, blog };
