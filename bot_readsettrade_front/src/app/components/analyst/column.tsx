"use client"
import { ColumnDef } from "@tanstack/table-core";
import { AnalystColumn } from "@/app/type/models";


const truncateText = (text: string | null | undefined, maxLength: number) => {
  if (!text) return "-";
  return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
};

export const Column = (): ColumnDef<AnalystColumn>[] => [
  {
    accessorKey: "symbol",
    header: () => <div className="text-center text-xs text-zinc-400">หลักทรัพย์</div>,
    cell: ({ row }) => (
      <div className="text-center font-semibold text-white">
        {row.original.symbol}
      </div>
    ),
  },
  {
    accessorKey: "broker",
    header: () => <div className="text-left text-xs text-zinc-400">โบรกเกอร์</div>,
    cell: ({ row }) => (
      <div className="text-sm text-zinc-300" title={row.original.broker || "ไม่ระบุโบรกเกอร์"}>
        {truncateText(row.original.broker, 20)}
      </div>
    ),
  },
  {
    accessorKey: "analyst",
    header: () => <div className="text-left text-xs text-zinc-400">นักวิเคราะห์</div>,
    cell: ({ row }) => (
      <div className="text-sm text-zinc-400" title={row.original.analyst || "ไม่ระบุนักวิเคราะห์"}>
        {truncateText(row.original.analyst, 20)}
      </div>
    ),
  },
  {
    accessorKey: "target_price",
    header: () => <div className="text-center text-xs text-zinc-400">ราคาเป้าหมาย</div>,
    cell: ({ row }) => (
      <div className="text-center text-emerald-400 font-medium">
        {row.original.target_price || "-"}
      </div>
    ),
  },
  {
    accessorKey: "upside_value",
    header: () => (
      <div className="text-center text-xs text-zinc-400">อัปไซด์</div>
    ),
    cell: ({ row }) => {
      const value = row.original.upside_value;
      const text = row.original.upside_text || "-";

      // เช็คจาก number จริง (ดีที่สุด)
      const isPositive = typeof value === "number" && value > 0;
      const isNegative = typeof value === "number" && value < 0;

      return (
        <div
          className={`text-center font-medium ${
            isPositive
              ? "text-green-400"
              : isNegative
              ? "text-red-400"
              : "text-zinc-400"
          }`}
        >
          {text}
        </div>
      );
    },
  },
  {
    accessorKey: "recommendation",
    header: () => <div className="text-center text-xs text-zinc-400">คำแนะนำ</div>,
    cell: ({ row }) => {
      const rec = row.original.recommendation || "-";

      const color =
        rec.toLowerCase().includes("buy")
          ? 'border-green-500/50 text-green-400 bg-green-500/5' 
          : rec.toLowerCase().includes('sell')
            ? 'border-red-500/50 text-red-400 bg-red-500/5'
            : 'border-yellow-500/50 text-yellow-500 bg-yellow-500/5'

      return (
        <div className="flex justify-center">
          <span className={`px-2 py-1 rounded text-xs font-medium ${color}`}>
            {rec}
          </span>
        </div>
      );
    },
  },
  {
    accessorKey: "report_date",
    header: () => <div className="text-center text-xs text-zinc-400">วันที่รายงาน</div>,
    cell: ({ row }) => (
      <div className="text-center text-zinc-500 text-xs">
        {row.original.report_date || "-"}
      </div>
    ),
  },
];