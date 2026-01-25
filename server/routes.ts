import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { loginRequestSchema } from "@shared/schema";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  app.get("/api/items", (req, res) => {
    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 10;
    
    const items = storage.getItems(page, limit);
    
    res.json({
      items,
      page,
      hasMore: true,
    });
  });

  app.post("/api/login", (req, res) => {
    const result = loginRequestSchema.safeParse(req.body);
    
    if (!result.success) {
      return res.status(400).json({ 
        success: false, 
        message: "Invalid credentials format" 
      });
    }
    
    const { username, password } = result.data;
    
    if (username && password) {
      return res.json({ 
        success: true, 
        message: `Login successful! Welcome, ${username}`,
        user: { username }
      });
    }
    
    return res.status(401).json({ 
      success: false, 
      message: "Invalid credentials" 
    });
  });

  return httpServer;
}
