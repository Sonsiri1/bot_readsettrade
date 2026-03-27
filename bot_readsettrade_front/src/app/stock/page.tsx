"use client"
import { DataTable } from "@/app/components/analyst/data-table";
import { Column } from "@/app/components/analyst/column";
import { Analyst } from "@/app/type/models";
import React from "react";
import Link from "next/link";
 
const AnalystConsensusPage = () => {
  const [symbol, setSymbol] = React.useState("AH");
  const [data, setData] = React.useState<Analyst[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [symbols, setSymbols] = React.useState<string[]>([]);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  // Define an asynchronous function inside the effect
  const fetchData = async () => {
    try {
      const response = await fetch(`${API_URL}/api/analysts/${symbol}`);
      if (!response.ok) {
        console.log("Network response was not ok");
      }
      const result = await response.json();
      const flatData = Object.values(result).flat() as Analyst[];
      setData(flatData);
      // console.log(flatData);
    } catch (error) {
      console.error("Error fetching data:", error);
      setData([]);
    } finally {
      setIsLoading(false);
    }
  };
  React.useEffect(() => {
    fetchData();
  }, [symbol]);

  React.useEffect(() => {
    fetch(`${API_URL}/api/symbols`)
      .then(res => res.json())
      .then(setSymbols);
  }, []);
  return (
    <div className="min-h-screen bg-[#0a0e1a] flex flex-col font-mono overflow-hidden relative selection:bg-[#00d4aa]/30 p-6">
      <div className="absolute inset-0 pointer-events-none opacity-20"/>
      <div className="absolute top-[-100px] right-[20%] w-[400px] h-[400px] rounded-full bg-[#00d4aa]/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-100px] left-[10%] w-[400px] h-[400px] rounded-full bg-[#00d4aa]/5 blur-[100px] pointer-events-none" />
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-white font-mono tracking-tight">
          Analyst Consensus
        </h1>
        <p className="text-zinc-500 text-sm mt-1">ข้อมูลจาก Broker</p>
      </div>
      <div className="flex justify-between mb-5">
        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="bg-zinc-900 text-white border border-zinc-700 px-3 py-1 rounded"
        >
          {symbols.map((sym) => (
            <option key={sym} value={sym}>
              {sym}
            </option>
          ))}
        </select>
        <Link href={`/stock/${symbol}`} className="flex justify-center items-center">
          <button className="group flex cursor-pointer items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-slate-400 transition-all duration-300 hover:border-[#00d4aa]/50 hover:bg-[#00d4aa]/5 hover:text-[#00d4aa]">
            รายละเอียด
          </button>
        </Link>
      </div>
      <DataTable<Analyst, unknown>
        columns={Column()}
        data={data}
        loading={isLoading}
      />
    </div>
  );
}
 
export default AnalystConsensusPage