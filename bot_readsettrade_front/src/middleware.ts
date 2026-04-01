import { NextRequest, NextResponse } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const token = req.cookies.get("jwt")?.value;

  const isStock = pathname.startsWith("/stock");
  const isAuth = pathname === "/" || pathname.startsWith("/register");

  // กันไป stock
  if (isStock) {
    try {
      if (!token) {
        return NextResponse.redirect(new URL("/", req.url));
      }
      const res = await fetch(`${API_BASE}/api/auth/me`, {
        headers: {
          cookie: `jwt=${token}`,
        },
        cache: "no-store",
      });

      if (!res.ok) {
        return NextResponse.redirect(new URL("/", req.url));
      }
    } catch {
      return NextResponse.redirect(new URL("/", req.url));
    }
  }

  // login แล้วห้ามเข้า login/register
  if (isAuth && token) {
    return NextResponse.redirect(new URL("/stock", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/stock/:path*", "/", "/register"],
};