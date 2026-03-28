"use client";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { DetailAnalyst } from "@/app/type/models";
import { ArrowLeft } from "lucide-react"; //icon

export default function DetailPage() {
  const { symbol } = useParams();
  const [data, setData] = useState<DetailAnalyst[]>([]);

  const router = useRouter();
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    fetch(`${API_URL}/api/analysts/detail/${symbol}`)
      .then(res => res.json())
      .then(setData);
  }, [symbol]);

  if (!data) return <div className="text-white p-6">Loading...</div>;

  return (
    <div className="selection:bg-[#00d4aa]/30 relative flex min-h-screen flex-col overflow-hidden bg-[#0a0e1a] p-4 font-mono text-slate-200 md:p-8">
  
      {/* พื้นหลัง */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(#ffffff10_1px,transparent_1px)] bg-[size:20px_20px] opacity-20" />
      <div className="pointer-events-none absolute right-[20%] top-[-100px] h-[500px] w-[500px] rounded-full bg-[#00d4aa]/10 blur-[120px]" />
      <div className="pointer-events-none absolute bottom-[-100px] left-[10%] h-[500px] w-[500px] rounded-full bg-blue-600/5 blur-[120px]" />

      <div className="relative z-10 mx-auto w-full max-w-5xl">
        
        {/* ปุ่ม */}
        <div className="mb-6">
          <button 
            onClick={() => router.back()}
            className="group flex cursor-pointer items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-slate-400 transition-all duration-300 hover:border-[#00d4aa]/50 hover:bg-[#00d4aa]/5 hover:text-[#00d4aa]"
          >
            <ArrowLeft size={18} className="transition-transform group-hover:-translate-x-1" />
            <span className="text-sm font-bold">ย้อนกลับ</span>
          </button>
        </div>

        {/* หัวข้อหลัก */}
        <div className="mb-10 flex items-end justify-between border-b border-white/10 pb-6">
          <div>
            <h1 className="flex items-center gap-4 text-6xl font-black tracking-tighter text-white">
              {symbol}
              <span className="rounded bg-[#00d4aa] px-2 py-1 font-mono text-sm uppercase tracking-normal text-[#0a0e1a]">
                มุมมองนักวิเคราะห์
              </span>
            </h1>
          </div>
          
          <div className="hidden text-right md:block">
            <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">ทั้งหมด</div>
            <div className="text-3xl font-bold leading-none text-white">{data.length}</div>
          </div>
        </div>

        {/* รายการข้อมูลแยกตามโบรกเกอร์ */}
        <div className="space-y-12">
          {data.map((item) => (
            <div key={item.id} className="group relative">
              
              {/* ข้อมูลโบรกเกอร์และคำแนะนำ */}
              <div className="mb-4 flex flex-col justify-between gap-4 md:flex-row md:items-center">
                <div>
                  <h2 className="text-2xl font-bold tracking-tight text-[#00d4aa] uppercase">{item.broker}</h2>
                  <div className="mt-1 flex items-center gap-4 text-xs text-slate-500">
                    <span>นักวิเคราะห์: <b className="text-slate-300">{item.analyst || 'ไม่ระบุชื่อ'}</b></span>
                    <span>วันที่: <b className="text-slate-300">{item.report_date || '-'}</b></span>
                  </div>
                </div>

                <div className={`rounded-full border-2 px-6 py-2 text-center text-sm font-black tracking-wide ${
                  item.recommendation?.toLowerCase().includes('buy') 
                    ? 'border-green-500/50 bg-green-500/5 text-green-400' 
                    : item.recommendation?.toLowerCase().includes('sell')
                      ? 'border-red-500/50 bg-red-500/5 text-red-400'
                      : 'border-yellow-500/50 bg-yellow-500/5 text-yellow-500'
                }`}>
                  {item.recommendation}
                </div>
              </div>

              {/* ตารางข้อมูลเชิงลึก */}
              <div className="grid grid-cols-4 gap-4">
                
                {/* ราคาเป้าหมายและ Upside */}
                <div className="flex flex-col justify-center rounded-2xl border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-6 lg:col-span-1 shadow-xl shadow-black/20">
                  <div className="mb-4">
                    <div className="mb-1 text-[10px] font-bold uppercase tracking-widest text-slate-500">ราคาเป้าหมาย</div>
                    <div className="text-4xl font-black text-white leading-tight">฿{item.target_price}</div>
                  </div>
                  <div>
                    <div className="mb-1 text-[10px] font-bold uppercase tracking-widest text-slate-500">ส่วนต่างราคา (Upside)</div>
                    <div className="text-3xl font-black text-[#00d4aa]">{item.upside_value !== null ? item.upside_value.toFixed(2) : '-'}</div>
                  </div>
                </div>

                {/* ประมาณการกำไร (Profit & EPS) */}
                <div className="rounded-2xl border border-white/5 bg-white/[0.03] p-6 lg:col-span-3 backdrop-blur-sm">
                  <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
                    
                    {/* กำไรสุทธิ */}
                    <div className="space-y-4">
                      <h4 className="border-b border-white/5 pb-2 text-[10px] font-bold  text-slate-500">กำไรสุทธิ (ล้านบาท)</h4>
                      <div className="space-y-2">
                        <div>
                          <div className="font-mono text-[10px] text-slate-400 uppercase">ปี 2569E</div>
                          <div className="text-lg font-bold text-white">{item.profit_2569 || '-'}</div>
                        </div>
                        <div>
                          <div className="font-mono text-[10px] text-slate-400 uppercase">ปี 2570E</div>
                          <div className="text-lg font-bold text-white">{item.profit_2570 || '-'}</div>
                        </div>
                      </div>
                    </div>

                    {/* กำไรต่อหุ้น */}
                    <div className="space-y-4">
                      <h4 className="border-b border-white/5 pb-2 text-[10px] font-bold  text-slate-500">กำไรต่อหุ้น (บาท)</h4>
                      <div className="space-y-2">
                        <div>
                          <div className="font-mono text-[10px] text-slate-400 uppercase">ปี 2569E</div>
                          <div className="text-lg font-bold text-white">{item.eps_2569 || '-'}</div>
                        </div>
                        <div>
                          <div className="font-mono text-[10px] text-slate-400 uppercase">ปี 2570E</div>
                          <div className="text-lg font-bold text-white">{item.eps_2570 || '-'}</div>
                        </div>
                      </div>
                    </div>

                    {/* อัตราส่วนทางการเงิน */}
                    <div className="space-y-4">
                      <h4 className="border-b mt-[0.5px] border-white/5 pb-2 text-[10px] font-bold  text-slate-500">ความคุ้มค่า (เท่า)</h4>
                      <div className="space-y-1">
                        <div className="flex items-center gap-4">
                          <span className="font-mono text-[10px] text-slate-400">P/E 69 :</span>
                          <span className="text-sm font-bold text-white">{item.pe_2569}</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="font-mono text-[10px] text-slate-400">P/E 70 :</span>
                          <span className="text-sm font-bold text-white">{item.pe_2570}</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="font-mono text-[10px] text-slate-400">P/BV 69 :</span>
                          <span className="text-sm font-bold text-white">{item.pbv_2569}</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="font-mono text-[10px] text-slate-400">P/BV 70 :</span>
                          <span className="text-sm font-bold text-white">{item.pbv_2570}</span>
                        </div>
                      </div>
                    </div>

                    {/* ปันผลคาดการณ์ */}
                    <div className="flex w-full flex-col justify-center rounded-xl border border-blue-500/20 bg-blue-500/10 p-4 text-center">
                      <h4 className="mb-2 text-[10px] font-bold text-blue-400 uppercase">อัตราปันผล</h4>
                      <div className="text-lg font-black text-blue-300">
                        30.69%, 40.55%
                      </div>
                      <div className="mt-1 text-[9px] text-blue-400/50 uppercase">ประมาณการปี 69-70</div>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}