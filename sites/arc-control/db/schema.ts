import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
export const records = sqliteTable('arc_records', {
  id: text('id').primaryKey(),
  kind: text('kind').notNull(),
  title: text('title').notNull(),
  payload: text('payload').notNull(),
  revision: integer('revision').notNull().default(1),
  updatedAt: text('updated_at').notNull(),
});
