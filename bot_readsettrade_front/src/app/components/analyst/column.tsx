"use client"
import { ColumnDef } from "@tanstack/table-core";
import { Analyst } from "@/app/type/models";
import Link from "next/link";


const truncateText = (text: string | null | undefined, maxLength: number) => {
  if (!text) return "-";
  return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
};

export const Column = (): ColumnDef<Analyst>[] => [
  {
    accessorKey: "symbol",
    header: () => <div className="text-center text-xs text-zinc-400">SYMBOL</div>,
    cell: ({ row }) => (
      <div className="text-center font-semibold text-white">
        {row.original.symbol}
      </div>
    ),
  },
  {
    accessorKey: "broker",
    header: () => <div className="text-left text-xs text-zinc-400">BROKER</div>,
    cell: ({ row }) => (
      <div className="text-sm text-zinc-300">
        {truncateText(row.original.broker, 20)}
      </div>
    ),
  },
  {
    accessorKey: "analyst",
    header: () => <div className="text-left text-xs text-zinc-400">ANALYST</div>,
    cell: ({ row }) => (
      <div className="text-sm text-zinc-400">
        {truncateText(row.original.analyst, 20)}
      </div>
    ),
  },
  {
    accessorKey: "target_price",
    header: () => <div className="text-center text-xs text-zinc-400">TARGET</div>,
    cell: ({ row }) => (
      <div className="text-center text-emerald-400 font-medium">
        {row.original.target_price || "-"}
      </div>
    ),
  },
  {
    accessorKey: "upside_downside",
    header: () => <div className="text-center text-xs text-zinc-400">UPSIDE</div>,
    cell: ({ row }) => {
      const value = row.original.upside_downside || "-";
      const isPositive = value.includes("+");

      return (
        <div
          className={`text-center font-medium ${
            isPositive ? "text-green-400" : "text-red-400"
          }`}
        >
          {value}
        </div>
      );
    },
  },
  {
    accessorKey: "recommendation",
    header: () => <div className="text-center text-xs text-zinc-400">REC</div>,
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
    header: () => <div className="text-center text-xs text-zinc-400">DATE</div>,
    cell: ({ row }) => (
      <div className="text-center text-zinc-500 text-xs">
        {row.original.report_date || "-"}
      </div>
    ),
  },
];