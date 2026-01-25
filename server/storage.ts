import { type User, type InsertUser, type ListItem } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  getItems(page: number, limit: number): ListItem[];
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;

  constructor() {
    this.users = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  getItems(page: number, limit: number): ListItem[] {
    const startId = (page - 1) * limit + 1;
    return Array.from({ length: limit }, (_, i) => ({
      id: startId + i,
      title: `Item #${startId + i}`,
      description: `This is a dynamically loaded item for infinite scroll testing. Item number ${startId + i}.`
    }));
  }
}

export const storage = new MemStorage();
