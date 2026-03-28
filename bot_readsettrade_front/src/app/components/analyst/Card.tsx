import { AnalystColumn } from '@/app/type/models';
import React from 'react';

type CardProps = {
  data: AnalystColumn[];
};

const Card = ({ data }: CardProps) => {
  if (!data || data.length === 0) return null;

  const company = data?.[0]?.company;

  // ราคาเป้าหมาย
  const targets = data
    .map(d => Number(d.target_price))
    .filter((n): n is number => !isNaN(n));

  // reduce คือ การนำ array มาทำเป็นค่าเดียว เช่น เอา target_price ทั้งหมดมาหาค่าเฉลี่ย
  const avg =
    targets.length > 0
      ? (targets.reduce((a, b) => a + b, 0) / targets.length).toFixed(2)
      : "-";

  const max = targets.length > 0 ? Math.max(...targets).toFixed(2) : "-";

  const min = targets.length > 0 ? Math.min(...targets).toFixed(2) : "-";

  // อัปไซด์
  const upsides = data
    .map(d => d.upside_value)
    .filter((n): n is number => typeof n === "number");

  const maxUpside = upsides.length > 0 ? Math.max(...upsides).toFixed(2) : "-";

  return (
    <div className="mt-5 w-full rounded-2xl border border-white/10 bg-gradient-to-r from-[#0b1220] via-[#0f1c2e] to-[#132a2e] p-6 text-white">

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">

        {/* รวมที่ควรรู้ */}
        <div>
          <div className="text-xs text-zinc-500">หลักทรัพย์</div>
          <div className="text-2xl font-bold">{data?.[0]?.symbol ?? "-"}</div>

          <div className="mt-2 text-sm text-zinc-300">
            {company?.company_name}
          </div>

          <div className="text-xs text-zinc-500 mt-1">
            {company?.sector ?? "-"} • {company?.industry ?? "-"}
          </div>
        </div>

        {/* ราคาเป้าหมายเฉลี่ย */}
        <div className="text-center">
          <div className="text-xs text-zinc-500">ราคาเป้าหมายเฉลี่ย</div>
          <div className="text-xl font-bold">฿{avg}</div>
        </div>

        {/* ช่วงราคาเป้าหมาย */}
        <div className="text-center">
          <div className="text-xs text-zinc-500">ช่วงราคาเป้าหมาย</div>
          <div className="text-lg font-bold">
            ฿{min} - ฿{max}
          </div>
        </div>

        {/* อัปไซด์สูงสุด */}
        <div className="text-center">
          <div className="text-xs text-zinc-500">อัปไซด์สูงสุด</div>
          <div className="text-lg font-bold text-green-400">
            {maxUpside}%
          </div>
        </div>

      </div>

      {/* คนวิเคราะห์ทั้งหมด */}
      <div className="mt-4 text-center text-xs text-zinc-400">
        {data.length} นักวิเคราะห์
      </div>
    </div>
  );
};

export default Card;