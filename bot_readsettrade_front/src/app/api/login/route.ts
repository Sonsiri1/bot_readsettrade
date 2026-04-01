import { NextRequest, NextResponse } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function POST(req: NextRequest) {
  const body = await req.json();

  const backendRes = await fetch(`${API_BASE}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!backendRes.ok) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const data = await backendRes.json();

  // ดึง jwt จาก backend response cookie
  const setCookie = backendRes.headers.get("set-cookie");
  const token = setCookie?.match(/jwt=([^;]+)/)?.[1];

  if (!token) {
    return NextResponse.json({ error: "No token" }, { status: 401 });
  }

  const res = NextResponse.json(data);

  // Set cookie บน frontend domain แทน ✅
  res.cookies.set("jwt", token, {
    httpOnly: true,
    secure: true,
    sameSite: "none",
    path: "/",
    maxAge: 60 * 60 * 2, // 2 ชั่วโมง
  });

  return res;
}