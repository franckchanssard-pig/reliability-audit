import { NextRequest, NextResponse } from "next/server";
import { getResponse, saveAnswers } from "@/lib/db";
import { QUESTIONS } from "@/lib/questionnaire";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const response = await getResponse(id);

    if (!response) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    const body = await request.json();
    const { answers } = body;

    if (!answers || typeof answers !== "object") {
      return NextResponse.json(
        { error: "answers object is required" },
        { status: 400 }
      );
    }

    // Validate all 15 questions are answered with values 1-5
    for (const q of QUESTIONS) {
      const val = answers[q.id];
      if (val === undefined || val === null) {
        return NextResponse.json(
          { error: `Missing answer for ${q.id}` },
          { status: 400 }
        );
      }
      if (typeof val !== "number" || val < 1 || val > 5) {
        return NextResponse.json(
          { error: `${q.id} must be a number between 1 and 5` },
          { status: 400 }
        );
      }
    }

    await saveAnswers(id, JSON.stringify(answers));

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error saving answers:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
