import { useEffect, useState, useRef } from "react";
import { WS_URL } from "./config";
import { motion } from "framer-motion";
import { LineChart, Line, ResponsiveContainer } from "recharts";
import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";

export default function App(){

  const ws = useRef(null);

  const [field,setField] = useState(null);
  const [Phi,setPhi] = useState(0);
  const [lyap,setLyap] = useState(0);
  const [history,setHistory] = useState([]);

  useEffect(()=>{

    const socket = new WebSocket(WS_URL);

    socket.onmessage = (e)=>{
      const d = JSON.parse(e.data);

      setField(d.field);
      setPhi(d.Phi || 0);
      setLyap(d.lyapunov || 0);

      setHistory(h=>[
        ...h.slice(-120),
        {Phi:d.Phi, lyap:d.lyapunov}
      ]);
    };

    ws.current = socket;

    return ()=>socket.close();

  },[]);

  return(
    <div className="bg-black text-white min-h-screen p-6">

      <h1 className="text-xl mb-4 opacity-80">
        MetastableX
      </h1>

      <div className="grid grid-cols-12 gap-4">

        <div className="col-span-8">
          <Glass>
            <Field field={field}/>
          </Glass>
        </div>

        <div className="col-span-4 flex flex-col gap-4">

          <MetricCard
            title="Energia (Φ)"
            value={Phi}
            eq={"\\Phi = \\langle x^2 \\rangle"}
            desc="Momento de segunda ordem do campo."
          />

          <MetricCard
            title="Expoente de Lyapunov (λ)"
            value={lyap}
            eq={"\\lambda \\approx \\log(\\mathrm{Var}(x))"}
            desc="Estimativa baseada na variância do campo."
          />

          <Glass>
            <div className="text-xs mb-2 opacity-70">
              Evolução Temporal
            </div>

            <ResponsiveContainer width="100%" height={120}>
              <LineChart data={history}>
                <Line dataKey="Phi" stroke="#22c55e" dot={false}/>
                <Line dataKey="lyap" stroke="#ef4444" dot={false}/>
              </LineChart>
            </ResponsiveContainer>
          </Glass>

        </div>

      </div>

    </div>
  );
}

/* ========================= */

function Glass({children}){
  return(
    <motion.div
      className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl p-4 shadow-xl"
    >
      {children}
    </motion.div>
  );
}

/* ========================= */

function Field({field}){

  if(!field) return <div>Loading...</div>;

  return(
    <div style={{
      display:"grid",
      gridTemplateColumns:`repeat(${field.length},3px)`
    }}>
      {field.flat().map((v,i)=>{

        const energy = v*v;

        return(
          <div key={i}
            style={{
              width:3,
              height:3,
              background:`hsl(${energy*240},100%,60%)`
            }}
          />
        )
      })}
    </div>
  );
}

/* ========================= */

function MetricCard({title,value,eq,desc}){

  return(
    <Glass>

      <div className="text-xs opacity-70 mb-1">
        {title}
      </div>

      <div className="text-2xl mb-2">
        {value.toFixed(4)}
      </div>

      <BlockMath math={eq}/>

      <div className="text-xs opacity-60 mt-2">
        {desc}
      </div>

    </Glass>
  );
}
