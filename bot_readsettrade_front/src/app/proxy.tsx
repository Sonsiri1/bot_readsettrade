// import { NextRequest, NextResponse } from "next/server";

// const adminRoutes = ["/admin"];
// const resellerRoutes = ["/resellers"];
// const authRoutes = ["/login", "/register", "/"];

// const API_BASE = process.env.NEXT_PUBLIC_API_URL;

// export default async function proxy(req: NextRequest) {
//   const { pathname } = req.nextUrl;
//   const token = req.cookies.get("jwt")?.value;

//   console.log("Token in Middleware:", token ? "Found" : "Not Found");

//   if (authRoutes.some((r) => pathname === r)) {
//     if (token) {
//       try {
//         // ตรวจ role แล้ว redirect ไปหน้าของคนนั้น
//         const res = await fetch(`${API_BASE}/api/auth/me`, {
//           headers: {
//             Cookie: `jwt=${token}`,
//             Authorization: `Bearer ${token}`, // ส่งสำรองไปในกรณีที่ Go เช็คจาก Header ด้วย
//           },
//           cache: "no-store",
//         });
//         console.log("status:", res.status);

//         if (res.ok) {
//           const data = await res.json();
//           console.log("data:", data);
//           if (data.role === "admin") {
//             return NextResponse.redirect(new URL("/admin/dashboard", req.url));
//           } else if (data.role === "reseller") {
//             return NextResponse.redirect(
//               new URL("/resellers/dashboard", req.url),
//             );
//           }
//         }
//       } catch (err) {
//         console.log("fetch error:", err);
//         return NextResponse.redirect(new URL("/", req.url));
//       }
//     }
//     return NextResponse.next();
//   }

//   const isAdmin = adminRoutes.some((r) => pathname.startsWith(r));
//   const isReseller = resellerRoutes.some((r) => pathname.startsWith(r));

//   if (!isAdmin && !isReseller) return NextResponse.next();

//   if (!token) {
//     const loginUrl = new URL("/login", req.url);
//     return NextResponse.redirect(loginUrl);
//   }

//   const res = await fetch(`${API_BASE}/api/auth/me`, {
//     headers: { Cookie: `jwt=${token}`, Authorization: `Bearer ${token}` },
//   });

//   if (!res.ok) {
//     const loginUrl = new URL("/login", req.url);
//     return NextResponse.redirect(loginUrl);
//   }

//   const data = await res.json();
  
//   if (isAdmin && data.role !== "admin") {
//     return NextResponse.redirect(new URL("/resellers/dashboard", req.url));
//   }

//   if (isReseller && data.role !== "reseller") {
//     return NextResponse.redirect(new URL("/admin/dashboard", req.url));
//   }

//   return NextResponse.next();
// }

// export const config = {
//   matcher: ["/admin/:path*", "/resellers/:path*", "/login", "/register", "/"],
// };