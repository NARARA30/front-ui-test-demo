import { sql } from "drizzle-orm";
import { pgTable, text, varchar, integer } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export const listItemSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
});

export const paginatedItemsSchema = z.object({
  items: z.array(listItemSchema),
  page: z.number(),
  hasMore: z.boolean(),
});

export type ListItem = z.infer<typeof listItemSchema>;
export type PaginatedItems = z.infer<typeof paginatedItemsSchema>;

export const loginRequestSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
});

export type LoginRequest = z.infer<typeof loginRequestSchema>;
