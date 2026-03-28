import { LineChart, Line, ResponsiveContainer } from "recharts";

export default function Metrics({data, history}){

  return(
    <div className="bg-white/5 p-4 rounded-xl border border-white/10">

      <h2 className="text-sm mb-2">Metrics</h2>

      <div className="text-xs space-y-1 mb-3">

        <div>Φ: {data.Phi?.toFixed(3)}</div>
        <div>λ: {data.lyapunov?.toFixed(3)}</div>

      </div>

      <ResponsiveContainer width="100%" height={120}>
        <LineChart data={history}>
          <Line dataKey="Phi" stroke="#22c55e" dot={false}/>
          <Line dataKey="lyap" stroke="#ef4444" dot={false}/>
        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}
