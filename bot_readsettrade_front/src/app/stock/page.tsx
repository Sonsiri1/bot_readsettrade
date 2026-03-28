"use client"
import { DataTable } from "@/app/components/analyst/data-table";
import { Column } from "@/app/components/analyst/column";
import { AnalystColumn } from "@/app/type/models";
import React from "react";
import SearchWithDetails from "@/app/components/ui/SearchWithDetails";
import Card from "@/app/components/analyst/Card";

const AnalystConsensusPage = () => {
  const [symbols, setSymbols] = React.useState<string[]>([]);
  const [symbol, setSymbol] = React.useState("AH");
  const [data, setData] = React.useState<AnalystColumn[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  console.log(`${API_URL}/api/symbols`);
  // Define an asynchronous function inside the effect
  const fetchData = async () => {
    try {
      const response = await fetch(`${API_URL}/api/analysts/${symbol}`);
      if (!response.ok) {
        console.log("Network response was not ok");
      }
      const result = await response.json();
      const flatData = Object.values(result).flat() as AnalystColumn[];
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
        < Card data={data}/>
      </div>
      < SearchWithDetails symbol={symbol} setSymbol={setSymbol} symbols={symbols}/>
      <DataTable<AnalystColumn, unknown>
        columns={Column()}
        data={data}
        loading={isLoading}
      />
    </div>
  );
}
 
export default AnalystConsensusPage