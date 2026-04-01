import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

// Secret key สำหรับ verify JWT (ต้องเหมือนกับที่ backend ใช้)
// เวลา proxy.ts call /api/auth/me ไปที่ Render → Render ยังไม่ตื่น (ใช้เวลา 30+ วินาที) → fetch timeout → catch → redirect กลับ / → cookie หาย
const SECRET_KEY = new TextEncoder().encode(
  process.env.JWT_SECRET ?? "your-secret-key"
);

// const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const token = req.cookies.get("jwt")?.value;

  const isStock = pathname.startsWith("/stock");
  const isAuth = pathname === "/" || pathname.startsWith("/register");

  // กันไป stock
  if (isStock) {
      if (!token) {
        return NextResponse.redirect(new URL("/", req.url));
      }
      // const res = await fetch(`${API_BASE}/api/auth/me`, {
      //   headers: {
      //     cookie: `jwt=${token}`,
      //   },
      //   cache: "no-store",
      // });

      // if (!res.ok) {
      //   return NextResponse.redirect(new URL("/", req.url));
      // }
      
    try {
      await jwtVerify(token, SECRET_KEY, {
        algorithms: ["HS256"],
      });
    } catch (e) {
      console.log("jwt error", e);
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