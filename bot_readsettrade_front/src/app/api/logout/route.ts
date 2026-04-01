import { NextResponse } from "next/server";

export async function POST() {
  const res = NextResponse.json({ msg: "logout success" });
  
  res.cookies.set("jwt", "", {
    httpOnly: true,
    secure: true,
    sameSite: "none",
    path: "/",
    maxAge: 0,
  });

  return res;
}