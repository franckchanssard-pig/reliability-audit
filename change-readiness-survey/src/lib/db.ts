import initSqlJs, { Database } from "sql.js";
import path from "path";
import fs from "fs";

const DB_PATH = path.join(process.cwd(), "data", "survey.db");

let db: Database | null = null;

async function getDb(): Promise<Database> {
  if (db) return db;

  // Try multiple locations for the wasm file
  const candidates = [
    path.join(process.cwd(), "node_modules", "sql.js", "dist", "sql-wasm.wasm"),
    path.join(process.cwd(), "data", "sql-wasm.wasm"),
  ];
  let wasmBinary: Buffer | null = null;
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      wasmBinary = fs.readFileSync(candidate);
      break;
    }
  }
  if (!wasmBinary) {
    throw new Error("sql-wasm.wasm not found in any expected location");
  }
  const SQL = await initSqlJs({ wasmBinary });

  // Ensure data directory exists
  const dir = path.dirname(DB_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Load existing DB or create new one
  if (fs.existsSync(DB_PATH)) {
    const buffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(buffer);
  } else {
    db = new SQL.Database();
  }

  // Create table if not exists
  db.run(`
    CREATE TABLE IF NOT EXISTS responses (
      id TEXT PRIMARY KEY,
      created_at TEXT NOT NULL,
      company_name TEXT NOT NULL,
      project_name TEXT NOT NULL,
      go_live_date TEXT,
      respondent_role TEXT,
      respondent_email TEXT,
      answers_json TEXT
    )
  `);

  persist(db);
  return db;
}

function persist(database: Database) {
  const data = database.export();
  const buffer = Buffer.from(data);
  fs.writeFileSync(DB_PATH, buffer);
}

export async function createResponse(params: {
  id: string;
  company_name: string;
  project_name: string;
  go_live_date?: string;
  respondent_role?: string;
  respondent_email?: string;
}): Promise<void> {
  const database = await getDb();
  database.run(
    `INSERT INTO responses (id, created_at, company_name, project_name, go_live_date, respondent_role, respondent_email)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      params.id,
      new Date().toISOString(),
      params.company_name,
      params.project_name,
      params.go_live_date || null,
      params.respondent_role || null,
      params.respondent_email || null,
    ]
  );
  persist(database);
}

export async function saveAnswers(
  id: string,
  answersJson: string
): Promise<void> {
  const database = await getDb();
  database.run(`UPDATE responses SET answers_json = ? WHERE id = ?`, [
    answersJson,
    id,
  ]);
  persist(database);
}

export async function getResponse(id: string): Promise<{
  id: string;
  created_at: string;
  company_name: string;
  project_name: string;
  go_live_date: string | null;
  respondent_role: string | null;
  respondent_email: string | null;
  answers_json: string | null;
} | null> {
  const database = await getDb();
  const stmt = database.prepare(
    `SELECT id, created_at, company_name, project_name, go_live_date, respondent_role, respondent_email, answers_json
     FROM responses WHERE id = ?`
  );
  stmt.bind([id]);

  if (stmt.step()) {
    const row = stmt.getAsObject() as {
      id: string;
      created_at: string;
      company_name: string;
      project_name: string;
      go_live_date: string | null;
      respondent_role: string | null;
      respondent_email: string | null;
      answers_json: string | null;
    };
    stmt.free();
    return row;
  }

  stmt.free();
  return null;
}
