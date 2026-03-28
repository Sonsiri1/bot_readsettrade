import Link from 'next/link'

type Props = {
  symbol: string;
  setSymbol: (val: string) => void;
  symbols: string[];
};
const SearchWithDetails = ({ symbol, setSymbol, symbols }: Props) => {
  return (
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
  )
}

export default SearchWithDetails