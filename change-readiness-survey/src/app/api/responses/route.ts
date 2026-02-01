import { NextRequest, NextResponse } from "next/server";
import { v4 as uuidv4 } from "uuid";
import { createResponse } from "@/lib/db";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const { company_name, project_name, go_live_date, respondent_role, respondent_email } = body;

    if (!company_name || !project_name) {
      return NextResponse.json(
        { error: "company_name and project_name are required" },
        { status: 400 }
      );
    }

    const id = uuidv4();

    await createResponse({
      id,
      company_name,
      project_name,
      go_live_date: go_live_date || undefined,
      respondent_role: respondent_role || undefined,
      respondent_email: respondent_email || undefined,
    });

    return NextResponse.json({ id });
  } catch (error) {
    console.error("Error creating response:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
