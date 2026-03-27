"use client";
import { useState } from "react";
import { useRouter } from 'next/navigation';

const Home = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const route = useRouter();
  const handleClick = async (username: string, password: string) => {
    const res = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      const data = await res.json();
      const token = data.token;
      localStorage.setItem('jwt', token);
      route.push('/stock');
    } else {
      setError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่!");
      console.log('ล็อคอินไม่ผ่าน');
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0e1a] flex flex-col font-mono overflow-hidden relative selection:bg-[#00d4aa]/30">
      
      {/* Grid Background & Glow Orbs */}
      <div className="absolute inset-0 pointer-events-none opacity-20"/>
      <div className="absolute top-[-100px] right-[20%] w-[400px] h-[400px] rounded-full bg-[#00d4aa]/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-100px] left-[10%] w-[400px] h-[400px] rounded-full bg-[#00d4aa]/5 blur-[100px] pointer-events-none" />
      {/* Main content */}
      <div className="flex-1 flex items-center justify-center p-8 z-10">
        <div className="w-full max-w-[400px]">
          
          {/* Logo */}
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 mb-10">
            <div className="flex items-center gap-3 mb-2">
              <svg width="32" height="24" viewBox="0 0 32 24" className="overflow-visible">
                <polyline
                  points="2,18 8,12 14,15 20,6 26,9 30,4"
                  fill="none"
                  stroke="#00d4aa"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="animate-[draw_2s_ease_forwards_0.5s]"
                />
              </svg>
              <span className="font-sans text-xl font-bold text-white tracking-tight">
                VIEW<span className="text-[#00d4aa]">StockAnalysts</span>
              </span>
            </div>
            <p className="text-[10px] text-white/20 tracking-[0.2em] uppercase">
              สำหรับดูข้อมูลหุ้นที่วิเคราะจากนักลงทุน
            </p>
          </div>

          {/* Form Card */}
          <div className="border border-white/10 bg-white/[0.02] backdrop-blur-xl p-8 shadow-2xl animate-in fade-in zoom-in-95 duration-500 delay-150 fill-mode-both">
            <div className="mb-6">
              <div className="text-[10px] text-[#00d4aa] tracking-[0.2em] mb-1 font-semibold">LOGIN</div>
              <h1 className="font-sans text-2xl font-semibold text-white tracking-tight">เข้าสู่ระบบ</h1>
            </div>

            <div className="space-y-4 mb-4">
              <div>
                <label className="text-[10px] text-white/40 tracking-wider block mb-1.5 uppercase">
                  ชื่อผู้ใช้
                  <span className="text-red-600">
                    *
                  </span>
                </label>
                <input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  type="text"
                  placeholder="username"
                  className="w-full bg-white/5 border border-white/10 text-slate-200 px-4 py-3 text-sm font-mono outline-none transition-all focus:border-[#00d4aa] focus:bg-[#00d4aa]/5 focus:ring-4 focus:ring-[#00d4aa]/5 placeholder:text-white/10"
                />
              </div>
              <div>
                <label className="text-[10px] text-white/40 tracking-wider block mb-1.5 uppercase">
                  รหัสผ่าน 
                  <span className="text-red-600">
                    *
                  </span>
                </label>
                <div className="relative">
                  <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    className="w-full bg-white/5 border border-white/10 text-slate-200 px-4 py-3 pr-12 text-sm font-mono outline-none transition-all focus:border-[#00d4aa] focus:bg-[#00d4aa]/5 focus:ring-4 focus:ring-[#00d4aa]/5 placeholder:text-white/10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 text-[10px] hover:text-[#00d4aa] transition-colors"
                  >
                    {showPassword ? "ซ่อน" : "แสดง"}
                  </button>
                </div>
                {error && <p className="text-red-600 text-xs mt-2">{error}</p>}
              </div>
            </div>

            <button onClick={() => handleClick(username, password)} type="submit" className="w-full bg-[#00d4aa] hover:bg-[#00f0c0] text-[#0a0e1a] py-3.5 text-xs font-bold tracking-[0.15em] transition-all hover:-translate-y-0.5 active:translate-y-0 hover:shadow-2xl cursor-pointer">
              เข้าสู่ระบบ
            </button>

            <div className="mt-6 pt-6 border-t border-white/5 flex justify-between items-center text-[10px] text-white/20">
              <span>SET · mai · TFEX</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default Home